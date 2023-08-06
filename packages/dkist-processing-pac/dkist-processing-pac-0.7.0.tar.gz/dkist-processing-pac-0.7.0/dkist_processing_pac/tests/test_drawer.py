import datetime

import numpy as np
import pytest
from astropy.io import fits as pyfits
from dkist_header_validator import spec122_validator

from dkist_processing_pac.input_data.drawer import Drawer
from dkist_processing_pac.tests.conftest import CalibrationSequenceStepDataset
from dkist_processing_pac.tests.conftest import InstAccess


@pytest.fixture(scope="session")
def cs_with_low_flux():
    pol_status = [
        "clear",
        "Sapphire Polarizer",
        "clear",
    ]
    pol_theta = [0.0, 60.0, 0.0]
    ret_status = ["clear", "clear", "clear"]
    ret_theta = [0.0, 0.0, 0.0]
    dark_status = [
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
    ]
    num_steps = len(pol_theta)
    start_time = None
    out_dict = dict()
    for n in range(num_steps):
        ds = CalibrationSequenceStepDataset(
            array_shape=(1, 2, 2),
            time_delta=2.0,
            pol_status=pol_status[n],
            pol_theta=pol_theta[n],
            ret_status=ret_status[n],
            ret_theta=ret_theta[n],
            dark_status=dark_status[n],
            start_time=start_time,
        )
        header_list = [
            spec122_validator.validate_and_translate_to_214_l0(
                d.header(), return_type=pyfits.HDUList
            )[0].header
            for d in ds
        ]
        hdu_list = []
        for m in range(ds.num_mod):
            hdu_list.append(
                pyfits.PrimaryHDU(data=np.ones((3, 4, 1)), header=pyfits.Header(header_list.pop(0)))
            )

        out_dict[n] = [InstAccess(h) for h in hdu_list]
        start_time = ds.start_time + datetime.timedelta(seconds=60)

    return out_dict, pol_status, pol_theta, ret_status, ret_theta, dark_status


@pytest.fixture(scope="session")
def cs_with_wrong_shape():
    pol_status = [
        "clear",
        "Sapphire Polarizer",
        "clear",
    ]
    pol_theta = [0.0, 60.0, 0.0]
    ret_status = ["clear", "clear", "clear"]
    ret_theta = [0.0, 0.0, 0.0]
    dark_status = [
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
        "FieldStop (5arcmin)",
    ]
    num_steps = len(pol_theta)
    out_dict = dict()
    start_time = None
    for n in range(num_steps):
        ds = CalibrationSequenceStepDataset(
            array_shape=(1, 2, 2),
            time_delta=2.0,
            pol_status=pol_status[n],
            pol_theta=pol_theta[n],
            ret_status=ret_status[n],
            ret_theta=ret_theta[n],
            dark_status=dark_status[n],
            start_time=start_time,
        )
        header_list = [
            spec122_validator.validate_and_translate_to_214_l0(
                d.header(), return_type=pyfits.HDUList
            )[0].header
            for d in ds
        ]
        hdu_list = []
        for m in range(ds.num_mod):
            hdu_list.append(
                pyfits.PrimaryHDU(data=np.ones((3, 4)), header=pyfits.Header(header_list.pop(0)))
            )

        out_dict[n] = [InstAccess(h) for h in hdu_list]
        start_time = ds.start_time + datetime.timedelta(seconds=60)

    return out_dict, pol_status, pol_theta, ret_status, ret_theta, dark_status


