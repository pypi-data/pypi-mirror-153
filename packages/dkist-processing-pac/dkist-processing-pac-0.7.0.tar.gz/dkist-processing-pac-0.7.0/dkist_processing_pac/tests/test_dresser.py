import numpy as np
import pytest

from dkist_processing_pac.input_data.drawer import Drawer
from dkist_processing_pac.input_data.dresser import Dresser


def test_dresser(general_cs):
    """
    Given: a dictionary of FitsAccess objects corresponding to a set of reduced polcal data
    When: creating a Dresser and adding two Drawers to it with the dictionary
    Then: the Dresser properties are populated correctly
    """
    cs_step_obj_dict = general_cs[0]
    D1 = Drawer(cs_step_obj_dict, skip_darks=False, remove_I_trend=False)
    D2 = Drawer(cs_step_obj_dict, skip_darks=True, remove_I_trend=False)
    DRSR = Dresser()
    DRSR.add_drawer(D1)
    DRSR.add_drawer(D2)

    assert DRSR.nummod == 3
    assert DRSR.numsteps == 7 + 7 - 2
    np.testing.assert_array_equal(
        DRSR.pol_in,
        [False, False, True, True, True, False, False] + [False, True, True, True, False],
    )
    np.testing.assert_array_equal(
        DRSR.theta_pol_steps,
        [-999, -999, 60.0, 0.0, 120.0, -999, -999] + [-999, 60.0, 0.0, 120.0, -999],
    )
    np.testing.assert_array_equal(
        DRSR.ret_in,
        [False, False, False, True, False, False, False] + [False, False, True, False, False],
    )
    np.testing.assert_array_equal(
        DRSR.theta_ret_steps,
        [-999, -999, -999, 45.0, -999, -999, -999] + [-999, -999, 45.0, -999, -999],
    )
    np.testing.assert_array_equal(
        DRSR.dark_in,
        [True, False, False, False, False, False, True] + [False, False, False, False, False],
    )
    assert DRSR.shape == (3, 4, 1)
    cc1 = np.ones((3, 7)) * np.arange(7)[None, :] + 100 * np.arange(3)[:, None]
    cc2 = np.ones((3, 5)) * np.arange(1, 6)[None, :] + 100 * np.arange(3)[:, None]
    cc = np.hstack([cc1, cc2])
    for i in range(np.prod(DRSR.shape)):
        np.testing.assert_array_equal(DRSR[np.unravel_index(i, DRSR.shape)][0], cc)

    # Test that uncertainty is correctly computed
    I1 = D1[0, 0, 0]
    I2 = D2[0, 0, 0]
    I, u = DRSR[0, 0, 0]
    np.testing.assert_array_equal(u, np.hstack((D1.get_uncertainty(I1), D2.get_uncertainty(I2))))


def test_wrong_modnum(general_drawer):
    """
    Given: a Dresser and a Drawer with a different number of modstates
    When: trying to insert the Drawer into the Dresser
    Then: an error is raised
    """
    DRSR = Dresser()
    DRSR.nummod = 99
    with pytest.raises(ValueError):
        DRSR.add_drawer(general_drawer)


def test_wrong_wave(general_drawer):
    """
    Given: a Dresser and a Drawer with a different wavelength
    When: trying to insert the Drawer into the Dresser
    Then: an error is raised
    """
    DRSR = Dresser()
    DRSR.wavelength = 999
    with pytest.raises(ValueError):
        DRSR.add_drawer(general_drawer)


def test_wrong_instrument(general_drawer):
    """
    Given: a Dresser and a Drawer from a different instrument
    When: trying to insert the Drawer into the Dresser
    Then: an error is raised
    """
    DRSR = Dresser()
    DRSR.instrument = "NOTHING"
    with pytest.raises(ValueError):
        DRSR.add_drawer(general_drawer)


def test_wrong_shape(general_drawer):
    """
    Given: a Dresser and a Drawer with a different data shape
    When: trying to insert the Drawer into the Dresser
    Then: an error is raised
    """
    DRSR = Dresser()
    DRSR.shape = (99,)
    with pytest.raises(ValueError):
        DRSR.add_drawer(general_drawer)
