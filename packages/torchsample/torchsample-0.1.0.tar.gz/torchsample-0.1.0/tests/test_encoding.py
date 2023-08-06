from functools import partial

import torch
from markers import cuda

import torchsample as ts

allclose = partial(torch.allclose, atol=1e-6)


def test_gamma():
    """Only exercises code; doesn't assert correct results."""
    coords = torch.rand(3, 4, 2)
    actual = ts.encoding.gamma(coords)
    assert actual.shape == (3, 4, 40)


def test_nearest_pixel_pixel_perfect():
    """Test coordinates that are exactly at pixel locations.

    Relative offsets should be 0 at these locations.
    """
    coords = torch.tensor(
        [
            # Top Row
            [-0.8, -2.0 / 3],  # top-left pixel; no offset
            [0.0, -2.0 / 3],  # top-center pixel; no offset
            [0.8, -2.0 / 3],  # top-right pixel; no offset
        ]
    )[None]
    actual = ts.encoding.nearest_pixel(coords, (5, 3))

    assert actual.shape == (1, 3, 2 + 2)

    assert allclose(actual[0, :3, 2:], torch.tensor(0.0))


def test_nearest_pixel_halfway():
    """Test coordinates exactly halfway between pixels, and slightly past halfway."""
    eps = 1e-6
    coords = torch.tensor(
        [
            # Intermediate halfway
            [-0.8 + 0.2, -2.0 / 3],  # halfway to second pixel right
            [-0.8, -1.0 / 3],  # halfway to second pixel down
            # Intermediate halfway
            # Just over halfway
            [-0.8 + 0.2 + eps, -2.0 / 3],  # halfway to second pixel right
            [-0.8, -1.0 / 3 + eps],  # halfway to second pixel down
        ]
    )[None]
    actual = ts.encoding.nearest_pixel(coords, (5, 3))

    assert actual.shape == (1, 4, 2 + 2)

    # Test the norm_coord portion
    assert allclose(coords.float(), actual[..., :2])

    # Intermediate halfway
    # torch.round rounds down, so these will be negative.
    # halfway to second pixel right
    assert allclose(actual[0, 0, 2:], 2.0 * torch.tensor([-0.5, 0.0]))
    # halfway to second pixel down
    assert allclose(actual[0, 1, 2:], 2.0 * torch.tensor([0.0, -0.5]))

    # Just over halfway
    # just over halfway to second pixel right
    assert allclose(actual[0, 2, 2:], 2.0 * torch.tensor([0.5, 0.0]))
    # just over halfway to second pixel down
    assert allclose(actual[0, 3, 2:], 2.0 * torch.tensor([0.0, 0.5]))


@cuda
def test_nearest_pixel_cuda():
    coords = torch.rand(3, 4, 2, device="cuda")
    actual = ts.encoding.nearest_pixel(coords, (640, 480))
    assert actual.device.type == "cuda"


@cuda
def test_identity_cuda():
    coords = torch.rand(3, 4, 2, device="cuda")
    actual = ts.encoding.identity(coords)
    assert actual.device.type == "cuda"


@cuda
def test_gamma_cuda():
    coords = torch.rand(3, 4, 2, device="cuda")
    actual = ts.encoding.gamma(coords)
    assert actual.device.type == "cuda"
