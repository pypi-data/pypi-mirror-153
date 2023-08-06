import numpy as np
import pytest
from lmfit import Parameters

from dkist_processing_pac.fitter.fitter_parameters import NdParameterArray


@pytest.fixture
def fake_parameters():
    params = Parameters()
    params.add("par_1", value=1.0)
    params.add("par_2", value=100.0)

    return params


@pytest.fixture
def fake_shape():
    return (1, 2, 3)


def test_nd_parameter_array(fake_parameters, fake_shape):
    """
    Given: a single Parameters object
    When: spreading that object across a full, nd, parameter array
    Then: the input object is copied across the full array, and setting and getting work as expected
    """
    par_list = NdParameterArray(fake_parameters, fake_shape)

    assert par_list.fake_shape == fake_shape
    assert len(par_list._all_parameters) == np.prod(fake_shape)

    # Make sure all individual parameters are different objects
    for i in range(np.prod(fake_shape)):
        for j in range(np.prod(fake_shape)):
            if i == j:
                continue
            assert par_list._all_parameters[i] is not par_list._all_parameters[j]

    # Check getter
    assert par_list._all_parameters[0] is par_list[0, 0, 0]
    assert par_list._all_parameters[1] is par_list[0, 0, 1]
    assert par_list._all_parameters[2] is par_list[0, 0, 2]
    assert par_list._all_parameters[3] is par_list[0, 1, 0]
    assert par_list._all_parameters[4] is par_list[0, 1, 1]
    assert par_list._all_parameters[5] is par_list[0, 1, 2]

    # Check setter
    assert par_list[0, 0, 0].valuesdict()["par_1"] == 1.0
    assert par_list[0, 0, 0].valuesdict()["par_2"] == 100.0
    new_pars = Parameters()
    new_pars.add("par_1", value=-10.0)
    new_pars.add("par_2", value=2000.0)
    par_list[0, 0, 0] = new_pars

    assert par_list[0, 0, 0].valuesdict()["par_1"] == -10.0
    assert par_list[0, 0, 0].valuesdict()["par_2"] == 2000.0

    # Check in-place-idness
    # This test is here to explicitly state how these objects act during fitting
    init_par = par_list[0, 1, 2]
    init_par["par_1"].set(value=20.0)
    assert par_list[0, 1, 2].valuesdict()["par_1"] == 20.0
