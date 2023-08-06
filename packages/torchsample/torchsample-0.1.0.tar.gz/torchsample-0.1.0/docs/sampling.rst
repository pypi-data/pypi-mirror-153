Sampling
========

After generating coordinates, we can use them to query some image or voxel-like
matrix using ``ts.sample``.


.. code-block:: python

   image = torch.rand(16, 3, 480, 640)
   coords = ts.coord.random(16, 4096, 2)
   samples = ts.sample(coords, image)  # (16, 4096, 3)

Frequently, the sampled features are fed into an MLP-like network.
Because of this, ``sample`` places the feature dimension last by default
so that downstream linear layers can be computed efficiently. The features can be
returned in the standard first dimension-after-batch, if supplied with ``feat_last=False``.


Sampling with positional encoding
---------------------------------
``sample`` can take in an optional function handle ``encoder``.
If provided, the encoder function is applied to the passed in coordinates, and the
encoded coordinates will be concatenated onto the output sampled featuremap.
This can be useful if sampling a featuremap and you want the downstream ``MLP``
to also have the coordinates available as input.

.. code-block:: python

   image = torch.rand(16, 3, 480, 640)
   coords = ts.coord.random(16, 4096, 2)
   samples = ts.sample(coords, image, encoder=ts.encoding.gamma)  # (16, 4096, 43)


See :ref:`Positional Encoding` for available encoders.


.. code-block:: python

   samples = ts.sample(coords, image, feat_last=False)  # (16, 3, 4096)
