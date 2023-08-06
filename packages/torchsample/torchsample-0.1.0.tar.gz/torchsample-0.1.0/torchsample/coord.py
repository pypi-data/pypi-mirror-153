import torch
import torch.nn.functional as F

from . import default
from ._nobatch import nobatch
from ._sample import sample


def tensor_to_size(tensor):
    """Field size from tensor."""
    return tensor.shape[:1:-1]


def feat_first(tensor):
    """Move the features (last dim) to dim1."""
    return tensor.movedim(-1, 1)


def feat_last(tensor):
    """Move the features (dim1) to last dim."""
    return tensor.movedim(1, -1)


def unnormalize(coord, size, align_corners=default.align_corners, clip=False):
    """Unnormalize normalized coordinates.

    Modified from PyTorch C source:
        https://github.com/pytorch/pytorch/blob/c52290bad18d23d7decd37b581307f8241c0e8c5/aten/src/ATen/native/GridSampler.h#L26

    Parameters
    ----------
    coord : torch.Tensor
        Values in range ``[-1, 1]`` to unnormalize.
    size : int or tuple
        Unnormalized side length in pixels.
        If tuple, order is ``(x, y, ...)`` to match ``coord``.
    align_corners : bool
        if ``True``, the corner pixels of the input and output tensors are
        aligned, and thus preserving the values at those pixels.
    clip : bool
        If ``True``, output will be clipped to range ``[0, size-1]``

    Returns
    -------
    torch.Tensor
        Unnormalized coordinates.
    """
    if coord.numel() == 0:
        return coord

    if isinstance(size, int):
        size = coord.new_tensor(size)
        size = size[(None,) * coord.ndim]
    else:
        # List, Tuple
        size = coord.new_tensor(size)
        size = size[(None,) * (coord.ndim - 1)]

    if align_corners:
        # unnormalize coord from [-1, 1] to [0, size - 1]
        unnorm = ((coord + 1) / 2) * (size - 1)
    else:
        # unnormalize coord from [-1, 1] to [-0.5, size - 0.5]
        unnorm = ((coord + 1) * size - 1) / 2

    if clip:
        unnorm = torch.clip(unnorm, 0, size - 1)

    return unnorm


def normalize(
    coord,
    size,
    align_corners=default.align_corners,
):
    """Normalize unnormalized coordinates.

    Related
    -------
    unnormalize

    Parameters
    ----------
    coord : torch.Tensor
        Values in range ``[0, size-1]`` to normalize.
    size : int or tuple
        Unnormalized side length in pixels.
        If tuple, order is ``(x, y, ...)`` to match ``coord``.
    align_corners : bool
        if ``True``, the corner pixels of the input and output tensors are
        aligned, and thus preserving the values at those pixels.

    Returns
    -------
    torch.Tensor
        Normalized coordinates.
    """
    if coord.numel() == 0:
        return coord

    if isinstance(size, int):
        size = coord.new_tensor(size)
        size = size[(None,) * coord.ndim]
    else:
        # List, Tuple
        size = coord.new_tensor(size)
        size = size[(None,) * (coord.ndim - 1)]

    if align_corners:
        norm = (coord / (size - 1)) * 2 - 1
    else:
        norm = (coord * 2 + 1) / size - 1

    return norm


def rand(batch, n_samples, dims=2, dtype=None, device=None):
    """Generate random coordinates in range ``[-1, 1]``.

    Parameters
    ----------
    batch : int
        Batch size. If ``0``, don't return a batch dimension.
    n_samples : int
        Number of coordinates to generate per exemplar.
    dims : int
        ``2`` for generating ``(x, y)`` coordinates.
        ``3`` for generating ``(x, y, z)`` coordinates.
        Defaults to ``2``.
    dtype : torch.dtype
        The desired data type of returned tensor.
    device : torch.device
        The desired device of returned tensor

    Returns
    -------
        (batch, n_samples, dims) random coordinates in range ``[-1, 1]``.
    """
    if batch == 0:
        return 2 * torch.rand(n_samples, dims, dtype=dtype, device=device) - 1
    else:
        return 2 * torch.rand(batch, n_samples, dims, dtype=dtype, device=device) - 1


