"""Top-level container for processed PolCal data. A Dresser contains any number of Drawers."""
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np

from dkist_processing_pac.input_data.drawer import Drawer


class Dresser:
    """Dresser is a collection of Drawer objects.

    It's primary function is to allow fitting code to not have to worry about how many Drawers the user has
    provided for, e.g., fitting the M36 group parameters.

    This class doesn't do much except keep track of the Drawers and concatenate a StoCCinG when a user asks for a
    specific location.

    Its attributes are basically the same as those of Drawer
    """

    def __init__(self):
        """Create a new class instance.

        This is easy; just initialize all the arrays that might eventually hold stuff.
        """
        self.drawers: List[Drawer] = []
        self.azimuth = np.array([])
        self.elevation = np.array([])
        self.table_angle = np.array([])
        self.theta_pol_steps = np.array([])
        self.theta_ret_steps = np.array([])
        self.pol_in = np.array([], dtype=bool)
        self.ret_in = np.array([], dtype=bool)
        self.dark_in = np.array([], dtype=bool)
        self.delta_t = np.array([])
        self.nummod: int = 0
        self.numsteps: int = 0
        self.mjd_begin: float = np.inf
        self.mjd_end: float = -np.inf
        self.wavelength: float = 0.0
        self.instrument: Optional[str] = None
        self.shape: Tuple[int, int, int] = ()

    def __repr__(self) -> str:

        rprstr = "<PolCal Dresser with (m,n) = ({}, {}) and the following Drawers:\n".format(
            self.nummod, self.numsteps
        )
        for d in self.drawers:
            rprstr += " {}\n".format(d)
        rprstr += ">"

        return rprstr

    @property
    def numdrawers(self) -> int:
        """Return the number of Drawers (AKA Calibration Sequences) in this Dresser."""
        return len(self.drawers)

    @property
    def drawer_step_list(self) -> List[int]:
        """Return the number of CS steps in each Drawer."""
        return [d.numsteps for d in self.drawers]

    def add_drawer(self, drawer: Drawer) -> None:
        """Add a Drawer to the Dresser.

        Checks are made to ensure the Drawer fits in the Dresser (correct instrument, number of positions, etc.), and
        the CS configuration vectors are updated to include information from the new Drawer.

        Parameters
        ----------
        drawer
            PolCal Data from a single CS
        """
        if self.nummod == 0:
            self.nummod = drawer.nummod
        else:
            if drawer.nummod != self.nummod:
                raise ValueError(
                    f"Trying to add Drawer with {drawer.nummod} mod states to Dresser with {self.nummod}"
                )

        if self.wavelength == 0.0:
            self.wavelength = drawer.wavelength
        else:
            if drawer.wavelength != self.wavelength:
                raise ValueError(
                    f"Drawer with wave = {drawer.wavelength:6.1f} cannot be added to Dresser with wave = {self.wavelength:6.1f}"
                )

        if self.instrument is None:
            self.instrument = drawer.instrument
        else:
            if drawer.instrument != self.instrument:
                raise ValueError(
                    f"Drawer from instrument {drawer.instrument} cannot be added to Dresser from instrument {self.instrument}"
                )

        if self.shape == ():
            self.shape = drawer.shape
        else:
            if drawer.shape != self.shape:
                raise ValueError(
                    f"Drawer with shape {drawer.shape} does not fit into Dresser with shape {self.shape}"
                )

        self.drawers.append(drawer)
        for attr in [
            "azimuth",
            "elevation",
            "table_angle",
            "theta_pol_steps",
            "theta_ret_steps",
            "pol_in",
            "ret_in",
            "dark_in",
        ]:
            setattr(self, attr, np.append(getattr(self, attr), getattr(drawer, attr)))

        self.delta_t = np.append(self.delta_t, drawer.timeobs - np.min(drawer.timeobs))

        self.mjd_begin = min(self.mjd_begin, drawer.mjd_begin)
        self.mjd_end = max(self.mjd_end, drawer.mjd_end)
        self.numsteps += drawer.numsteps

    @property
    def I_clear(self) -> np.ndarray:
        """Return the I_clear property for each Drawer.

        Returns
        -------
        Array of floats with length equal to the number of drawers
        """
        I_clear = np.empty((self.numdrawers,), dtype=np.float64)
        for i, d in enumerate(self.drawers):
            I_clear[i] = d.I_clear

        return I_clear

    def __getitem__(
        self, item: Union[Tuple[int, int, int], Tuple[np.ndarray]]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Concatenate and return all the SoCCs at the same position from each Drawer along with the uncertainty.

        We call this a Set of Calibration Curves in a Group (a StoCCinG).

        Uncertainty is computed using the Drawer's `.get_uncertainty` method.

        Parameters
        ----------
        item: tuple
            The (x, y, l) position tuple. Don't worry, python's slicing syntax will take care of this for you.

        Returns
        -------
        numpy.ndarray
            Array of shape (M, N) where M is the number of modulator states and N is the total number of steps across
            all CS's in all Drawers.

        numpy.ndarray
            Array of the same shape that corresponds to uncertainty on the first array.
        """
        data = np.empty((self.nummod, self.numsteps), dtype=np.float64)
        uncertainty = np.empty(data.shape, dtype=np.float64)

        xpos, ypos, lpos = item

        idx = 0
        for d in self.drawers:
            drawer_data = d[xpos, ypos, lpos]
            data[:, idx : idx + d.numsteps] = drawer_data
            uncertainty[:, idx : idx + d.numsteps] = d.get_uncertainty(drawer_data)
            idx += d.numsteps

        return data, uncertainty
