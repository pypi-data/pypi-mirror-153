from typing import Dict

import numpy as np
import pytest
from astropy.time import Time

from dkist_processing_pac.optics.mueller_matrices import mirror_matrix
from dkist_processing_pac.optics.mueller_matrices import rotation_matrix
from dkist_processing_pac.optics.telescope import get_TM_db_location
from dkist_processing_pac.optics.telescope import load_TM_database
from dkist_processing_pac.optics.telescope import Telescope


@pytest.fixture
def general_telescope(general_dresser):
    return Telescope(general_dresser)


def test_dresser_init(general_dresser):
    """
    Given: a Dresser
    When: initializing a Telescope with the Dresser
    Then: the correct geometry and properties are loaded
    """
    TM = Telescope(general_dresser)
    assert type(TM.elevation) is np.ndarray
    assert type(TM.azimuth) is np.ndarray
    assert type(TM.table_angle) is np.ndarray

    np.testing.assert_array_equal(TM.elevation, np.deg2rad(general_dresser.elevation))
    np.testing.assert_array_equal(TM.azimuth, np.deg2rad(general_dresser.azimuth))
    np.testing.assert_array_equal(TM.table_angle, np.deg2rad(general_dresser.table_angle))

    assert TM.numsteps == general_dresser.numsteps
    assert TM.wavelength == general_dresser.wavelength
    assert TM.mean_time == np.mean([general_dresser.mjd_begin, general_dresser.mjd_end])


def test_setting_mirror_params(general_telescope):
    """
    Given: a Telescope
    When: setting the individual mirror attribues
    Then: the attributes are correctly updated
    """
    TM = general_telescope
    TM.x34 = 1.0
    TM.t34 = 2.0
    TM.x56 = 3.0
    TM.t56 = 4.0
    TM.x12 = 5.0
    TM.t12 = 6.0
    assert TM.x34 == 1
    assert TM.t34 == 2
    assert TM.x56 == 3
    assert TM.t56 == 4
    assert TM.x12 == 5
    assert TM.t12 == 6


def test_components(general_telescope):
    """
    Given: a Telescope
    When: accessing the individual mirror and rotation Mueller matrices
    Then: the correct matrices are returned
    """
    TM = general_telescope
    numsteps = TM.numsteps
    TM.x12 = x12 = np.random.random() * (1.25 - 0.95) + 0.95
    TM.x34 = x34 = np.random.random() * (1.25 - 0.95) + 0.95
    TM.x56 = x56 = np.random.random() * (1.25 - 0.95) + 0.95
    TM.t12 = t12 = np.random.random() * (3.75 - 2.53) + 2.53
    TM.t34 = t34 = np.random.random() * (3.75 - 2.53) + 2.53
    TM.t56 = t56 = np.random.random() * (3.75 - 2.53) + 2.53

    np.testing.assert_array_equal(TM.M12, mirror_matrix(x12, t12))
    assert TM.M12.shape == (4, 4)

    np.testing.assert_array_equal(TM.M34, mirror_matrix(x34, t34))
    assert TM.M34.shape == (4, 4)

    np.testing.assert_array_equal(TM.M56, mirror_matrix(x56, t56))
    assert TM.M56.shape == (4, 4)

    np.testing.assert_array_equal(TM.R23, rotation_matrix(-np.pi / 2.0))
    assert TM.R23.shape == (4, 4)

    true_R45 = np.transpose(
        np.dstack((rotation_matrix(-1 * TM.elevation[i]) for i in range(numsteps))), (2, 0, 1)
    )
    np.testing.assert_array_equal(TM.R45, true_R45)
    assert TM.R45.shape == (numsteps, 4, 4)

    true_R67 = np.transpose(
        np.dstack((rotation_matrix(TM.azimuth[i] - TM.table_angle[i]) for i in range(numsteps))),
        (2, 0, 1),
    )
    np.testing.assert_almost_equal(TM.R67, true_R67)
    assert TM.R67.shape == (numsteps, 4, 4)

    np.testing.assert_array_equal(TM.TM, TM.R67 @ TM.M56 @ TM.R45 @ TM.M34 @ TM.R23)
    assert TM.TM.shape == (numsteps, 4, 4)


@pytest.fixture
def tm_parameter_dict() -> Dict[str, float]:
    return {
        "x12": 1.0,
        "t12": 2.0,
        "x34": 3.0,
        "t34": 4.0,
        "x56": 5.0,
        "t56": 6.0,
    }


def test_load_params_from_dict(general_telescope, tm_parameter_dict):
    """
    Given: a Telescope and a dictionary of parameters
    When: loading the parameters into the Telescope
    Then: the internal attributes are correctly updated
    """
    general_telescope.load_pars_from_dict(tm_parameter_dict)
    assert general_telescope.x12 == 1
    assert general_telescope.t12 == 2
    assert general_telescope.x34 == 3
    assert general_telescope.t34 == 4
    assert general_telescope.x56 == 5
    assert general_telescope.t56 == 6


