from __future__ import annotations
from typing import Tuple
import torch
from .handler import ModelHandler, TorchModelHandler

# AUTHORSHIP
__version__ = "0.0.1"
__author__ = "Mirko Polato"
__copyright__ = "Copyright 2022, gossipy"
__license__ = "MIT"
__maintainer__ = "Mirko Polato, PhD"
__email__ = "mak1788@gmail.com"
__status__ = "Development"
#

__all__ = [
    "RandomAttackMixin",
    "SameValueAttackMixin",
    "GradientScalingAttackMixin",
    "BackGradientAttackMixin"
]


class RandomAttackMixin(TorchModelHandler):
    def __init__(self, noise: float):
        self.noise = noise

    def _update(self, data: Tuple[torch.Tensor, torch.Tensor]) -> None:
        with torch.no_grad():
            for param in self.model.parameters():
                param.add_(torch.randn(param.size()) * self.noise)


class SameValueAttackMixin(ModelHandler):
    def _update(self, data: Tuple[torch.Tensor, torch.Tensor]) -> None:
        pass


class GradientScalingAttackMixin(TorchModelHandler):
    def __init__(self, scale: float):
        self.scale = min(scale, 1.0)

    def _update(self, data: Tuple[torch.Tensor, torch.Tensor]) -> None:
        x, y = data
        self.model.train()
        y_pred = self.model(x)
        loss = self.criterion(y_pred, y)
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.model.parameters():
            param.grad *= self.scale
        self.optimizer.step()
        self.n_updates += 1


class BackGradientAttackMixin(GradientScalingAttackMixin):
    def __init__(self):
        super(BackGradientAttackMixin, self).__init__(-1)