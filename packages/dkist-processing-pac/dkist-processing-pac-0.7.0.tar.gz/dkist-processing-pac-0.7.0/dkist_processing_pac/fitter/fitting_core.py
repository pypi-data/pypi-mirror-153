"""Math functions that are used during fitting."""
import numpy as np
from lmfit import Parameters

from dkist_processing_pac.optics import telescope
from dkist_processing_pac.optics.calibration_unit import CalibrationUnit
from dkist_processing_pac.optics.telescope import Telescope


def compare_I(
    params: Parameters,
    I_cal: np.ndarray,
    I_unc: np.ndarray,
    TM: telescope,
    CM: CalibrationUnit,
    modmat: np.ndarray,
    use_M12: bool = True,
) -> np.ndarray:
    """Compute fitness/fitting function for fitting Telescope and CU parameters.

    First, a modulation matrix is determined and then used to generate some model output data. These data are then
    compared to the observed output data.

    Parameters
    ----------
    params
        Object containing information about the parameters to be used in the fit

    I_cal
        Array of shape (M, N) containing the observed intensity for each modulator state (M) in each CS step (N).

    TM
       An object describing the telescope configuration at each step in the CS

    CM
        An object describing the CU configuration at each step in the CS

    modmat
         Object within to place the current iteration's modulation matrix

    use_M12
        If True then include the M12 Mueller matrix

    Returns
    -------
    numpy.ndarray
        Array of shape (M * N,) containing the difference between the observed and modeled data, normalized by the
        observed data. lmfit.minimize handles the squaring and summing internally.
    """
    parvals = params.valuesdict()
    TM.x34 = parvals["x34"]
    TM.t34 = parvals["t34"]
    TM.x56 = parvals["x56"]
    TM.t56 = parvals["t56"]

    CM.load_pars_from_dict(parvals)

    S = generate_S(TM, CM, use_M12=use_M12)
    O = fill_modulation_matrix(parvals, modmat)

    I_mod = generate_model_I(O, S)

    diff = np.ravel((I_mod - I_cal) / I_unc)

    return diff


def generate_S(TM: Telescope, CM: CalibrationUnit, use_M12: bool = True) -> np.ndarray:
    """Compute the Stokes vector immediately after the Calibration Unit.

    Parameters
    ----------
    TM
        The Telescope object used for fitting

    CM
        The CalibrationSequence object used for fitting

    use_M12
        If True then include the M12 Mueller matrix

    Returns
    -------
    numpy.ndarray
        (4, N) array containing the CU output Stokes vector at each step in the CS
    """
    # We always pass light through the CU and then M3-M6
    S = TM.TM @ CM.CM

    if use_M12:
        # If requested put M12 at the front of the stack
        S = S @ TM.M12

    # Now propagate the S_in vector through the Mueller stack
    S = np.sum(S * CM.S_in[:, None, :], axis=2).T

    return S


def fit_modulation_matrix(I_cal: np.ndarray, S: np.ndarray) -> np.ndarray:
    """Find a modulation matrix, O, that satisfies I = O T s.

    In our case the problem will most likely be massively over-constrained so we use a least-squares fit to find O.

    Parameters
    ----------
    M -> number of modulator states
    N -> number of steps in Calibration Sequence

    I_cal : numpy.ndarray
        Array of shape (M, N) containing the observed intensity values

    S : numpy.ndarray
        Array of shape (4, N) containing the model Stokes vector input to the instrument (i.e., after M6)

    Returns
    -------
    numpy.ndarray
        Array of shape (M, 4) containing the instrument modulation matrix.

    """
    # linalg.lstsq solves x for Ax = B, but in our case we want to solve O for I = O S.
    #  Fortunately we can use the identity Ax = B <-> x.T A.T = B.T and therefore recast our problem into the proper
    #  form: I.T = S.T O.T

    fit_matrix = np.linalg.lstsq(S.T, I_cal.T, rcond=None)[0]
    O = fit_matrix.T

    # Here we remove a degree of freedom from the modulation matrix so that the I_sys parameter is not degenerate
    # with an overall scaling of O.
    O /= O[0, 0]

    return O


def fill_modulation_matrix(parvals, modmat):
    """Populate a numpy array with the modulation matrix as described in fitting parameters."""
    nummod = modmat.shape[0]
    for m in range(nummod):
        for i, s in enumerate(["I", "Q", "U", "V"]):
            modmat[m, i] = parvals["modmat_{}{}".format(m, s)]

    return modmat


def generate_model_I(O: np.ndarray, S: np.ndarray) -> np.ndarray:
    """Given models for the telescope, CU, and modulation matrix, construct ideal output data.

    The "input" light is taken from the CalibrationSequence object and is probably unpolarized light ([1,0,0,0]).

    Parameters
    ----------
    O : numpy.ndarray
        Array of shape (M, 4) containing the instrument modulation matrix.

    S : numpy.ndarray
        Array of shape (4, N) containing the model Stokes vector input to the instrument (i.e., after M6)

    Returns
    -------
    numpy.ndarray
        Array of shape (M, N) containing the modeled intensity in each modulation state at each step of the CS.
    """
    I_mod = O @ S

    return I_mod