@pytest.fixture
def dummy_fits_access(general_cs):
    out_dict = general_cs[0]
    return out_dict[1][0]


def test_from_fits_access(dummy_fits_access):
    """
    Given: a single FitsAccess object
    When: creating a Telescope object using .from_fits_access
    Then: the correct object is created and all parameters/attributes are loaded correctly
    """
    tm = Telescope.from_fits_access(dummy_fits_access)

    # Test that attributes are correctly set
    assert type(tm.elevation) is np.ndarray
    assert tm.elevation[0] == np.deg2rad(dummy_fits_access.elevation)
    assert type(tm.azimuth) is np.ndarray
    assert tm.azimuth[0] == np.deg2rad(dummy_fits_access.azimuth)
    assert type(tm.elevation) is np.ndarray
    assert tm.table_angle[0] == np.deg2rad(dummy_fits_access.table_angle)
    assert tm.mean_time == Time(dummy_fits_access.time_obs, format="fits").mjd
    assert tm.wavelength == dummy_fits_access.wavelength

    # Test that database values are loaded correctly
    pars = load_TM_database(
        get_TM_db_location(), dummy_fits_access.wavelength, Time(dummy_fits_access.time_obs).mjd
    )
    assert pars["x12"] == tm.x12
    assert pars["t12"] == tm.t12
    assert pars["x34"] == tm.x34
    assert pars["t34"] == tm.t34
    assert pars["x56"] == tm.x56
    assert pars["t56"] == tm.t56


@pytest.fixture(scope="session")
def telescope_db_file(tmp_path_factory):
    file_name = tmp_path_factory.mktemp("telsecope") / "telescope_db.txt"
    with open(file_name, "w") as f:
        f.write(
            str("{:15.6f}" + "{:8.2f}" + "{:7.3f}" * 6 + "\n").format(
                55000, 500, 1, 10, 3, 30, 5, 50
            )
        )
        f.write(
            str("{:15.6f}" + "{:8.2f}" + "{:7.3f}" * 6 + "\n").format(
                56000, 500, 2, 20, 4, 40, 6, 60
            )
        )
        f.write(
            str("{:15.6f}" + "{:8.2f}" + "{:7.3f}" * 6 + "\n").format(
                55000, 600, 1.5, 15, 3.5, 35, 5.5, 55
            )
        )
        f.write(
            str("{:15.6f}" + "{:8.2f}" + "{:7.3f}" * 6 + "\n").format(
                56000, 600, 2.5, 25, 4.5, 45, 6.5, 65
            )
        )

    return str(file_name)


def test_load_db_exact_match(telescope_db_file):
    """
    Given: a telescope database file
    When: loading parameters based on an exact wavelength and time
    Then: the correct values are returned
    """
    wavelength = 500.0
    mean_time = 55000
    tm_pars = load_TM_database(telescope_db_file, wavelength=wavelength, mean_time=mean_time)
    assert tm_pars["x12"] == 1
    assert tm_pars["t12"] == 10
    assert tm_pars["x34"] == 3
    assert tm_pars["t34"] == 30
    assert tm_pars["x56"] == 5
    assert tm_pars["t56"] == 50


# This is for all the remaining tests:
"""
Given: a telescope database file
When: loading parameters with a certain method and a (wavelength, time) that aren't on the exact grid
Then: correct values are returned
"""


def test_load_db_wave_linear_interp(telescope_db_file):
    wavelength = 550
    mean_time = 55000
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="linear"
    )
    assert tm_pars["x12"] == 1.25
    assert tm_pars["t12"] == 12.5
    assert tm_pars["x34"] == 3.25
    assert tm_pars["t34"] == 32.5
    assert tm_pars["x56"] == 5.25
    assert tm_pars["t56"] == 52.5


def test_load_db_time_linear_interp(telescope_db_file):
    wavelength = 500.0
    mean_time = 55500
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="linear"
    )
    assert tm_pars["x12"] == 1.5
    assert tm_pars["t12"] == 15
    assert tm_pars["x34"] == 3.5
    assert tm_pars["t34"] == 35
    assert tm_pars["x56"] == 5.5
    assert tm_pars["t56"] == 55


def test_load_db_both_linear_interp(telescope_db_file):
    mean_time = 55500
    wavelength = 550
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="linear"
    )
    assert tm_pars["x12"] == 1.75
    assert tm_pars["t12"] == 17.5
    assert tm_pars["x34"] == 3.75
    assert tm_pars["t34"] == 37.5
    assert tm_pars["x56"] == 5.75
    assert tm_pars["t56"] == 57.5


