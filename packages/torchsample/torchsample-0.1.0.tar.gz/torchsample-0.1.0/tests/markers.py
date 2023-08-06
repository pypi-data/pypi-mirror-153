import pytest
import torch

cuda = pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA GPU required.")
