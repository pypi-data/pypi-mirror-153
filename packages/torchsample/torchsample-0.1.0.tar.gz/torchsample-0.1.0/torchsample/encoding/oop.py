from abc import ABC, abstractmethod

from torch import nn

from .functional import gamma, identity, nearest_pixel


class _OOPWrapper(nn.Module, ABC):
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    @abstractmethod
    def forward(self, coords):
        pass


class Gamma(_OOPWrapper):
    """See ``torchsample.encoding.functional.gamma``."""

    def forward(self, coords):
        return gamma(coords, **self.kwargs)


class Identity(_OOPWrapper):
    """See ``torchsample.encoding.functional.gamma``."""

    def forward(self, coords):
        return identity(coords, **self.kwargs)


class NearestPixel(_OOPWrapper):
    """See ``torchsample.encoding.functional.nearest_pixel``."""

    def forward(self, coords):
        return nearest_pixel(coords, **self.kwargs)
