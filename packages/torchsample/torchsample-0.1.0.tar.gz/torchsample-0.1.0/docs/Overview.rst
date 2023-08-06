Overview
========

Using coordinates in pytorch is a mismash between normalized
coordinates, unnormalized coordinates, matrix indices, calls to
``meshgrid`` and ``grid_sample``, and permuting/reshaping tensors.
TorchSample aims to make it very simple to generate coordinates, and to
sample a neural network with them.

For example, if we wanted to generate all the coordinates for a 2D image, and
use them to query the image, we would have to perform the following:

.. code-block:: python

   import torch
   import torch.nn.functional as F

   image = torch.rand(1, 3, 480, 640)
   unnormalized_coords_x, unnormalized_coords_y = torch.meshgrid(
       (torch.arange(image.shape[-1]), torch.arange(image.shape[-2])),
       indexing="xy",
   )  # These are each shape (480, 640)
   # This is for align_corners=False
   normalized_coords_x = (unnormalized_coords_x * 2 + 1) / image.shape[-1] - 1
   normalized_coords_y = (unnormalized_coords_y * 2 + 1) / image.shape[-2] - 1
   normalized_coords = torch.stack((normalized_coords_x, normalized_coords_y), -1)
   normalized_coords = normalized_coords[None]  # Add a singleton batch dimension

   sampled = F.grid_sample(
       image, normalized_coords, mode="nearest", align_corners=False
   )  # (1, 3, 480, 640)

   assert (sampled == image).all()

That's quite a lot of work! During all of this, it would be very easy to accidentally:

1. Swap ``(x, y)`` for ``(row, col)`` during mesh creation.
2. Normalize the coordinates improperly.
3. Stack the coordinates in the wrong order.

Conversely, lets see how this would look using TorchSample:

.. code-block:: python

   import torch
   import torchsample as ts

   image = torch.rand(1, 3, 480, 640)
   coords = ts.coord.full_like(image)
   sampled = ts.sample(coords, image, mode="nearest", feat_last=False)
   assert (sampled == image).all()

Using TorchSample, the code is much more terse, readable, and less likely to contain a bug.
This allows the developer to instead focus on their actual network architecture rather than getting caught up in the coordinate/sampling machinery.
