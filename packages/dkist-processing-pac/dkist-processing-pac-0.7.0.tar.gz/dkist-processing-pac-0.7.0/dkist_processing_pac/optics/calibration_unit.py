"""Optical model for the GOS Calibration Unit."""
import logging
from typing import Dict

import numpy as np
import pkg_resources

from dkist_processing_pac.input_data.dresser import Dresser
from dkist_processing_pac.optics.mueller_matrices import elliptical_retarder_matrix
from dkist_processing_pac.optics.mueller_matrices import polarizer_matrix
from dkist_processing_pac.optics.mueller_matrices import rotation_matrix


class CalibrationUnit:
    """Compute the Mueller matrices of the Calibration Unit at each step in a Calibration Sequence.

    The sequence is defined by vectors containing the angles of the polarizer and retarder, but each of these elements
    can either be inserted or removed from the beam as necessary.

    The complete model of the Calibration Unit consists of a polarizer followed by an elliptical retarder. The set of
    Mueller matrices for each element can be accessed directly and are updated in real time whenever they are queried.

    The set of N (number of steps) Mueller matrices for the entire CU is accessed via the .CM property.

    The fact that all components of the model are recomputed each time they are queried makes this class a natural fit
    for iterative fitting techniques.

    Multiple Calibration Sequences can be strung together with the + operator. This simply stores all CS's in the same
    object; each CS is allowed to have its own set of parameters.

    Notes
    -----
    The three retardance values (horizontal, 45 degree, and circular) can vary with time via

            ret_i(t) = ret_0_i + dret_i * (t - t_0),

    where ret_0_i is the retardance at time t_0.

    """

    def __init__(self, dresser: Dresser):
        """Initialize CU parameters from a Dresser.

        Really all this does is automatically set the CS configuration variables (theta_pol_steps, etc.) and then
        initialize zero arrays of the appropriate length for all the parameters that will be fit.

        Parameters
        ----------
        dresser
            Object containing one or more Drawers of SoCCs.
        """
        # For auto-complete stuff
        self.pol_in: np.ndarray = np.empty((1,))
        self.ret_in: np.ndarray = np.empty((1,))
        self.dark_in: np.ndarray = np.empty((1,))
        self.delta_t: np.ndarray = np.empty((1,))
        self.numsteps: int = 0

        # Set the Calibration Sequence values
        for attr in [
            "pol_in",
            "ret_in",
            "dark_in",
            "delta_t",
            "numsteps",
        ]:
            setattr(self, attr, getattr(dresser, attr))
        self.theta_pol_steps = np.deg2rad(dresser.theta_pol_steps)
        self.theta_ret_steps = np.deg2rad(dresser.theta_ret_steps)
        self.steps_per_drawer = dresser.drawer_step_list
        self.py = self.load_py_from_database(dresser.wavelength)

        # Set all optical parameters to stupid defaults. They will get initialized later.
        self.Q_in = 0.0
        self.U_in = 0.0
        self.V_in = 0.0
        self.t_pol_0 = 1.0 + np.zeros(dresser.numdrawers, dtype=np.float64)
        self.t_ret_0 = 1.0 + np.zeros(dresser.numdrawers, dtype=np.float64)
        self.I_sys = 1.0 + np.zeros(dresser.numdrawers, dtype=np.float64)
        self.ret_0_h = np.zeros(dresser.numdrawers, dtype=np.float64)
        self.dret_h = np.zeros(dresser.numdrawers, dtype=np.float64)
        self.ret_0_45 = np.zeros(dresser.numdrawers, dtype=np.float64)
        self.dret_45 = np.zeros(dresser.numdrawers, dtype=np.float64)
        self.ret_0_r = np.zeros(dresser.numdrawers, dtype=np.float64)
        self.dret_r = np.zeros(dresser.numdrawers, dtype=np.float64)

    @property
    def numdrawers(self) -> int:
        """Return the number of Drawers (AKA CS's) represented in this object."""
        return len(self.steps_per_drawer)

    def load_pars_from_dict(self, params: Dict[str, float]) -> None:
        """Update CU Model parameters based on a dictionary of the same.

        Parameters
        ----------
        params : dict
            CU Model parameter key: value pairs
        """
        self.Q_in = params["Q_in"]
        self.U_in = params["U_in"]
        self.V_in = params["V_in"]

        for i in range(self.numdrawers):
            self.t_pol_0[i] = params[f"t_pol_CS{i:02n}"]
            self.t_ret_0[i] = params[f"t_ret_CS{i:02n}"]

            self.I_sys[i] = params[f"I_sys_CS{i:02n}"]

            self.ret_0_h[i] = params[f"ret0h_CS{i:02n}"]
            self.ret_0_45[i] = params[f"ret045_CS{i:02n}"]
            self.ret_0_r[i] = params[f"ret0r_CS{i:02n}"]

    @staticmethod
    def load_py_from_database(wavelength: float) -> float:
        """Compute the transmission coefficient in the y direction (py).

        Linear interpolation is used to match the input wavelength. py values outside the database wavelength range
        are simply extended from the min/max database values.
        """
        wave, py = np.loadtxt(
            pkg_resources.resource_filename("dkist_processing_pac", "data/py_table.txt"),
            unpack=True,
        )
        py = np.interp(wavelength, wave, py)
        logging.info(f"py = {py:7.6f} at {wavelength:4n} nm")
        return py

    @property
    def t_pol(self) -> np.ndarray:
        """Return the transmission of the polarizer at each step in the CS.

        If multiple CS's exist then the transmission will be valid for the entire suite.

        Returns
        -------
        numpy.ndarray
            Array of shape (N,)
        """
        t_pol = np.ones(self.numsteps)
        id1 = 0
        id2 = 0

        for i in range(self.numdrawers):
            id2 += self.steps_per_drawer[i]
            t_pol[id1:id2] = self.t_pol_0[i]
            id1 = id2

        return t_pol

    @property
    def t_ret(self) -> np.ndarray:
        """Return the transmission of the retarder at each step in the CS.

        If multiple CS's exist then the transmission will be valid for the entire suite.

        Returns
        -------
        numpy.ndarray
            Array of shape (N,)
        """
        t_ret = np.ones(self.numsteps)
        id1 = 0
        id2 = 0

        for i in range(self.numdrawers):
            id2 += self.steps_per_drawer[i]
            t_ret[id1:id2] = self.t_ret_0[i]
            id1 = id2

        return t_ret

    @property
    def S_in(self) -> np.ndarray:
        """Return the Stokes vector incident on the Calibration Unit.

        NOTE that this does not include the effects of M12. S_in is parametrized via:

        S_in = I_sys * [1, Q_in, U_in, V_in]

        Returns
        -------
        numpy.ndarray
            Array of shape (N,4)
        """
        S_in = np.zeros((self.numsteps, 4), dtype=np.float64)
        id1 = 0
        id2 = 0

        for i in range(self.numdrawers):
            id2 += self.steps_per_drawer[i]

            S_in[id1:id2] = self.I_sys[i] * np.array(
                [[1.0, self.Q_in, self.U_in, self.V_in]] * self.steps_per_drawer[i]
            )
            id1 = id2

        return S_in

    @property
    def ret_h(self) -> np.ndarray:
        """Return the computed horizontal retardance at each step of the CS.

        If multiple CS's exist then ret will be valid for the entire suite.

        Returns
        -------
        numpy.ndarray
            Array of shape (N,)
        """
        ret = np.zeros(self.numsteps)
        id1 = 0
        id2 = 0

        for i in range(self.numdrawers):
            id2 += self.steps_per_drawer[i]
            ret[id1:id2] = self.ret_0_h[i] + self.dret_h[i] * self.delta_t[id1:id2]
            id1 = id2

        return ret

    @property
    def ret_45(self) -> np.ndarray:
        """Return the computed diagonal retardance at each step of the CS.

        If multiple CS's exist then ret will be valid for the entire suite.

        Returns
        -------
        numpy.ndarray
            Array of shape (N,)
        """
        ret = np.zeros(self.numsteps)
        id1 = 0
        id2 = 0

        for i in range(self.numdrawers):
            id2 += self.steps_per_drawer[i]
            ret[id1:id2] = self.ret_0_45[i] + self.dret_45[i] * self.delta_t[id1:id2]
            id1 = id2

        return ret

    @property
    def ret_r(self) -> np.ndarray:
        """Return the computed circular retardance at each step of the CS.

        If multiple CS's exist then ret will be valid for the entire suite.

        Returns
        -------
        numpy.ndarray
            Array of shape (N,)
        """
        ret = np.zeros(self.numsteps)
        id1 = 0
        id2 = 0

        for i in range(self.numdrawers):
            id2 += self.steps_per_drawer[i]
            ret[id1:id2] = self.ret_0_r[i] + self.dret_r[i] * self.delta_t[id1:id2]
            id1 = id2

        return ret

    @property
    def pol_mat(self) -> np.ndarray:
        """Return Mueller matrices of the polarizer for each CS step.

        Returns
        -------
        numpy.ndarray
            Array of shape (N, 4, 4)
        """
        pol_mat = np.empty((self.numsteps, 4, 4), dtype=np.float64)
        t_pol = self.t_pol

        for i in range(self.numsteps):
            if self.pol_in[i]:
                theta_pol = (
                    -self.theta_pol_steps[i] + np.pi / 2.0
                )  # Header/213 coordinate conversion
                rot_in = rotation_matrix(theta_pol)
                rot_out = rotation_matrix(-theta_pol)

                pol_mat[i] = rot_out @ polarizer_matrix(t_pol[i], self.py) @ rot_in
            else:
                pol_mat[i] = np.diag(np.ones(4, dtype=np.float64))

        return pol_mat

    @property
    def ret_mat(self) -> np.ndarray:
        """Return Mueller matrices of the retarder for each step in the CS.

        Returns
        -------
        numpy.ndarray
            Array of shape (N, 4, 4)
        """
        ret_mat = np.empty((self.numsteps, 4, 4), dtype=np.float64)
        t_ret = self.t_ret
        ret_h = self.ret_h
        ret_45 = self.ret_45
        ret_r = self.ret_r

        for i in range(self.numsteps):
            if self.ret_in[i]:
                theta_ret = -self.theta_ret_steps[i]  # Header/213 coordinate conversion
                rot_in = rotation_matrix(theta_ret)
                rot_out = rotation_matrix(-theta_ret)
                ret_mat[i] = (
                    rot_out
                    @ elliptical_retarder_matrix(t_ret[i], ret_h[i], ret_45[i], ret_r[i])
                    @ rot_in
                )
            else:
                ret_mat[i] = np.diag(np.ones(4, dtype=np.float64))

        return ret_mat

    @property
    def dark_mat(self) -> np.ndarray:
        """Return Mueller Matrices of the dark slide for each step of the CS."""
        dark_mat = np.empty((self.numsteps, 4, 4), dtype=np.float32)
        for i in range(self.numsteps):
            if self.dark_in[i]:
                dark_mat[i] = np.zeros((4, 4), dtype=np.float32)
            else:
                dark_mat[i] = np.diag(np.ones(4, dtype=np.float32))

        return dark_mat

    @property
    def CM(self) -> np.ndarray:
        """Return Mueller matrices of the entire Calibration Unit for each step of the CS.

        Returns
        -------
        numpy.ndarray
            Array of shape (N, 4, 4)
        """
        return self.ret_mat @ self.pol_mat @ self.dark_mat
