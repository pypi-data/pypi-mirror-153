from typing import Dict

import numpy as np
import pytest

from dkist_processing_pac.input_data.dresser import Dresser
from dkist_processing_pac.optics.calibration_unit import CalibrationUnit
from dkist_processing_pac.optics.mueller_matrices import elliptical_retarder_matrix
from dkist_processing_pac.optics.mueller_matrices import polarizer_matrix
from dkist_processing_pac.optics.mueller_matrices import rotation_matrix


def test_dresser_init(general_dresser):
    """
    Given: a Dresser object
    When: initializing a CalibrationUnit object with that Dresser
    Then: the correct properties from the Dresser are loaded into the CalibrationUnit
    """
    CM = CalibrationUnit(general_dresser)
    assert CM.steps_per_drawer == [d.numsteps for d in general_dresser.drawers]
    assert CM.numsteps == general_dresser.numsteps
    assert CM.numdrawers == 1
    assert CM.py == CM.load_py_from_database(general_dresser.wavelength)
    np.testing.assert_array_equal(CM.delta_t, general_dresser.delta_t)
    np.testing.assert_array_equal(CM.pol_in, general_dresser.pol_in)
    np.testing.assert_array_equal(CM.ret_in, general_dresser.ret_in)
    np.testing.assert_array_equal(CM.dark_in, general_dresser.dark_in)
    np.testing.assert_array_equal(CM.theta_pol_steps, np.deg2rad(general_dresser.theta_pol_steps))
    np.testing.assert_array_equal(CM.theta_ret_steps, np.deg2rad(general_dresser.theta_ret_steps))


@pytest.fixture
def general_CM(general_dresser):
    return CalibrationUnit(general_dresser)


@pytest.fixture
def CM_with_two_drawers(general_drawer):
    dresser = Dresser()
    dresser.add_drawer(general_drawer)
    dresser.add_drawer(general_drawer)

    CM = CalibrationUnit(dresser)
    return CM


@pytest.fixture
def parameter_dict() -> Dict[str, float]:
    pdict = {"Q_in": 1.0, "U_in": 2.0, "V_in": 3.0}

    num_drawers = 2
    value = 4
    for i in range(num_drawers):
        pdict["t_pol_CS{:02n}".format(i)] = value
        pdict["t_ret_CS{:02n}".format(i)] = value + 1

        pdict["I_sys_CS{:02n}".format(i)] = value + 2

        pdict["ret0h_CS{:02n}".format(i)] = value + 3
        pdict["ret045_CS{:02n}".format(i)] = value + 5
        pdict["ret0r_CS{:02n}".format(i)] = value + 7
        value += 9

    return pdict


def test_load_params(CM_with_two_drawers, parameter_dict):
    """
    Given: a CalibrationUnit object
    When: populating CU parameters from a parameter dictionary
    Then: the internal attributes are populated correctly
    """
    CM = CM_with_two_drawers
    CM.load_pars_from_dict(parameter_dict)

    assert CM.Q_in == 1.0
    assert CM.U_in == 2.0
    assert CM.V_in == 3.0

    value = 4
    for i in range(CM.numdrawers):
        assert CM.t_pol_0[i] == value
        assert CM.t_ret_0[i] == value + 1

        assert CM.I_sys[i] == value + 2

        assert CM.ret_0_h[i] == value + 3
        assert CM.ret_0_45[i] == value + 5
        assert CM.ret_0_r[i] == value + 7
        value += 9


def test_single_ret(general_CM):
    """
    Given: a CalibrationUnit object
    When: accessing the retardance vectors
    Then: the correct vectors are returned
    """
    psteps = rsteps = np.arange(5)
    pin = rin = din = np.array([1, 1, 0, 0, 1], dtype=np.bool)
    times = np.arange(5) * 1e3 + 4e4

    CM = general_CM
    CM.pol_in = pin
    CM.ret_in = rin
    CM.dark_in = din
    CM.theta_pol_steps = psteps
    CM.theta_ret_steps = rsteps
    CM.delta_t = times - times[0]
    CM.ret_0_h = np.array([4])
    CM.dret_h = np.array([1])
    CM.ret_0_45 = np.array([1])
    CM.dret_45 = np.array([2])
    CM.ret_0_r = np.array([1])
    CM.dret_r = np.array([-1])

    np.testing.assert_array_equal(CM.ret_h, np.arange(5) * 1e3 * 1 + 4)
    np.testing.assert_array_equal(CM.ret_45, np.arange(5) * 1e3 * 2 + 1)
    np.testing.assert_array_equal(CM.ret_r, np.arange(5) * 1e3 * -1 + 1)


