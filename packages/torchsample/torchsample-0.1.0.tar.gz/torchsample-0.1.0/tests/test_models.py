import torch
import torch.nn.functional as F
import torchtest
from markers import cuda

import torchsample as ts


def test_mlp():
    batch = [
        torch.rand(7, 4096, 10),
        torch.rand(7, 4096, 3),
    ]
    model = ts.models.MLP(10, 100, 100, 3)
    torchtest.assert_vars_change(
        model=model,
        loss_fn=F.l1_loss,
        optim=torch.optim.Adam(model.parameters()),
        batch=batch,
        device="cpu",
    )


def test_mlp_list():
    batch = [
        torch.rand(7, 4096, 10),
        torch.rand(7, 4096, 3),
    ]
    model = ts.models.MLP([10, 100, 100, 3])
    torchtest.assert_vars_change(
        model=model,
        loss_fn=F.l1_loss,
        optim=torch.optim.Adam(model.parameters()),
        batch=batch,
        device="cpu",
    )


@cuda
def test_mlp_cuda():
    batch = [
        torch.rand(7, 4096, 10),
        torch.rand(7, 4096, 3),
    ]
    model = ts.models.MLP([10, 100, 100, 3])
    torchtest.assert_vars_change(
        model=model,
        loss_fn=F.l1_loss,
        optim=torch.optim.Adam(model.parameters()),
        batch=batch,
        device="cuda",
    )