def randint(
    batch,
    n_samples,
    size,
    device=None,
    align_corners=default.align_corners,
    replace=False,
):
    """Generate random pixel coordinates in range ``[-1, 1]``.

    Unlike ``rand``, the resulting coordinates will land exactly on pixels.
    Intended for sampling high resolution GT data during data loading.

    Due to numerical precision, it is suggested to use ``mode="nearest"``
    when sampling featuremaps of resolution ``size`` using these coordinates.

    Parameters
    ----------
    batch : int
        Batch size. If ``0``, don't return a batch dimension.
    n_samples : int
    size : tuple
        Size of field to generate pixel coordinates for. i.e. ``(x, y, ...)``.
    device : torch.device
        The desired device of returned tensor
    align_corners : bool
        if ``True``, the corner pixels of the input and output tensors are
        aligned, and thus preserving the values at those pixels.
    replace : bool
        Sample with or without replacement. Defaults to ``False``.

    Returns
    -------
        (batch, n_samples, dims) random coordinates in range ``[-1, 1]``.
    """
    return_nobatch = False
    if batch == 0:
        batch = 1
        return_nobatch = True

    if replace:
        coords = []
        for s in size:
            unnorm = torch.randint(s, size=(batch, n_samples), device=device)
            norm = normalize(unnorm, s, align_corners)
            coords.append(norm)
        coords = torch.stack(coords, dim=-1)
    else:
        unnorm = torch.cartesian_prod(
            *(torch.arange(x) for x in size),
        ).to(device)
        coords = normalize(unnorm, size, align_corners)
        coords = coords[None].repeat(batch, 1, 1)
        n_elements = coords.shape[1]

        batch_select = torch.arange(batch, device=device)[:, None]
        batch_select = batch_select.repeat(1, n_samples)
        rand_coord_indices = torch.stack(
            [
                torch.randperm(n_elements, device=device)[:n_samples]
                for _ in range(batch)
            ],
            dim=0,
        )
        coords = coords[batch_select, rand_coord_indices]

    if return_nobatch:
        return coords[0]
    else:
        return coords


@nobatch
def randint_like(n_samples, tensor, align_corners=default.align_corners, replace=False):
    """Generate random pixel coordinates in range ``[-1, 1]``.

    See ``randint``.

    Parameters
    ----------
    n_samples : int
    tensor : tuple
        Tensor to generate random coordinates for. Coordinates will be
        placed on same device as ``tensor``.
    align_corners : bool
        if ``True``, the corner pixels of the input and output tensors are
        aligned, and thus preserving the values at those pixels.
    replace : bool
        Sample with or without replacement. Defaults to ``True``.

    Returns
    -------
        (batch, n_samples, dims) random coordinates in range ``[-1, 1]``.
    """
    batch = tensor.shape[0]
    size = tensor_to_size(tensor)
    return randint(
        batch,
        n_samples,
        size,
        device=tensor.device,
        align_corners=align_corners,
        replace=replace,
    )


@nobatch
def full(batch, size, device=None, align_corners=default.align_corners):
    """Generate 2D or 3D coordinates to fully n_samples an image.

    Parameters
    ----------
    batch : int
        Batch size. If ``0``, don't return a batch dimension.
    size : tuple
        Size of field to generate pixel coordinates for. i.e. ``(x, y, ...)``.
    device : torch.device
        The desired device of returned tensor
    align_corners : bool
        if ``True``, the corner pixels of the input and output tensors are
        aligned, and thus preserving the values at those pixels.

    Returns
    -------
    coords : torch.Tensor
        ``(n, h, w, 2)`` Normalized coordinates for sampling functions.
    """
    unnormalized = torch.meshgrid(*[torch.arange(x) for x in size], indexing="xy")
    normalized = [
        normalize(*x, align_corners=align_corners) for x in zip(unnormalized, size)
    ]
    normalized = torch.stack(normalized, -1).to(device)
    if batch:
        normalized = normalized[None]
        expand = tuple([1] * len(size))
        normalized = normalized.repeat(batch, 1, *expand)
    return normalized


@nobatch
def full_like(tensor, *args, **kwargs):
    batch = tensor.shape[0]
    size = tensor_to_size(tensor)
    return full(batch, size, *args, device=tensor.device, **kwargs)