def test_load_db_wave_nearest_interp(telescope_db_file):
    wavelength = 500.0
    mean_time = 55000
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="nearest"
    )
    assert tm_pars["x12"] == 1
    assert tm_pars["t12"] == 10
    assert tm_pars["x34"] == 3
    assert tm_pars["t34"] == 30
    assert tm_pars["x56"] == 5
    assert tm_pars["t56"] == 50


def test_load_db_time_nearest_interp(telescope_db_file):
    wavelength = 500.0
    mean_time = 55501
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="nearest"
    )
    assert tm_pars["x12"] == 2
    assert tm_pars["t12"] == 20
    assert tm_pars["x34"] == 4
    assert tm_pars["t34"] == 40
    assert tm_pars["x56"] == 6
    assert tm_pars["t56"] == 60


def test_load_db_both_nearest_interp(telescope_db_file):
    wavelength = 551
    mean_time = 55500
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="nearest"
    )
    assert tm_pars["x12"] == 1.5
    assert tm_pars["t12"] == 15
    assert tm_pars["x34"] == 3.5
    assert tm_pars["t34"] == 35
    assert tm_pars["x56"] == 5.5
    assert tm_pars["t56"] == 55


def test_load_db_wave_out_of_bounds_linear(telescope_db_file):
    mean_time = 55000
    wavelength = 700
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="linear"
    )
    assert tm_pars["x12"] == 1.5
    assert tm_pars["t12"] == 15
    assert tm_pars["x34"] == 3.5
    assert tm_pars["t34"] == 35
    assert tm_pars["x56"] == 5.5
    assert tm_pars["t56"] == 55


def test_load_db_time_out_of_bounds_linear(telescope_db_file):
    wavelength = 500.0
    mean_time = 4
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="linear"
    )
    assert tm_pars["x12"] == 1
    assert tm_pars["t12"] == 10
    assert tm_pars["x34"] == 3
    assert tm_pars["t34"] == 30
    assert tm_pars["x56"] == 5
    assert tm_pars["t56"] == 50


def test_load_db_both_out_of_bounds_linear(telescope_db_file):
    mean_time = 1e7
    wavelength = 2
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="linear"
    )
    assert tm_pars["x12"] == 2
    assert tm_pars["t12"] == 20
    assert tm_pars["x34"] == 4
    assert tm_pars["t34"] == 40
    assert tm_pars["x56"] == 6
    assert tm_pars["t56"] == 60


def test_load_db_wave_out_of_bounds_nearest(telescope_db_file):
    mean_time = 55000
    wavelength = 700
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="nearest"
    )
    assert tm_pars["x12"] == 1.5
    assert tm_pars["t12"] == 15
    assert tm_pars["x34"] == 3.5
    assert tm_pars["t34"] == 35
    assert tm_pars["x56"] == 5.5
    assert tm_pars["t56"] == 55


def test_load_db_time_out_of_bounds_nearest(telescope_db_file):
    wavelength = 500.0
    mean_time = 4
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="nearest"
    )
    assert tm_pars["x12"] == 1
    assert tm_pars["t12"] == 10
    assert tm_pars["x34"] == 3
    assert tm_pars["t34"] == 30
    assert tm_pars["x56"] == 5
    assert tm_pars["t56"] == 50


def test_load_db_both_out_of_bounds_nearest(telescope_db_file):
    wavelength = 2
    mean_time = 1e7
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="nearest"
    )
    assert tm_pars["x12"] == 2
    assert tm_pars["t12"] == 20
    assert tm_pars["x34"] == 4
    assert tm_pars["t34"] == 40
    assert tm_pars["x56"] == 6
    assert tm_pars["t56"] == 60


def test_load_db_wave_out_of_bounds_cubic(telescope_db_file):
    mean_time = 55000
    wavelength = 700
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="cubic"
    )
    assert tm_pars["x12"] == 1.5
    assert tm_pars["t12"] == 15
    assert tm_pars["x34"] == 3.5
    assert tm_pars["t34"] == 35
    assert tm_pars["x56"] == 5.5
    assert tm_pars["t56"] == 55


def test_load_db_time_out_of_bounds_cubic(telescope_db_file):
    wavelength = 500.0
    mean_time = 4
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="cubic"
    )
    assert tm_pars["x12"] == 1
    assert tm_pars["t12"] == 10
    assert tm_pars["x34"] == 3
    assert tm_pars["t34"] == 30
    assert tm_pars["x56"] == 5
    assert tm_pars["t56"] == 50


def test_load_db_both_out_of_bounds_cubic(telescope_db_file):
    wavelength = 2
    mean_time = 1e7
    tm_pars = load_TM_database(
        telescope_db_file, wavelength=wavelength, mean_time=mean_time, method="cubic"
    )
    assert tm_pars["x12"] == 2
    assert tm_pars["t12"] == 20
    assert tm_pars["x34"] == 4
    assert tm_pars["t34"] == 40
    assert tm_pars["x56"] == 6
    assert tm_pars["t56"] == 60
