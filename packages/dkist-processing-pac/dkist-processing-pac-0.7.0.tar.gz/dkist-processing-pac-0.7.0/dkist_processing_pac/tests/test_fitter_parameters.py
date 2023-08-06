import numpy as np
import pytest

from dkist_processing_pac.fitter.fitter_parameters import PolcalDresserParameters
from dkist_processing_pac.optics.calibration_unit import CalibrationUnit
from dkist_processing_pac.optics.telescope import get_TM_db_location
from dkist_processing_pac.optics.telescope import load_TM_database
from dkist_processing_pac.optics.telescope import Telescope


def test_dresser_parameters(general_dresser, test_fit_mode, test_init_set):
    """
    Given: a Dresser and names of a fit mode and init set
    When: initializing a set of DresserParameters
    Then: the internal parameters are correctly loaded
    """
    mode_name, true_switches, true_vary = test_fit_mode
    init_name, true_CU_pars, true_TM_pars = test_init_set
    fit_pars = PolcalDresserParameters(
        dresser=general_dresser, fit_mode=mode_name, init_set=init_name
    )

    assert fit_pars.dresser is general_dresser
    assert fit_pars.fit_mode == mode_name
    assert fit_pars.init_set == init_name
    assert fit_pars.fit_TM is False
    assert fit_pars.num_modstates == general_dresser.nummod
    assert fit_pars.fov_shape == general_dresser.shape

    assert fit_pars.switches == true_switches
    assert fit_pars.vary == true_vary

    assert fit_pars.init_params.fake_shape == general_dresser.shape
    assert fit_pars.fit_params.fake_shape == general_dresser.shape

    # test_parameter_list has coverage that fit_pars.init_params was constructed correctly.
    # Thus we can just use a single point's parameters for these tests
    params = fit_pars.init_params[0, 0, 0]
    cu_init_pars = true_CU_pars["params"]
    wave_idx = np.argmin(np.abs(general_dresser.wavelength - true_CU_pars["wave"]))
    assert params["Q_in"].vary is False if true_switches["use_M12"] else true_vary["Q_in"]
    assert (
        params["Q_in"].value == 0 if true_switches["use_M12"] else cu_init_pars["Q_in"][wave_idx, 1]
    )
    assert params["U_in"].vary is False
    assert params["U_in"].value == 0
    assert params["V_in"].vary is False
    assert params["V_in"].value == 0

    assert params["I_sys_CS00"].vary == true_vary["I_sys"]
    assert params["I_sys_CS00"].value == general_dresser.I_clear[0]

    assert params["t_pol_CS00"].vary == true_vary["t_pol"]
    assert params["t_pol_CS00"].value == cu_init_pars["t_pol"][wave_idx, 1]
    assert params["t_ret_CS00"].vary == true_vary["t_ret"]
    assert params["t_ret_CS00"].value == cu_init_pars["t_ret"][wave_idx, 1]

    assert params["ret0h_CS00"].vary == true_vary["ret0h"]
    assert params["ret0h_CS00"].value == cu_init_pars["ret0h"][wave_idx, 1]
    assert params["ret045_CS00"].vary == true_vary["ret045"]
    assert params["ret045_CS00"].value == cu_init_pars["ret045"][wave_idx, 1]
    assert params["ret0r_CS00"].vary == true_vary["ret0r"]
    assert params["ret0r_CS00"].value == cu_init_pars["ret0r"][wave_idx, 1]

    assert params["modmat_0I"].vary is False
    assert params["modmat_0I"].value == 1

    mean_time = 0.5 * (general_dresser.mjd_begin + general_dresser.mjd_end)
    tm_db_file = get_TM_db_location()
    tm_db_pars = load_TM_database(
        db_file=tm_db_file, wavelength=general_dresser.wavelength, mean_time=mean_time
    )
    assert params["x12"].vary is False
    assert params["x12"].value == tm_db_pars["x12"]
    assert params["t12"].vary is False
    assert params["t12"].value == tm_db_pars["t12"]

    assert params["x34"].vary is fit_pars.fit_TM
    assert params["x34"].value == tm_db_pars["x34"]
    assert params["t34"].vary is fit_pars.fit_TM
    assert params["t34"].value == tm_db_pars["t34"]

    assert params["x56"].vary is fit_pars.fit_TM
    assert params["x56"].value == tm_db_pars["x56"]
    assert params["t56"].vary is fit_pars.fit_TM
    assert params["t56"].value == tm_db_pars["t56"]


def test_init_point_parameters(fully_realistic_dresser):
    """
    Given: a Dresser and DresserParameters
    When: initializing starting parameters for a single point in the FOV
    Then: the I_sys and modulation matrix values are correctly populated based on the input data
    """
    full_params = PolcalDresserParameters(
        dresser=fully_realistic_dresser, fit_mode="use_M12", init_set="OCCal_VIS"
    )

    CM = CalibrationUnit(fully_realistic_dresser)
    TM = Telescope(fully_realistic_dresser)
    global_params = full_params.init_params._all_parameters[0]
    pardict = global_params.valuesdict()
    CM.load_pars_from_dict(pardict)
    TM.load_pars_from_dict(pardict)
    full_params.initialize_single_point_parameters((0, 0, 0), CM=CM, TM=TM)

    assert (
        full_params.init_params[0, 0, 0]["I_sys_CS00"].value == fully_realistic_dresser.I_clear[0]
    )
    assert full_params.init_params[0, 0, 0]["modmat_0I"].vary == False
    assert full_params.init_params[0, 0, 0]["modmat_0I"].value == 1.0


@pytest.fixture(scope="session")
def session_full_params(session_dresser, test_fit_mode, test_init_set):

    return PolcalDresserParameters(
        dresser=session_dresser, fit_mode=test_fit_mode[0], init_set=test_init_set[0]
    )


def test_demodulation_matrix(session_full_params):
    """
    Given: DresserParameters
    When: accessing the *de*modulation matrices
    Then: the correct matrix is returned
    """
    mod_mat = np.random.random((session_full_params.num_modstates, 4))
    for m in range(session_full_params.num_modstates):
        for s, sname in enumerate(["I", "Q", "U", "V"]):
            session_full_params.fit_params[0, 0, 0][f"modmat_{m}{sname}"].set(value=mod_mat[m, s])

    all_demod = session_full_params.demodulation_matrices
    assert all_demod.shape == session_full_params.fov_shape + (4, session_full_params.num_modstates)
    np.testing.assert_equal(all_demod[0, 0, 0], np.linalg.pinv(mod_mat))