def test_pol_mat(general_CM):
    """
    Given: a CalibrationUnit object
    When: accessing the internal polarization matrix
    Then: the correct matrix is returned
    """
    CM = general_CM
    CM.numsteps = 3
    CM.py = 0
    CM.theta_pol_steps = np.deg2rad(np.array([90, 45, 0]))
    CM.theta_ret_steps = np.deg2rad(np.array([-90, 0, 0]))
    CM.pol_in = np.array([True, False, True])
    CM.ret_in = np.array([False, False, False])
    CM.dark_in = np.array([False, False, False])
    CM.delta_t = np.array([0, 10000, 20000])

    truth1 = polarizer_matrix(1, 0)
    truth2 = np.diag(np.ones(4))
    truth3 = rotation_matrix(-np.pi / 2) @ polarizer_matrix(1, 0) @ rotation_matrix(np.pi / 2)

    assert CM.pol_mat.shape == (3, 4, 4)
    np.testing.assert_array_equal(CM.pol_mat[0], truth1)
    np.testing.assert_array_equal(CM.pol_mat[1], truth2)
    np.testing.assert_array_equal(CM.pol_mat[2], truth3)


def test_ret_mat(general_CM):
    """
    Given: a CalibrationUnit object
    When: accessing the internal retarder matrix
    Then: the correct matrix is returned
    """
    CM = general_CM
    CM.numsteps = 3
    CM.theta_pol_steps = np.deg2rad(np.array([90, 45, 0]))
    CM.theta_ret_steps = np.deg2rad(np.array([-90, 0, -45]))
    CM.pol_in = np.array([False, False, False])
    CM.ret_in = np.array([False, True, True])
    CM.dark_in = np.array([False, False, False])
    CM.delta_t = np.array([0, 1, 2])
    CM.ret_0_h = np.array([0])
    CM.dret_h = np.array([1])
    CM.ret_0_45 = np.array([1])
    CM.dret_45 = np.array([2])
    CM.ret_0_r = np.array([1])
    CM.dret_r = np.array([2])

    truth1 = np.diag(np.ones(4))
    truth2 = elliptical_retarder_matrix(1, 1.0, 3.0, 3.0)
    truth3 = (
        rotation_matrix(-np.pi / 4)
        @ elliptical_retarder_matrix(1, 2.0, 5.0, 5.0)
        @ rotation_matrix(np.pi / 4)
    )

    assert CM.ret_mat.shape == (3, 4, 4)
    np.testing.assert_array_equal(CM.ret_mat[0], truth1)
    np.testing.assert_array_equal(CM.ret_mat[1], truth2)
    np.testing.assert_array_equal(CM.ret_mat[2], truth3)


def test_CM(general_CM):
    """
    Given: a CalibrationUnit object
    When: accessing the full Mueller matrix of the entire CU
    Then: the correct matrix is returned
    """
    CM = general_CM
    CM.numsteps = 4
    CM.py = 0
    CM.theta_pol_steps = np.deg2rad(np.array([90, 45, 90, 45]))
    CM.theta_ret_steps = np.deg2rad(np.array([-90, -45, -90, -45]))
    CM.pol_in = np.array([True, False, True, True])
    CM.ret_in = np.array([True, False, True, True])
    CM.dark_in = np.array([False, False, False, False])
    CM.delta_t = np.array([0, 1, 0, 1])
    CM.ret_0_h = np.array([1])
    CM.dret_h = np.array([1])
    CM.ret_0_45 = np.array([1])
    CM.dret_45 = np.array([2])
    CM.ret_0_r = np.array([0])
    CM.dret_r = np.array([1])

    truth1 = (
        rotation_matrix(-np.pi / 2)
        @ elliptical_retarder_matrix(1, 1, 1, 0)
        @ rotation_matrix(np.pi / 2.0)
        @ polarizer_matrix(1, 0)
    )
    truth2 = np.diag(np.ones(4))
    truth3 = (
        rotation_matrix(-np.pi / 2)
        @ elliptical_retarder_matrix(1, 1, 1, 0)
        @ rotation_matrix(np.pi / 2.0)
        @ polarizer_matrix(1, 0)
    )
    truth4 = (
        rotation_matrix(-np.pi / 4)
        @ elliptical_retarder_matrix(1, 2, 3, 1)
        @ rotation_matrix(np.pi / 4.0)
        @ rotation_matrix(-np.pi / 4.0)
        @ polarizer_matrix(1, 0)
        @ rotation_matrix(np.pi / 4)
    )

    assert CM.CM.shape == (4, 4, 4)
    np.testing.assert_allclose(CM.CM[0], truth1)
    np.testing.assert_allclose(CM.CM[1], truth2)
    np.testing.assert_allclose(CM.CM[2], truth3)
    np.testing.assert_allclose(CM.CM[3], truth4)
