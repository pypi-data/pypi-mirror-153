import torch
from markers import cuda
from torch.testing import assert_close

import torchsample as ts


def test_unsqueeze_at():
    unsqueeze_at = ts._sample._unsqueeze_at
    tensor = torch.rand(10, 3, 480, 640)

    assert unsqueeze_at(tensor, 0, 0).shape == (10, 3, 480, 640)
    assert unsqueeze_at(tensor, 0, 1).shape == (1, 10, 3, 480, 640)
    assert unsqueeze_at(tensor, 0, 2).shape == (1, 1, 10, 3, 480, 640)

    assert unsqueeze_at(tensor, 2, 0).shape == (10, 3, 480, 640)
    assert unsqueeze_at(tensor, 2, 1).shape == (10, 3, 1, 480, 640)
    assert unsqueeze_at(tensor, 2, 2).shape == (10, 3, 1, 1, 480, 640)


def test_squeeze_at():
    squeeze_at = ts._sample._squeeze_at
    tensor = torch.rand(10, 3, 1, 1, 480, 640)

    assert squeeze_at(tensor, 0, 0).shape == (10, 3, 1, 1, 480, 640)
    assert squeeze_at(tensor, 2, 1).shape == (10, 3, 1, 480, 640)
    assert squeeze_at(tensor, 2, 2).shape == (10, 3, 480, 640)


def test_sample2d_coords_shape3():
    coords = torch.tensor(
        [
            # Top Row
            [-1.0, -1.0],
            [0.0, -1.0],
            [1.0, -1.0],
            # Bottom Row
            [-1.0, 1.0],
            [0.0, 1.0],
            [1.0, 1.0],
            # Trying out small interpolations.
            # Any value below -0.5 shouldn't change value.
            [-0.9, -1],
            [-0.6, -1],
            [-0.5, -1],
            # Coordinates that are a little less nice
            [-0.5 + 0.25, -0.5],  # 1/4 pixel towards (1x, 0y)
            [-0.5, -0.5 + 0.25],  # 1/4 pixel towards (0x, 1y)
        ]
    )[None]
    n_coords = coords.shape[1]

    featmap = torch.tensor([[10.0, 20.0], [30.0, 40.0]])[None, None]
    featmap = featmap.repeat(1, 5, 1, 1)

    actual = ts.sample2d(coords, featmap, encoder=ts.encoding.identity)
    assert actual.shape == (1, n_coords, 7)

    actual = ts.sample2d(coords, featmap)
    assert actual.shape == (1, n_coords, 5)

    # Top Row
    # [-1, -1]: top-left pixel
    # This in unnormalized coordinates gets mapped to (-0.5, -0.5).
    assert torch.allclose(actual[0, 0], torch.tensor(10.0))
    # [0, -1]: middle between 10 and 20
    assert torch.allclose(actual[0, 1], torch.tensor(15.0))
    # [1, -1]: top-right pixel
    assert torch.allclose(actual[0, 2], torch.tensor(20.0))

    # Bottom Row
    # [-1, 1]: bottom-left pixel
    assert torch.allclose(actual[0, 3], torch.tensor(30.0))
    # [0, 1]: middle between 30 and 40
    assert torch.allclose(actual[0, 4], torch.tensor(35.0))
    # [0, 1]: bottom-right pixel
    assert torch.allclose(actual[0, 5], torch.tensor(40.0))

    # Trying out small interpolations.
    # These shouldn't change value due to border padding.
    assert torch.allclose(actual[0, 6], torch.tensor(10.0))
    assert torch.allclose(actual[0, 7], torch.tensor(10.0))
    assert torch.allclose(actual[0, 8], torch.tensor(10.0))

    # Coordinates that are a little less nice
    assert torch.allclose(actual[0, 9], torch.tensor(12.5))
    assert torch.allclose(actual[0, 10], torch.tensor(15.0))


@cuda
def test_sample2d_coords_shape3_cuda():
    coords = torch.rand(3, 4, 2, device="cuda")
    featmap = torch.rand(3, 10, 480, 640, device="cuda")
    actual = ts.sample2d(coords, featmap)
    assert actual.device.type == "cuda"


def test_sample_unified_2d():
    featmap = torch.rand(10, 3, 192, 256)
    coords = ts.coord.rand(10, 4096)

    sample_out = ts.sample(coords, featmap)
    sample2d_out = ts.sample2d(coords, featmap)
    assert_close(sample_out, sample2d_out)


@cuda
def test_sample_unified_2d_cuda():
    coords = torch.rand(3, 4, 2, device="cuda")
    featmap = torch.rand(3, 10, 480, 640, device="cuda")
    actual = ts.sample(coords, featmap)
    assert actual.device.type == "cuda"


def test_sample3d_coords_shape4():
    # TODO
    pass


def test_sample_unified_3d():
    featmap = torch.rand(10, 3, 5, 192, 256)
    coords = ts.coord.rand(10, 4096, 3)

    sample_out = ts.sample(coords, featmap)
    sample3d_out = ts.sample3d(coords, featmap)
    assert_close(sample_out, sample3d_out)


@cuda
def test_sample_unified_3d_cuda():
    featmap = torch.rand(10, 3, 5, 192, 256, device="cuda")
    coords = ts.coord.rand(10, 4096, 3, device="cuda")
    actual = ts.sample(coords, featmap)
    assert actual.device.type == "cuda"
