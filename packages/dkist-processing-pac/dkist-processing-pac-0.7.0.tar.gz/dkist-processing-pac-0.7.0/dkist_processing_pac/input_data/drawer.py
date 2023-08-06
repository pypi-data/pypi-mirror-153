"""Container for processed PolCal task data. A single Calibration Sequence produces a single Drawer."""
import logging
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import numpy as np
from astropy.time import Time
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess

from dkist_processing_pac.data import CONSTANTS


class Drawer:
    """
    Container for a single processed set of Calibration Sequence PolCal data.

    In addition to storing the data, a Drawer simplifies retrieval of a single Set of Calibration Curves (SoCC).
    Each SoCC implies a separate polcal fit.

    Distribution of the actual data is handled by slicing into this class. Each slice will provide a SoCC for a given
    (x, y, l) location. The result will be a single array that is M x N where M is the number of modulator states and N
    is the number of steps in the CS.
    In addition to the detector data, this class generates a set of vectors that describe the configuration of the
    Telescope and Calibration Unit during each exposure in the aggregated data.
    """

    def __init__(
        self,
        fits_access_dict: Dict[int, List[L0FitsAccess]],
        skip_darks: bool = True,
        remove_I_trend: bool = True,
    ):
        self.theta_pol_steps = np.array([])
        self.theta_ret_steps = np.array([])
        self.pol_in = np.array([], dtype=bool)
        self.ret_in = np.array([], dtype=bool)
        self.dark_in = np.array([], dtype=bool)
        self.timeobs = np.array([])
        self.nummod: int = 0
        self.numsteps: int = 0
        self.azimuth = np.array([])
        self.elevation = np.array([])
        self.table_angle = np.array([])
        self.mjd_begin: float = np.inf
        self.mjd_end: float = -np.inf
        self.wavelength: float = 0.0
        self.RN: float = 0.0
        self.norm_func = np.poly1d([0.0, 1.0])
        self.I_clear: float = 0.0
        self.clear_objs: List[List[L0FitsAccess]] = []
        self.clear_times: np.ndarray = np.ndarray([])

        self.fits_access_dict = dict()
        self.load_from_dict_of_objects(fits_access_dict, skip_darks=skip_darks)
        if remove_I_trend:
            self.find_clears()
            self.fit_intensity_trend()

    def load_from_dict_of_objects(
        self, raw_fits_access: Dict[int, List[L0FitsAccess]], skip_darks: bool = True
    ):
        """Load processed polcal frames into the Drawer.

        In addition to loading the actual data, FitsAccess properties are inspected to create vectors of the polarizer
        and retarder angles, telescope geometry, and observation times.

        Parameters
        ----------
        raw_fits_access
            Dict where keys are the CS step number and values are a list of FitsAccess objects

        skip_darks
            If True (default) then don't load any dark steps from the CS
        """
        inst_set = set()
        nummod_set = set()
        wave_set = set()
        ip_start_list = []
        ip_end_list = []
        final_step_num = 0
        for cs_step in sorted(raw_fits_access.keys()):
            meta_obj = raw_fits_access[cs_step][0]
            if meta_obj.gos_level0_status == "DarkShutter" and skip_darks:
                continue

            inst_set.add(meta_obj.instrument)
            wave_set.add(meta_obj.wavelength)
            ip_start_list.append(Time(meta_obj.ip_start_time))
            ip_end_list.append(Time(meta_obj.ip_end_time))

            self.azimuth = np.append(self.azimuth, meta_obj.azimuth)
            self.elevation = np.append(self.elevation, meta_obj.elevation)
            self.table_angle = np.append(self.table_angle, meta_obj.table_angle)

            self.theta_pol_steps = np.append(self.theta_pol_steps, meta_obj.gos_polarizer_angle)
            self.theta_ret_steps = np.append(self.theta_ret_steps, meta_obj.gos_retarder_angle)
            self.pol_in = np.append(
                self.pol_in, meta_obj.gos_polarizer_status not in ["undefined", "clear", False]
            )
            self.ret_in = np.append(
                self.ret_in, meta_obj.gos_retarder_status not in ["undefined", "clear", False]
            )
            self.dark_in = np.append(self.dark_in, meta_obj.gos_level0_status == "DarkShutter")

            self.timeobs = np.append(self.timeobs, Time(meta_obj.time_obs).mjd)
            nummod_set.add(meta_obj.number_of_modulator_states)
            self.fits_access_dict[final_step_num] = raw_fits_access[
                cs_step
            ]  # So the index is still correct after skipping darks
            final_step_num += 1

        if len(nummod_set) > 1:
            raise ValueError("Not all input files have the same number of modulator states")
        self.nummod = nummod_set.pop()

        if len(inst_set) > 1:
            raise ValueError("Data belong to more than one instrument")
        self.instrument = inst_set.pop()

        if len(wave_set) > 1:
            raise ValueError("Data have more than one wavelength")
        self.wavelength = wave_set.pop()

        self.mjd_begin = min(ip_start_list).mjd
        self.mjd_end = max(ip_end_list).mjd

        # TODO: Make this match Data (probably by changing Data???)
        # noise_floor_dict = CONSTANTS['Fallback_noise_floors']
        self.RN = 0.0

        self.numsteps = len(self.fits_access_dict.keys())

    def __repr__(self):
        return "<PolCal SoCC Drawer started at {} with (m,n) = ({}, {}) and shape = {}>".format(
            self.mjd_begin, self.nummod, self.numsteps, self.shape
        )

    def __getitem__(self, item: Union[Tuple[int, int, int], Tuple[np.ndarray]]) -> np.ndarray:
        """Return a single SoCC from the Drawer.

        The slice must have three elements (x, y, l). E.g.:

            >>> I = DRWR[x, y, l]

        Parameters
        ----------
        item : tuple
            The (x, y, l) position tuple. Don't worry, python's slicing syntax will take care of this for you.

        Returns
        -------
        numpy.ndarray
            A 2D array of shape (M, N) where M is the number of modulator states and N is the number of steps in the
            Calibration Sequence.

        """
        if type(item) is not tuple or len(item) != 3:
            raise IndexError("Drawer must be indexed by exactly three values")

        xpos, ypos, lpos = item

        if (
            not np.issubdtype(type(xpos), np.integer)
            or not np.issubdtype(type(ypos), np.integer)
            or not np.issubdtype(type(lpos), np.integer)
        ):
            raise IndexError("Only integers are allowed as valid indices")

        result = np.zeros((self.nummod, self.numsteps), dtype=np.float64)

        for n in range(self.numsteps):
            obj_list = self.fits_access_dict[n]
            modnum_list = [h.modulator_state for h in self.fits_access_dict[n]]
            for m in range(self.nummod):
                idx = modnum_list.index(m + 1)
                result[m, n] = obj_list[idx].data[xpos, ypos, lpos] / self.norm_func(
                    self.timeobs[n]
                )

        return result

    @property
    def shape(self) -> Tuple[int]:
        """Return the shape of this object's 'data'.

        This is useful for those who will be using the slicing functionality and expect to be able to see the shape of
        these data.
        """
        data = self.fits_access_dict[0][0].data

        return data.shape

    def find_clears(self) -> None:
        """Identify which FitsAccess objects contain clear observations and populate self.clear_objs.

        A clear frame is defined as one in which both the polarizer and retarder were out of the light path.
        """
        clear_objs = []
        clear_times = np.array([])
        for n in range(self.numsteps):
            if not self.pol_in[n] and not self.ret_in[n] and not self.dark_in[n]:
                clear_objs.append(self.fits_access_dict[n])
                clear_times = np.append(clear_times, self.timeobs[n])

        self.clear_objs = clear_objs
        self.clear_times = clear_times

    def fit_intensity_trend(self) -> None:
        """Use clear frames to fit any global intensity trends.

        The flux in each clear is averaged over all modulation states and the set of all clears is used to fit a linear
        trend of flux vs time. This line is then stored for application on SoCC retrieval.

        Note that because the absolute offset (i.e., intercept) is also fit the overall intensity is normalized by
        something very close to the flux in the first clear measurement.
        """
        try:
            avg_clear_flux = np.zeros(len(self.clear_objs))
        except AttributeError:
            logging.info(
                "WARNING: clear frames have not yet been identified. Use .find_clears() to do so"
            )
            return
        if len(self.clear_objs) == 0:
            logging.info(
                "WARNING: this Drawer does not contain any clear measurements. No correction is possible."
            )
            return

        # First, get the linear trend in clear intensity
        for n in range(len(self.clear_objs)):
            tmp = 0.0
            for j in range(self.nummod):
                tmp += np.nanmean(self.clear_objs[n][j].data)
            avg_clear_flux[n] = tmp / self.nummod

        self.I_clear = np.mean(avg_clear_flux)
        logging.info(f"Average flux in clear measurements (I_clear): {self.I_clear:<10.3f}")
        if self.I_clear < CONSTANTS["min_clear_flux"]:
            raise ValueError(
                "Flux in Clear measurements is too low ({:.2f} < {:.2f})".format(
                    self.I_clear, CONSTANTS["min_clear_flux"]
                )
            )
        fit = np.poly1d(np.polyfit(self.clear_times, avg_clear_flux, 1)) / self.I_clear
        self.norm_func = fit

    def get_uncertainty(self, data: np.ndarray) -> np.ndarray:
        """Compute the uncertainty (for weighting the fit) of a set of data.

        Right now this just computes a very simply noise estimate. In the future it will be able to read from
        uncertainty frames provided by the IPAs
        """
        return np.sqrt(np.abs(data) + self.RN**2)
