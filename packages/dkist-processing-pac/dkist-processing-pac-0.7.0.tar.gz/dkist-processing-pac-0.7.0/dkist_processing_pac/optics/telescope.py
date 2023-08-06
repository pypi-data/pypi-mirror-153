"""Optical model for all DKIST mirrors from M1 up to, but not including, M7."""
from __future__ import annotations

import logging
import warnings
from typing import Dict

import numpy as np
import pkg_resources
import scipy.interpolate as spi
from astropy.time import Time
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess
from scipy.spatial.qhull import QhullError
from sunpy.coordinates import sun

from dkist_processing_pac.input_data.dresser import Dresser
from dkist_processing_pac.optics.mueller_matrices import mirror_matrix
from dkist_processing_pac.optics.mueller_matrices import rotation_matrix

warnings.simplefilter("always", UserWarning)
ATOL = 1e-6
RTOL = 1e-6


def get_TM_db_location() -> str:
    """Return the current location of the telescope model look-up database."""
    return pkg_resources.resource_filename("dkist_processing_pac", "data/telescope_db.txt")


def load_TM_database(
    db_file: str, wavelength: float, mean_time: float, method="linear"
) -> Dict[str, float]:
    """Load (x, t) mirror parameters based on a database of previous measurements.

    Given a date and wavelength, the closest set of parameters is found via interpolation. The default is to use
    linear interpolation, but cubic interpolation can be requested via the `method` parameter.

    If the supplied time or wavelength is outside the parameter space covered by the database then the values
    are set to the closest (time, wave) coordinate rather than extrapolating.

    Parameters
    ----------
    db_file : str
        The path to the database file (see Notes)

    mean_time : float
        The time at which to interpolate the parameters. Format is MJD.

    wavelength : float
        The wavelength at which to interpolate the parameters (nm)

    method : str
        The interpolation method to use. Can be either 'nearest', 'linear' (default), or 'cubic'

    Notes
    -----
    Currently the database is simply a space-delimited text file with the following columns:

        MJD wavelength x12 t12 x34 t34 x56 t56

    """
    times, wave, x12, t12, x34, t34, x56, t56 = np.loadtxt(db_file, unpack=True)
    logging.info(
        f"Loading database parameters from {db_file} for {wavelength} at {Time(mean_time, format='mjd').fits}"
    )
    values = dict()
    for source, target in zip(
        [x12, t12, x34, t34, x56, t56], ["x12", "t12", "x34", "t34", "x56", "t56"]
    ):

        try:
            value = float(
                spi.griddata((times, wave), source, (mean_time, wavelength), method=method)
            )
        except QhullError:
            value = float(
                spi.griddata((times, wave), source, (mean_time, wavelength), method="nearest")
            )

        # griddata returns NaN if out of range
        if np.isnan(value):
            warnings.warn(
                "Requested time/wavelength is outside of the Telescope Database range, using the nearest "
                "in-bounds value"
            )
            value = float(
                spi.griddata((times, wave), source, (mean_time, wavelength), method="nearest")
            )

        logging.info(
            f"loaded {target} = {value:.5f} at {wavelength} nm and {Time(mean_time, format='mjd').fits}"
        )
        values[target] = value

    return values


# TODO: Rewrite based on Dave's new compute_telescope_geom to remove sunpy dependency
def compute_parallactic_angle(time):
    """Calculate the parallactic angle of the Solar disk center at a specific time.

    All angles are in radians.

    Parameters
    ----------
    time : astropy.time.Time
        The absolute date/time at which to compute the parallactic angle

    Returns
    -------
    float
        The parallactic angle of disk center at the time specified [radians]

    """
    dkist_lat = 20.7047 * np.pi / 180
    dkist_long = -156.25 * np.pi / 180
    dec = sun.true_declination(time).value * np.pi / 180.0
    ra = sun.true_rightascension(time).value * 15.0 * np.pi / 180.0
    ha = (
        time.sidereal_time("apparent", longitude=dkist_long * 180 / np.pi).value
        * 15
        * np.pi
        / 180.0
        - ra
    )

    p = np.arctan2(np.sin(ha), np.tan(dkist_lat) * np.cos(dec) - np.sin(dec) * np.cos(ha))

    return p


