import numpy as np

from dkist_processing_pac.optics.mueller_matrices import mirror_matrix
from dkist_processing_pac.optics.mueller_matrices import rotation_matrix

RTOL = 1e-6


def test_rotation():
    """Test that the rotation matrix is correct. Sort of."""
    np.testing.assert_allclose(rotation_matrix(0), np.diag(np.ones(4)), rtol=RTOL)


def test_mirror():
    """Test that the mirror matrix is correct. Sort of."""
    np.testing.assert_allclose(mirror_matrix(1, 0), np.diag(np.ones(4)), rtol=RTOL)
