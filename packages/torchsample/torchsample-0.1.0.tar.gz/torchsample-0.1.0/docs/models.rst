Models
======
Commonly, sampled features are fed into an MLP-like model.
TorchSample provides classes for common models that are used with coordinate
sampling.

MLP
---
``MLP`` is a multilayer-perceptron that can handle arbitrary dimension input.
The last input dimension is features, and the returned prediction will have
the same shape as the input, except for the feature dimension.

.. code-block:: python

   # A simple network that takes in (x, y) coordinates and predicts RGB.
   model = ts.models.MLP(2, 256, 256, 256, 3)

By default, ``MLP`` uses relu activation, and applies activation between
all layers **except** the output layer.

The activation function can be specified. For example, if we want to
use a sine activation function (see `SIREN`_), we could:

.. code-block:: python

   model = ts.models.MLP(2, 256, 256, 256, 3, activation=torch.sin)


.. _SIREN: https://arxiv.org/pdf/2006.09661.pdf
