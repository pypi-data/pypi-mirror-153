"""Machinery to collect data and parameter objects and spawn fits for each FOV point."""
import copy
import logging
import time

import lmfit
import numpy as np
from lmfit import Parameters

from dkist_processing_pac.fitter.fitter_parameters import NdParameterArray
from dkist_processing_pac.fitter.fitter_parameters import PolcalDresserParameters
from dkist_processing_pac.fitter.fitting_core import compare_I
from dkist_processing_pac.input_data.dresser import Dresser
from dkist_processing_pac.optics.calibration_unit import CalibrationUnit
from dkist_processing_pac.optics.telescope import Telescope


class PolcalFitter:
    """Object that brings together data (Dresser), optic models (CM and TM), and fit parameters (PolcalDresserParameters) to run fits."""

    def __init__(
        self,
        *,
        dresser: Dresser,
        fit_mode: str,
        init_set: str,
        fit_TM: bool = False,
        threads: int = 1,
        super_name: str = "",
        _dont_fit: bool = False,
        **fit_kwargs,
    ):

        self.fits_have_run = False
        self.dresser = dresser
        self.fit_TM = fit_TM

        # Initialize Calibration Unit and Telescope Models with the geometry from the dresser
        self.CM = CalibrationUnit(self.dresser)
        self.TM = Telescope(self.dresser)

        # Set up fitting switches and global initial values
        self.full_params = PolcalDresserParameters(self.dresser, fit_mode, init_set)

        # Initialize CM and TM objects with global starting guesses. The point-specific initialization on the CM
        # happens inside run_fits
        global_params = self.full_params.init_params._all_parameters[0]
        pardict = global_params.valuesdict()
        self.CM.load_pars_from_dict(pardict)
        self.TM.load_pars_from_dict(pardict)

        if not _dont_fit:
            self.run_fits(threads=threads, super_name=super_name, **fit_kwargs)

    @property
    def demodulation_matrices(self) -> np.ndarray:
        """Return the best-fit demodulation matrices if fits have been run, otherwise raise an error."""
        if not self.fits_have_run:
            raise ValueError("Cannot access demodulation matrices until fits have been run")

        return self.full_params.demodulation_matrices

    @property
    def fit_parameters(self) -> NdParameterArray:
        """Return the best-fit parameters."""
        if not self.fits_have_run:
            raise ValueError("Cannot access best-fit parameters until fits have been run")

        return self.full_params.fit_params

    def run_fits(self, *, threads: int = 1, super_name: str = "", **fit_kwargs):
        """Start a minimizer for each FOV point and record the results.

        This is also where the non-CU parameters are initialized for each FOV point. This happens prior to fitting.
        """
        use_M12 = self.full_params.switches["use_M12"]
        fov_shape = self.dresser.shape
        num_fits = np.prod(fov_shape)
        self.print_starting_values(self.full_params.init_params[0, 0, 0], global_pars=True)
        for i in range(num_fits):
            # These lines ensure that all FOV points have the same CU and TM starting parameters.
            # If we don't deepcopy then each point will start off at the best-fit of the previous point, which is not
            # strictly wrong, just not how we do it.
            point_TM = copy.deepcopy(self.TM)
            point_CM = copy.deepcopy(self.CM)

            # Get the correct SoCC out of the Dresser (heyo!)
            idx = np.unravel_index(i, fov_shape)
            logging.info(f"Fitting point {idx}")
            I_cal, I_unc = self.dresser[idx]

            # Initialize sensible starting values for non-CU parameters
            self.full_params.initialize_single_point_parameters(idx, CM=point_CM, TM=point_TM)
            params_to_fit = self.full_params.init_params[idx]
            self.print_starting_values(params_to_fit, global_pars=False)

            # We use a single array object to contain the modulation matrix so a new object is created during each
            # fit iteration
            modmat = np.zeros((I_cal.shape[0], 4), dtype=np.float64)

            t1 = time.time()
            mini = lmfit.Minimizer(
                compare_I,
                params_to_fit,
                fcn_args=(I_cal, I_unc, point_TM, point_CM, modmat),
                fcn_kws={"use_M12": use_M12},
            )
            logging.info("starting minimizer")
            fit_out = mini.minimize(method="leastsq", params=params_to_fit, **fit_kwargs)
            logging.info(
                f"minimization completed in {time.time() - t1:4.1f} s. Chisq = {fit_out.chisqr:8.2e}, redchi = {fit_out.redchi:8.2e}"
            )

            # Save the best-fit parameters
            self.full_params.fit_params[idx] = fit_out.params

        self.fits_have_run = True

    @staticmethod
    def print_starting_values(params: Parameters, global_pars: bool = True):
        """Print out free and fixed parameter values.

        If `global_pars` is True then only parameters pertaining to all FOV points will be printed. If it is False then
        *only* parameters pertaining to FOV points will be printed.
        """
        fixed_pars = dict()
        free_pars = dict()

        for name, par in params.items():
            if ("I_sys" in name or "modmat" in name) is global_pars:
                continue
            if par.vary:
                free_pars[name] = par.value
            else:
                fixed_pars[name] = par.value

        logging.info(f"{'Global' if global_pars else 'Point'} fixed parameters:")
        for p, v in fixed_pars.items():
            logging.info(f"\t{p} = {v:0.5f}")

        logging.info(f"{'Global' if global_pars else 'Point'} free parameters:")
        for p, v in free_pars.items():
            logging.info(f"\t{p} = {v:0.5f}")
