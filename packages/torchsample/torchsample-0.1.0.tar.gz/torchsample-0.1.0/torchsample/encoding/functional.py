import torch

from torchsample import default

from ..coord import unnormalize


def identity(coords):
    """Return ``coords`` unmodified."""
    return coords


def gamma(coords, order=10):
    """Positional encoding via sin and cos.

    From:
        NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis

    Parameters
    ----------
    coords : torch.Tensor
        ``(..., dim)`` Coordinates to convert to positional encoding.
        In range ``[-1, 1]``.
    order : int
        Number

    Returns
    -------
    torch.Tensor
        ``(..., 2*dim*order)``
    """
    output = []
    for o in range(order):
        freq = (2**o) * torch.pi
        cos = torch.cos(freq * coords)
        sin = torch.sin(freq * coords)
        output.append(cos)
        output.append(sin)

    output = torch.cat(output, dim=-1)

    return output


def nearest_pixel(coords, size, align_corners=default.align_corners):
    """Encode normalized coords and relative offset to nearest neighbor.

    Note: offsets are multiplied by 2, so that their range is ``[-1, 1]``
    instead of ``[-0.5, 0.5]``

    From:
        High Quality Segmentation for Ultra High-resolution Images

    Example
    -------
    .. code-block:: python

        import torch
        import torchsample as ts

        target = torch.rand(1, 3, 480, 640)
        featmap = torch.rand(1, 256, 15, 20)
        coords = ts.coord.randint(1, 4096, (640, 480))
        pos_enc = ts.encoding.nearest_pixel(coords, (20, 15))

    Parameters
    ----------
    coords : torch.Tensor
        ``(..., dim)`` Coordinates to convert to positional encoding.
        In range ``[-1, 1]``.
    size : tuple
        Size of field to generate pixel-center offsets for. i.e. ``(x, y, ...)``.

    Returns
    -------
    torch.Tensor
        ``(..., 2*dim)`` Normalized coordinates and nearest-pixel relative offset.
    """
    unnorm_coords = unnormalize(coords, size, align_corners)
    # 2x to scale the range from [-0.5, 0.5] to [-1, 1]
    # Note: torch rounds 0.5 DOWN
    unnorm_offset = 2 * (torch.round(unnorm_coords) - unnorm_coords)
    output = torch.cat((coords, unnorm_offset), dim=-1)
    return output