def test_dkistdc_drawer(general_cs):
    """
    Given: a dictionary of FitsAccess objects corresponding to a set of reduced polcal data
    When: initializing a Drawer with that dictionary
    Then: the Drawer is populated correctly and behaves as expected
    """
    cs_step_obj_dict = general_cs[0]
    D = Drawer(cs_step_obj_dict, remove_I_trend=False)
    assert D.nummod == 3
    assert D.numsteps == 7 - 2
    np.testing.assert_array_equal(D.pol_in, [False, True, True, True, False])
    np.testing.assert_array_equal(D.theta_pol_steps, [-999, 60.0, 0.0, 120.0, -999])
    np.testing.assert_array_equal(D.ret_in, [False, False, True, False, False])
    np.testing.assert_array_equal(D.theta_ret_steps, [-999, -999, 45.0, -999, -999])
    np.testing.assert_array_equal(D.dark_in, [False, False, False, False, False])
    assert D.shape == (3, 4, 1)
    cc = np.ones((3, 5)) * np.arange(1, 6)[None, :] + 100 * np.arange(3)[:, None]
    for i in range(np.prod(D.shape)):
        D_cc = D[np.unravel_index(i, D.shape)]
        assert type(D_cc) is np.ndarray
        assert D_cc.dtype == np.float64
        np.testing.assert_array_equal(D_cc, cc)

    # Test slicing errors
    with pytest.raises(IndexError):
        I = D[1, 0]
    with pytest.raises(IndexError):
        I = D[0]
    with pytest.raises(IndexError):
        I = D[0, 1.1, 0]
    with pytest.raises(IndexError):
        I = D[0, :, 0]

    # Test uncertainty
    assert D.RN == 0.0  # TODO: Update this test when RN is updated in the actual Drawer module

    I = D[0, 0, 0]
    u = D.get_uncertainty(I)
    np.testing.assert_array_equal(u, np.sqrt(np.abs(I) + D.RN**2))


def test_dkistdc_drawer_with_darks(general_cs):
    """
    Given: a dictionary of FitsAccess objects corresponding to a set of reduced polcal data
    When: initializing a Drawer with that dictionary and NOT ignoring darks
    Then: the Drawer is populated correctly and behaves as expected
    """
    cs_step_obj_dict = general_cs[0]
    D = Drawer(cs_step_obj_dict, skip_darks=False, remove_I_trend=False)
    assert D.nummod == 3
    assert D.numsteps == 7
    np.testing.assert_array_equal(D.pol_in, [False, False, True, True, True, False, False])
    np.testing.assert_array_equal(D.theta_pol_steps, [-999, -999, 60.0, 0.0, 120.0, -999, -999])
    np.testing.assert_array_equal(D.ret_in, [False, False, False, True, False, False, False])
    np.testing.assert_array_equal(D.theta_ret_steps, [-999, -999, -999, 45.0, -999, -999, -999])
    np.testing.assert_array_equal(D.dark_in, [True, False, False, False, False, False, True])
    assert D.shape == (3, 4, 1)
    cc = np.ones((3, 7)) * np.arange(7)[None, :] + 100 * np.arange(3)[:, None]
    for i in range(np.prod(D.shape)):
        np.testing.assert_array_equal(D[np.unravel_index(i, D.shape)], cc)


def test_dkistdc_drawer_I_trend(general_cs):
    """
    Given: a dictionary of FitsAccess objects corresponding to a set of reduced polcal data
    When: initializing a Drawer with that dictionary and fitting the trend in I_sys
    Then: the I_sys trend is fit correctly
    """
    cs_step_obj_dict = general_cs[0]
    D = Drawer(cs_step_obj_dict, remove_I_trend=True)
    assert D.shape == (3, 4, 1)
    cc = np.ones((3, 5)) * np.arange(1, 6)[None, :] + 100 * np.arange(3)[:, None]
    cc /= np.arange(1, 6) * 0.00970874 + 0.97087379
    for i in range(np.prod(D.shape)):
        np.testing.assert_allclose(D[np.unravel_index(i, D.shape)], cc)


def test_dkistdc_drawer_low_flux(cs_with_low_flux):
    """
    Given: a dictionary of FitsAccess objects corresponding to a set of reduced polcal data with low flux
    When: trying to initialize a Drawer with that dictionary
    Then: an error is raised
    """
    with pytest.raises(ValueError):
        D = Drawer(cs_with_low_flux[0], remove_I_trend=True)


def test_dkistdc_drawer_bad_shape(cs_with_wrong_shape):
    """
    Given: a dictionary of FitsAccess objects corresponding to a set of reduced polcal data with inconsistent shapes
    When: trying to initialize a Drawer with that dictionary
    Then: an error is raised
    """
    with pytest.raises(ValueError):
        D = Drawer(cs_with_wrong_shape[0])
