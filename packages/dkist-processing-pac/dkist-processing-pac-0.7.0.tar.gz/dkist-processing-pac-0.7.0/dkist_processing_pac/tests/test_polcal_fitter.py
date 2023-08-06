import numpy as np

from dkist_processing_pac.fitter.polcal_fitter import PolcalFitter


def test_polcal_fitter_init(general_dresser, test_fit_mode, test_init_set):
    """
    Given: a Dresser and names of a fit mode and init set
    When: initializing a PolcalFitter object with these inputs
    Then: everything needed for the fit is correctly set up
    """
    mode_name, true_switches, true_vary = test_fit_mode
    init_name, true_CU_pars, true_TM_pars = test_init_set
    fitter = PolcalFitter(
        dresser=general_dresser, init_set=init_name, fit_mode=mode_name, _dont_fit=True
    )
    wave_idx = np.argmin(np.abs(general_dresser.wavelength - true_CU_pars["wave"]))

    for par_name, prop_name in zip(
        ["t_ret", "t_pol", "ret0h", "ret045", "ret0r"],
        ["t_ret_0", "t_pol_0", "ret_0_h", "ret_0_45", "ret_0_r"],
    ):
        assert getattr(fitter.CM, prop_name)[0] == true_CU_pars["params"][par_name][wave_idx, 1]

    for p in ["x12", "t12", "x34", "t34", "x56", "t56"]:
        assert getattr(fitter.TM, p) == fitter.full_params.init_params[0, 0, 0][p]

    for s in true_switches.keys():
        assert true_switches[s] == fitter.full_params.switches[s]

    for v in true_vary.keys():
        assert true_vary[v] == fitter.full_params.vary[v]


def test_polcal_fitter_correct(fully_realistic_dresser, visp_modulation_matrix):
    """
    Given: a realistic set of polcal input data
    When: actually running the fit
    Then: the correct demodulation matrices are computed
    """
    fitter = PolcalFitter(dresser=fully_realistic_dresser, fit_mode="use_M12", init_set="OCCal_VIS")
    assert fitter.demodulation_matrices.shape == (1, 1, 1, 4, 10)
    np.testing.assert_allclose(
        fitter.demodulation_matrices[0, 0, 0], np.linalg.pinv(visp_modulation_matrix), rtol=1e-3
    )
