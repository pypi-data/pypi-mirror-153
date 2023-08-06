"""Sanity integration tests between various components.
"""

import pytest
import torch

import torchsample as ts


@pytest.fixture
def single_batch():
    return torch.rand(1, 10, 3, 15)


def test_full_sample2d(single_batch):
    expected = single_batch.permute(0, 2, 3, 1)

    coords = ts.coord.full_like(single_batch)
    sampled = ts.sample2d(coords, single_batch)

    assert sampled.shape == (1, 3, 15, 10)

    assert torch.allclose(expected, sampled, atol=1e-6)


def test_full_sample2d_pos(single_batch):
    expected = single_batch.permute(0, 2, 3, 1)
    # Identity encoder just tacks on the normalized coord.
    encoder = ts.encoding.Identity()

    coords = ts.coord.full_like(single_batch)
    sampled = ts.sample2d(coords, single_batch, encoder=encoder)

    assert sampled.shape == (1, 3, 15, 10 + 2)

    assert torch.allclose(expected, sampled[..., :10], atol=1e-6)
    assert torch.allclose(coords, sampled[..., 10:], atol=1e-6)


def test_randint_align_corners_true():
    align_corners = True
    batch = torch.rand(2, 3, 480, 640)
    coords = ts.coord.randint(2, 4096, (640, 480), align_corners=align_corners)
    coords = ts.coord.randint_like(4096, batch, align_corners=align_corners)
    sampled = ts.sample2d(coords, batch, mode="nearest", align_corners=align_corners)

    sampled_flat = sampled.reshape(-1, 3)
    batch_flat = batch.permute(0, 2, 3, 1).reshape(-1, 3)
    assert all([x in batch_flat for x in sampled_flat])


def test_randint_align_corners_false():
    align_corners = False
    batch = torch.rand(2, 3, 480, 640)
    coords = ts.coord.randint(2, 4096, (640, 480), align_corners=align_corners)
    coords = ts.coord.randint_like(4096, batch, align_corners=align_corners)
    sampled = ts.sample2d(coords, batch, mode="nearest", align_corners=align_corners)

    sampled_flat = sampled.reshape(-1, 3)
    batch_flat = batch.permute(0, 2, 3, 1).reshape(-1, 3)
    assert all([x in batch_flat for x in sampled_flat])
