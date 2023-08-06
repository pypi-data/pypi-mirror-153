"""Objects for storing fit parameters."""
from __future__ import annotations

import copy
import logging
import os
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import asdf
import numpy as np
import pkg_resources
import yaml
from lmfit import Parameters

from dkist_processing_pac.fitter.fitting_core import fit_modulation_matrix
from dkist_processing_pac.fitter.fitting_core import generate_S
from dkist_processing_pac.input_data.dresser import Dresser
from dkist_processing_pac.optics.calibration_unit import CalibrationUnit
from dkist_processing_pac.optics.telescope import get_TM_db_location
from dkist_processing_pac.optics.telescope import load_TM_database
from dkist_processing_pac.optics.telescope import Telescope

GLOBAL_PARAMS = ["Q_in", "U_in", "V_in"]


class PolcalDresserParameters:
    """Object for initializing fit parameters prior to a fit and storing the results after the fit."""

    def __init__(self, dresser: Dresser, fit_mode: str, init_set: str):

        self.dresser = dresser
        self.fit_mode = fit_mode
        self.init_set = init_set
        self.fit_TM = False
        self.num_modstates = dresser.nummod
        self.fov_shape = dresser.shape
        mean_time = 0.5 * (dresser.mjd_begin + dresser.mjd_end)

        self.switches, self.vary = self.load_fit_mode(fit_mode)
        single_parameters = self.initialize_CU_parameters(
            wavelength=dresser.wavelength, num_drawers=dresser.numdrawers
        )
        self.initialize_TM_parameters(
            single_params_obj=single_parameters, wavelength=dresser.wavelength, mean_time=mean_time
        )
        self.init_params = NdParameterArray(single_parameters, self.fov_shape)
        self.fit_params = NdParameterArray(single_parameters, self.fov_shape)

    @property
    def demodulation_matrices(self) -> np.ndarray:
        """Return the demodulation matrices of all points in the FOV.

        Has shape (X, Y, L, 4, M)
        """
        full_shape = self.fov_shape + (4, self.num_modstates)
        demodulation_matrices = np.zeros(full_shape, dtype=np.float64)
        num_points = np.prod(self.fov_shape)
        for i in range(num_points):
            idx = np.unravel_index(i, self.fov_shape)
            params = self.fit_params[idx]

            modmat = np.zeros((self.num_modstates, 4))
            for m in range(self.num_modstates):
                for s, sname in enumerate(["I", "Q", "U", "V"]):
                    modmat[m, s] = params["modmat_{}{}".format(m, sname)].value

            demod = np.linalg.pinv(modmat)
            demodulation_matrices[idx] = demod

        return demodulation_matrices

    @property
    def calibration_unit_init_values(self) -> Dict[str, Union[Dict[str, np.ndarray], np.array]]:
        """Load initial values for the Calibration Unit parameters and return them in a dictionary.

        The return dict has two keys:

        "params" - A dict of {PARAM_NAME: np.ndarray with shape (W, 3)}. The 2nd dimension is [min, value, max]
        "wave" - A ndarray of length W corresponding to the wavelength index in the "params" dict
        """
        cu_init_file = pkg_resources.resource_filename(
            "dkist_processing_pac", "data/init_values/{}_cu_pars.asdf".format(self.init_set)
        )

        if not os.path.exists(cu_init_file):
            raise FileNotFoundError(
                "Could not find the polcal init value file {}".format(cu_init_file)
            )

        with asdf.open(cu_init_file, "rb", lazy_load=False, copy_arrays=True) as f:
            cu_init_pars = f.tree
            logging.info(f'using initial values from set "{self.init_set}"')

        return cu_init_pars

    @property
    def telescope_init_values(self) -> Dict[str, Union[Dict[str, np.ndarray], np.array]]:
        """Load initial values for the Telescope Model parameters and return them in a dictionary.

        The return dict has two keys:

        "params" - A dict of {PARAM_NAME: np.ndarray with shape (W, 3)}. The 2nd dimension is [min, value, max]
        "wave" - A ndarray of length W corresponding to the wavelength index in the "params" dict
        """
        telescope_init_file = pkg_resources.resource_filename(
            "dkist_processing_pac", "data/init_values/{}_tm_pars.asdf".format(self.init_set)
        )
        if not os.path.exists(telescope_init_file):
            raise FileNotFoundError(
                "Could not find the polcal init value file {}".format(telescope_init_file)
            )
        with asdf.open(telescope_init_file, "rb", lazy_load=False, copy_arrays=True) as f:
            telescope_init_pars = f.tree

        return telescope_init_pars

    @staticmethod
    def load_fit_mode(fit_mode: str) -> Tuple[Dict[str, bool], Dict[str, bool]]:
        """Load a 'fit mode' and return the fitting switches and parameter free-ness.

        A fit mode contains information on which parameters should be free in the fit and which should be fixed to
        their starting values. It also controls a few "switches" that set things like weather to use the M12 Mueller
        matrix in the fit.
        """
        mode_file = pkg_resources.resource_filename(
            "dkist_processing_pac", "data/fit_modes/{}.yml".format(fit_mode)
        )
        if not os.path.exists(mode_file):
            raise FileNotFoundError("Could not find file for recipe '{}'".format(fit_mode))

        with open(mode_file, "rb") as f:
            recipe = yaml.load(f, Loader=yaml.SafeLoader)
            logging.info(f'using PA&C fitting mode "{fit_mode}"')

        switches = recipe["switches"]
        vary = recipe["vary"]

        return switches, vary

    def initialize_CU_parameters(self, wavelength: float, num_drawers: int) -> Parameters:
        """Create a single lmfit `Parameters` object with correct starting values for the CU parameters.

        The CU parameters will be constant for all points in the FOV. The point-specific parameter starting values
        are set in
        """
        cu_init_pars = self.calibration_unit_init_values

        wave_idx = np.argmin(np.abs(cu_init_pars["wave"] - wavelength))
        single_params_obj = Parameters()

        # Insert polcal parameters
        for p in cu_init_pars["params"].keys():
            val = cu_init_pars["params"][p][
                wave_idx, 1
            ]  # The 1 refers to a slice in the [min, value, max] 1st dimension
            vary = self.vary[p]
            if p not in GLOBAL_PARAMS:
                for d in range(num_drawers):
                    single_params_obj.add(f"{p}_CS{d:02n}", vary=vary, value=val)
            else:
                single_params_obj.add(p, vary=vary, value=val)

        # Now add I_sys. This is separate because I_sys is set based on the actual data values
        for d in range(num_drawers):
            val = self.dresser.I_clear[d]
            vary = self.vary["I_sys"]
            single_params_obj.add("I_sys_CS{:02n}".format(d), value=val, vary=vary)

        ## Set global transmission
        #
        if self.switches["global_transmission"]:
            # Kind of a hack; if global transmission is desired then we tie all transmissions to the first transmission
            pol_expr_str = "1. * t_pol_CS00"
            ret_expr_str = "1. * t_ret_CS00"
            for i in range(
                1, num_drawers
            ):  # Start at 1 so we don't infinitely recurse on the "global" value
                single_params_obj["t_pol_CS{:02n}".format(i)].set(expr=pol_expr_str)
                single_params_obj["t_ret_CS{:02n}".format(i)].set(expr=ret_expr_str)

        ## Set global retardance values
        #
        if self.switches["global_retardance"]:
            expr_str_h = "1. * ret0h_CS00"
            expr_str_45 = "1. * ret045_CS00"
            expr_str_r = "1. * ret0r_CS00"
            for i in range(1, num_drawers):
                single_params_obj["ret0h_CS{:02n}".format(i)].set(expr=expr_str_h)
                single_params_obj["ret045_CS{:02n}".format(i)].set(expr=expr_str_45)
                single_params_obj["ret0r_CS{:02n}".format(i)].set(expr=expr_str_r)

        ## If M12 will be used then we force Q_in, to be fixed at zero
        #
        if self.switches["use_M12"]:
            logging.info("Using M12 Mueller matrix and fixing Q_in = 0")
            single_params_obj["Q_in"].set(vary=False, value=0.0)

        ## Add the modulation matrix variables
        #
        for m in range(self.num_modstates):
            for s in ["I", "Q", "U", "V"]:
                single_params_obj.add("modmat_{}{}".format(m, s), value=0)

        # Now set modmat_0I to 1 and fix it. This ensures all the normalization stuff stays in I_sys
        single_params_obj["modmat_0I"].set(value=1, vary=False)

        return single_params_obj

    def initialize_TM_parameters(
        self, single_params_obj: Parameters, wavelength: float, mean_time: float
    ):
        """Load telescope parameter values into a given single `Parameters` object.

        If fit_TM is True then the values are taken from the initial value table. If fit_TM is False (more likely),
        then the values are taken from the telescope parameter look-up database.
        """
        tm_init_pars = self.telescope_init_values
        wave_idx = np.argmin(np.abs(tm_init_pars["wave"] - wavelength))

        tm_db_file = get_TM_db_location()
        tm_db_pars = load_TM_database(
            db_file=tm_db_file, wavelength=wavelength, mean_time=mean_time
        )

        tm_par_names = ["x12", "t12", "x34", "t34", "x56", "t56"]

        for p in tm_par_names:
            if self.fit_TM:
                val = tm_init_pars["params"][p][wave_idx, 1]
            else:
                val = tm_db_pars[p]
            single_params_obj.add(p, vary=self.fit_TM, value=val)

        # M12 mirror parameters *NEVER* vary because the methods in this package cannot constrain these
        # parameters
        single_params_obj["x12"].set(vary=False)
        single_params_obj["t12"].set(vary=False)

        return single_params_obj

    def initialize_single_point_parameters(
        self,
        idx: Tuple[Union[int, np.ndarray], ...],
        CM: CalibrationUnit,
        TM: Telescope,
    ):
        """Set non-CU parameters for a single point based on the input data."""
        point_params = self.init_params[idx]
        I_clears = self.dresser.I_clear
        I_cal, _ = self.dresser[idx]

        self.initialize_modulation_matrix(point_params, I_cal, CM, TM)

        for d in range(self.dresser.numdrawers):
            val = I_clears[d]
            point_params[f"I_sys_CS{d:02n}"].set(value=val)

    def initialize_modulation_matrix(
        self,
        params: Parameters,
        I_cal: np.ndarray,
        CM: CalibrationUnit,
        TM: Telescope,
    ):
        """Compute a first-guess modulation matrix given an initial set of CU parameters and input SoCC.

        Then set the actual modulation matrix fitting parameters based on this first-guess.
        """
        S = generate_S(TM, CM, use_M12=self.switches["use_M12"])
        O = fit_modulation_matrix(I_cal, S)

        for m in range(O.shape[0]):
            for i, s in enumerate(["I", "Q", "U", "V"]):
                params["modmat_{}{}".format(m, s)].set(value=O[m, i])

        # Just in case
        params["modmat_0I"].set(value=1)


class NdParameterArray:
    """Store single lmfit `Parameters` objects for an N-dimensional set of points.

    This is basically a normal python list, but with some sneaky indexing to make it look like it has the same shape
    as the fit FOV.
    """

    def __init__(self, parameters: Parameters, fake_shape: tuple):

        self.fake_shape = fake_shape
        num_points = np.prod(fake_shape)
        self._all_parameters: List[Parameters] = [
            copy.deepcopy(parameters) for _ in range(num_points)
        ]

    def __getitem__(self, multi_idx: Tuple[Union[int, np.ndarray], ...]) -> Parameters:
        true_idx = self._get_true_idx(multi_idx)
        return self._all_parameters[true_idx]

    def __setitem__(self, multi_idx: Tuple[Union[int, np.ndarray], ...], new_params: Parameters):
        true_idx = self._get_true_idx(multi_idx)
        self._all_parameters[true_idx] = new_params

    def _get_true_idx(self, multi_idx: Tuple[Union[int, np.ndarray], ...]) -> int:
        return int(np.ravel_multi_index(multi_idx, self.fake_shape))
