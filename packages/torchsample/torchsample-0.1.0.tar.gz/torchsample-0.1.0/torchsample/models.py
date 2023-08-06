import torch
import torch.nn.functional as F
from torch import nn


class MLP(nn.Module):
    """Multi Layer Perceptron.

    Applies the MLP to the final dimension of input tensor.
    """

    def __init__(self, *layers, activation=None):
        """Construct an ``MLP`` with specified nodes-per-layer.

        Parameters
        ----------
        layers : list or tuple
            List of how many nodes each layer should have.
            Must be at least 2 long.
        activation : callable
            Activation function applied to all layers except
            the output layer. Defaults to inplace ``relu``.
        """
        super().__init__()
        if len(layers) == 1:
            # Assume user passed in a list
            # instead of unpacking
            layers = layers[0]
        if activation is None:
            activation = nn.ReLU(inplace=True)

        self.activation = activation

        self.layers = nn.ModuleList()
        for in_dim, out_dim in zip(layers[:-1], layers[1:]):
            self.layers.append(nn.Linear(in_dim, out_dim))

    def forward(self, x):
        """Forward pass through linear and activation layers.

        Parameters
        ----------
        x : torch.Tensor
            (..., feat_in) shaped tensor.

        Returns
        -------
        torch.Tensor
            (..., feat_out) shaped tensor.
        """
        shape = x.shape[:-1]
        x = x.reshape(-1, x.shape[-1])
        for layer in self.layers[:-1]:
            x = layer(x)
            x = self.activation(x)
        x = self.layers[-1](x)
        x = x.view(*shape, -1)
        return x
