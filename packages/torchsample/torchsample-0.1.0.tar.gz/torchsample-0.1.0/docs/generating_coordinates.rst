Generating Coordinates
======================

To keep a simple, uniform, consistent API; everything in TorchSample
operates off of normalized coordinates in range ``[-1, 1]``, unless
explicitly stated otherwise.

Similarly, all coordinates are **always** in order ``(x, y, ...)``.
If the shape of a space is given, it is **always** in order ``(x, y, ...)``.
For example, the shape of a 4D tensor is typically expressed as
``(b, c, h, w)``. So, if a function needs the query space shape, the
argument would be ``(w, h)`` since ``w`` is associated with ``x`` and
``h`` is associated with ``y``.


Random Coordinates
------------------
To generate random coordinates, use ``ts.coord.rand``:

.. code-block:: python

   coords = ts.coord.rand(16, 4096, 2, device="cuda")
   assert coords.shape == (16, 4096, 2)

To generate coordinates that **fall exactly on pixels** for a
given resolution, you can use ``ts.coord.randint``. Despite the name, the
returned coordinates are still normalized and in range ``[-1. 1]``.

.. code-block:: python

   image = torch.rand(16, 3, 480, 640)
   coords = ts.coord.randint(16, 4096, (640, 480))

Similar to ``numpy``, TorchSample offers convenience functions ending in ``_like``
that accepts a 4D or 5D tensor so that the caller doesn't have to juggle around shape.

.. code-block:: python

   image = torch.rand(16, 3, 480, 640)
   coords = ts.coord.randint_like(4096, image)  # (16, 4096, 2)


Comprehensive Coordinates
-------------------------
During inference time, its common to want to generate coordinates that
comprehensively query an entire space.

.. code-block:: python

   image = torch.random
   coords = ts.coord.full(1, (640, 480))  # (1, 480, 640, 2)

Or, create comprehensive coordinates that match a given tensor:

.. code-block:: python

   image = torch.rand(16, 3, 480, 640)
   coords = ts.coord.full_like(image)  # (16, 480, 640, 2)


Helpers
-------
To go back-and-forth between normalized and unnormalized coordinates, the
helper functions ``ts.coord.normalize`` and ``ts.coord.unnormalize`` are
available.

.. code-block:: python

   coords = ts.coord.rand(16, 4096, 2)  # range [-1, 1]
   # xrange [0, 639];  yrange [0, 479]
   unnormalized_coords = ts.coord.unnormalize(coords, (640, 480))
   renormalized_coords = ts.coord.normalize(coords, (640, 480))
   assert_close(coords, renormalized_coords)
