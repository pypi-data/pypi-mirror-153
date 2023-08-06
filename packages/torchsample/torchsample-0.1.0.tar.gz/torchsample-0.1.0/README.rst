.. image:: https://raw.githubusercontent.com/BrianPugh/torchsample/main/assets/banner-white-bg-512w.png

|GHA tests| |Codecov report| |readthedocs|

.. inclusion-marker-do-not-remove

Lightweight pytorch functions for neural network featuremap sampling.

**WARNING: API is not yet stable. API subject to change!**

Introduction
------------
Sampling neural network featuremaps at explicit coordinates has become more and more common with popular
developments like:

* `Learning Continuous Image Representation with Local Implicit Image Function`_
* `NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis`_
* `PointRend: Image Segmentation as Rendering`_

.. _Learning Continuous Image Representation with Local Implicit Image Function: https://arxiv.org/pdf/2012.09161.pdf
.. _NeRF\: Representing Scenes as Neural Radiance Fields for View Synthesis: https://arxiv.org/pdf/2003.08934.pdf
.. _PointRend\: Image Segmentation as Rendering: https://arxiv.org/pdf/1912.08193.pdf

PyTorch provides the tools necessary that to sample coordinates, but they result in a large amount of error-prone code.
TorchSample intends to make it simple so you can focus on other parts of the model.

.. inclusion-marker-remove

Usage
-----

Installation
^^^^^^^^^^^^
Requires python ``>=3.8`` Install ``torchsample`` via pip:

.. code-block:: bash

  pip install torchsample

Or, if you want to install the nightly version:

.. code-block:: bash

  pip install git+https://github.com/BrianPugh/torchsample.git@main


Training
^^^^^^^^
A common scenario is to randomly sample points from a featmap and
from the ground truth.

.. code-block:: python

  import torchsample as ts

  b, c, h, w = batch["image"].shape
  coords = ts.coord.rand(b, 4096, 2)  # (b, 4096, 2) where the last dim is (x, y)

  featmap = feature_extractor(batch["image"])  # (b, feat, h, w)
  sampled = ts.sample(coords, featmap)  # (b, 4096, feat)
  gt_sample = ts.sample(coords, batch["gt"])


Inference
^^^^^^^^^
During inference, a comprehensive query of the network to form a complete
image is common.

.. code-block:: python

  import torch
  import torchsample as ts

  b, c, h, w = batch["image"].shape
  coords = ts.coord.full_like(batch["image"])
  featmap = encoder(batch["image"])  # (b, feat, h, w)
  feat_sampled = ts.sample(coords, featmap)  # (b, h, w, c)
  output = model(featmap)  # (b, h, w, pred)
  output = output.permute(0, 3, 1, 2)


Positional Encoding
^^^^^^^^^^^^^^^^^^^
Common positional encoding schemes are available.

.. code-block:: python

  import torchsample as ts

  coords = ts.coord.rand(b, 4096, 2)
  pos_enc = ts.encoding.gamma(coords)


A common task it concatenating the positional encoding to
sampled values. You can do this by passing a callable into
``ts.sample``:

.. code-block:: python

  import torchsample as ts

  encoder = ts.encoding.Gamma()
  sampled = ts.sample(coords, featmap, encoder=encoder)


Models
^^^^^^
``torchsample`` has some common builtin models:

.. code-block:: python

  import torchsample as ts

  # Properly handles (..., feat) tensors.
  model = ts.models.MLP(256, 256, 512, 512, 1024, 1024, 1)


Design Decisions
----------------

* ``align_corners=False`` by default (same as Pytorch).
  You should probably not touch it; `explanation here`_.
* Everything is in normalized coordinates ``[-1, 1]`` by default.
* Coordinates are always in order ``(x, y, ...)``.
* Whenever a size is given, it will be in ``(w, h)`` order;
  i.e. matches coordinate order. It makes implementation simpler
  and a consistent rule helps prevent bugs.
* When ``coords`` is a function argument, it comes first.
* Simple wrapper functions (like ``ts.coord.rand``) are
  provided to make the intentions of calling code more clear.
* Try and mimic native ``pytorch`` and ``torchvision`` interfaces as
  much as possible.
* Try and make the common-usecase as simple and intuitive as possible.



.. |GHA tests| image:: https://github.com/BrianPugh/torchsample/workflows/tests/badge.svg
   :target: https://github.com/BrianPugh/torchsample/actions?query=workflow%3Atests
   :alt: GHA Status
.. |Codecov report| image:: https://codecov.io/github/BrianPugh/torchsample/coverage.svg?branch=main
   :target: https://codecov.io/github/BrianPugh/torchsample?branch=main
   :alt: Coverage
.. |readthedocs| image:: https://readthedocs.org/projects/torchsample/badge/?version=latest
        :target: https://torchsample.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. _explanation here: docs/align_corners.rst