def rand_biased(
    batch,
    n_samples,
    pred,
    k=3.0,
    beta=0.75,
    align_corners=default.align_corners,
):
    """Uncertainty-based point sampling.

    Described in training part of section 3.1 of:
        PointRend: Image Segmentation as Rendering

    Parameters
    ----------
    batch : int
        Batch size. If ``0``, don't return a batch dimension.
    n_samples : int
        Number of coordinates to generate per exemplar.
    pred : torch.Tensor
        ``(b, c, h, w)`` or ``(b, c, d, h, w)`` prediction probabilities.
    k : float
        Multiplier for oversampling for biased coordinates.
    beta : float
        Portion of coordinates to be biased towards uncertain regions.
        Lower values of beta are more similar to a uniform random distribution,
        ignoring ``pred``.
    align_corners : bool
        if ``True``, the corner pixels of the input and output tensors are
        aligned, and thus preserving the values at those pixels.

    Returns
    -------
    torch.Tensor
        (b, n_samples, dim) Normalized coordinates.
    """
    if pred.ndim == 4:
        dim = 2
    elif pred.ndim == 5:
        dim = 3
    else:
        raise ValueError(f"Cannot handle pred dimensionality {pred.ndim}.")

    return_nobatch = False
    if batch == 0:
        batch = 1
        return_nobatch = True

    if k < 1:
        raise ValueError('"k" must be >=1')
    if not (0 <= beta <= 1):
        raise ValueError('"beta" must be in range [0, 1]')

    coords = pred.new_empty((batch, n_samples, dim))
    n_biased = int(beta * n_samples)
    n_unbiased = n_samples - n_biased

    if n_biased:
        oversampled_coords = rand(batch, int(k * n_samples), dim, device=coords.device)
        pred_sampled = sample(oversampled_coords, pred)
        certainty = torch.max(pred_sampled, dim=-1).values  # (b, k*n_samples)
        _, indices = torch.sort(certainty, dim=1)
        indices = indices[:, :n_biased]
        coords[:, :n_biased] = oversampled_coords[
            torch.arange(batch)[:, None].expand(-1, n_biased), indices
        ]

    if n_unbiased:
        # This won't happen during testing when ``beta==0``
        coords[:, n_biased:] = rand(batch, n_unbiased, dim, device=coords.device)

    if return_nobatch:
        return coords[0]
    else:
        return coords


def uncertain(
    pred,
    threshold=0.5,
    align_corners=default.align_corners,
):
    """Report all coordinates with uncertain scores.

    Used for inference with models trained with ``rand_biased``.

    .. code-block:: python

        features = feature_extractor(batch["image"])
        ss_pred = decoder(batch["image"])
        index_coords, norm_coords = ts.coord.uncertain(ss_pred)
        features_sampled = ts.sample(norm_coords, features)
        refined = mlp(features_sampled)
        ss_pred_refined = ss_pred.clone()
        ss_pred_refined[index_coords] = ts.feat_first(refined).flatten()

    Parameters
    ----------
    pred : torch.Tensor
        ``(1, c, h, w)`` or ``(1, c, d, h, w)`` prediction probabilities.
        Can NOT handle ``>1`` batch size; would result in ragged
        tensors.
    threshold : float
        Coords with a max probability lower than this threshold will
        have coordinates generated.
    align_corners : bool
        if ``True``, the corner pixels of the input and output tensors are
        aligned, and thus preserving the values at those pixels.


    Returns
    -------
    index_coords : tuple
        Integer pixel coordinates that can be used to directly index
        into ``pred``.
    norm_coords
        Normalized coordinates to be used with ``ts.sample``.
        Does NOT have a batch dimension, as it would end up
        with a ragged tensor.
    """
    size = tensor_to_size(pred)
    certainty = pred.max(1, keepdim=True).values

    # Expand so when indexing we also index into the all the features.
    certainty = certainty.expand(pred.shape)
    # (n_coords, certainty.ndim)
    mask = certainty < threshold
    index_coords = mask.nonzero(as_tuple=True)
    index_coords_no_c = mask[:, 0].nonzero(as_tuple=True)
    # Get rid of the batch index and flip the remaining
    # (..., y, x) to get (x, y, ...)
    pixel_coords = torch.stack(index_coords_no_c[:0:-1], -1)[None]

    norm_coords = normalize(pixel_coords, size, align_corners)

    return index_coords, norm_coords