class Telescope:
    """Build up the Mueller matrix of the full "Telescope Model" for use in PA&C analysis.

    As detailed in the DKIST PolCal Plan this model is parametrized by 3 mirror groups (M12, M34, M56) and the rotation
    matrices between them. The mirror Mueller matrices are calculated in real time from the parameters x (the ratio of
    reflectivity between light parallel and perpendicular to the plane of incidence) and tau (the retardance). The
    rotation matrices are also calculated in real time based on the (alt, az, coude_table) angles of DKIST.

    Each of the matrices in the Telescope Model are individually accessible as properties of the class
    (e.g. Telescope.M34) and the full model exists in the .TM property. Note that the Telescope Model does NOT
    include the M12 group, but that group's Mueller matrix is still included in this object.

    Because each component of the model is recomputed each time it is queried this class lends itself well to iterative
    fitting.

    """

    def __init__(self, dresser: Dresser):
        """Initialize the class with a Dresser.

        Geometry, time, and wavelength are read from the Dresser.
        """
        self.x12 = 1.0
        self.t12 = np.pi
        self.x34 = 1.0
        self.t34 = np.pi
        self.x56 = 1.0
        self.t56 = np.pi
        self.elevation = np.deg2rad(np.atleast_1d(dresser.elevation))
        self.azimuth = np.deg2rad(np.atleast_1d(dresser.azimuth))
        self.table_angle = np.deg2rad(np.atleast_1d(dresser.table_angle))

        if (
            self.elevation.shape != self.azimuth.shape
            or self.elevation.shape != self.table_angle.shape
        ):
            raise ValueError("Telescope geometry vectors do not have the same shape")

        self.numsteps = self.elevation.size

        self.wavelength = dresser.wavelength
        self.mean_time = 0.5 * (dresser.mjd_begin + dresser.mjd_end)

    def load_pars_from_dict(self, params: Dict[str, float]) -> None:
        """Update Telescope Model parameters based on a dictionary of the same.

        Parameters
        ----------
        params : dict
            Telescope Model parameter key: value pairs
        """
        self.x12 = params["x12"]
        self.t12 = params["t12"]
        self.x34 = params["x34"]
        self.t34 = params["t34"]
        self.x56 = params["x56"]
        self.t56 = params["t56"]

    def load_pars_from_database(self):
        """Update Telescope Model parameters from the default location based on time and wavelength attributes.

        A convenience function for instrument pipelines to initialize a correct `Telescope` object quickly.
        """
        db_file = get_TM_db_location()
        pars = load_TM_database(
            db_file=db_file, wavelength=self.wavelength, mean_time=self.mean_time
        )
        self.load_pars_from_dict(pars)

    def generate_inverse_telescope_model(self, M12=True, include_parallactic=True) -> np.ndarray:
        """Produce the inverse of the full Telescope Model's Mueller matrix.

        The user can choose to include M12 as part of the Telescope Model, in which case the inverse will capture all
        polarization effects between the DKIST entrance aperture and M7.

        If, for whatever reason, the generated inverse does not satisfy T int(T) = inv(T) T = Identity then an error
        will be raised.

        Parameters
        ----------
        M12 : bool
            If True then include M12 in the Telescope Model

        include_parallactic : bool
            If True then the final rotation from DKIST to Solar reference frame will be included in the output matrix

        Returns
        -------
        numpy.ndarray
            The (4, 4) inverse Mueller matrix of the Telescope Model.
        """
        full_model = self.TM

        if M12:
            full_model = full_model @ self.M12

        if full_model.shape[0] > 1:
            warnings.warn("Multiple telescope geometries found. Only using the first configuration")

        inverse = np.linalg.inv(full_model[0, :, :])

        if not (
            np.allclose(np.diag(np.ones(4)), inverse @ full_model[0], rtol=RTOL, atol=ATOL)
            and np.allclose(np.diag(np.ones(4)), full_model[0] @ inverse, rtol=RTOL, atol=ATOL)
        ):
            raise ArithmeticError("The generated inverse is not mathematically valid")

        if include_parallactic:
            time = Time(self.mean_time, format="mjd")
            p_rot = rotation_matrix(-1 * compute_parallactic_angle(time))
            inverse = p_rot @ inverse

        return inverse

    @classmethod
    def from_fits_access(cls, fits_obj: L0FitsAccess) -> Telescope:
        """Create a `Telescope` object directly from a single FitsAccess object.

        This is a convenience function for instrument pipelines to quickly create an object that can be used to grab
        an inverse telescope model.
        """
        dresser = Dresser()
        dresser.elevation = np.array([fits_obj.elevation])
        dresser.azimuth = np.array([fits_obj.azimuth])
        dresser.table_angle = np.array([fits_obj.table_angle])
        dresser.wavelength = fits_obj.wavelength

        telescope = cls(dresser=dresser)
        telescope.mean_time = Time(fits_obj.time_obs, format="fits").mjd
        telescope.load_pars_from_database()
        return telescope

    @property
    def M12(self) -> np.ndarray:
        """Return the M12 mirror Mueller matrix."""
        return mirror_matrix(self.x12, self.t12)

    @property
    def M34(self) -> np.ndarray:
        """Return the M34 mirror Mueller matrix."""
        return mirror_matrix(self.x34, self.t34)

    @property
    def M56(self) -> np.ndarray:
        """Return the M56 mirror Mueller matrix."""
        return mirror_matrix(self.x56, self.t56)

    @property
    def R23(self) -> np.ndarray:
        """Return the rotation matrix between M2 and M3. This is always the same, so it doesn't have a step dimension.

        Returns
        -------
        numpy.ndarray
            Array of shape (4, 4)
        """
        return rotation_matrix(-np.pi / 2.0)

    @property
    def R45(self) -> np.ndarray:
        """Return the rotation matrix between M4 and M5.

        Returns
        -------
        numpy.ndarray
            Array of shape (N, 4, 4)
        """
        Rarr = np.empty((self.numsteps, 4, 4), dtype=np.float64)
        for i in range(self.numsteps):
            Rarr[i, :, :] = rotation_matrix(-1 * self.elevation[i])

        return Rarr

    @property
    def R67(self) -> np.ndarray:
        """Return the rotation matrix between M6 and M7.

        Returns
        -------
        numpy.ndarray
            Array of shape (N, 4, 4)
        """
        Rarr = np.empty((self.numsteps, 4, 4), dtype=np.float64)
        for i in range(self.numsteps):
            theta = self.azimuth[i] - self.table_angle[i]
            Rarr[i, :, :] = rotation_matrix(theta)

        return Rarr

    @property
    def TM(self) -> np.ndarray:
        """Return the completed Telescope Model Mueller matrix.

        Returns
        -------
        numpy.ndarray
            Array of shape (N, 4, 4)
        """
        return self.R67 @ self.M56 @ self.R45 @ self.M34 @ self.R23
