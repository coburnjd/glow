from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import torch
from parameterized import parameterized
from tests import utils


class RepeatModule(torch.nn.Module):
    def __init__(self, repeats):
        super(RepeatModule, self).__init__()
        self.repeats = repeats

    def forward(self, tensor):
        tensor = tensor + tensor
        return tensor.repeat(self.repeats)


class TestRepeat(unittest.TestCase):
    @utils.deterministic_expand(
        [
            lambda: ("basic_1", RepeatModule([4]), torch.randn(3)),
            lambda: ("basic_2", RepeatModule([3, 5]), torch.randn(3)),
            lambda: ("basic_3", RepeatModule([4, 3, 5]), torch.tensor(3)),
            lambda: ("2d_1", RepeatModule([4, 2]), torch.randn(5, 1)),
            lambda: ("2d_2", RepeatModule([4, 2, 6]), torch.randn(4, 3)),
            lambda: ("3d_1", RepeatModule([4, 4, 2]), torch.randn(6, 3, 4)),
            lambda: ("3d_2", RepeatModule([3, 1, 1]), torch.randn(3, 3, 4)),
            lambda: ("3d_3", RepeatModule([1, 5, 1]), torch.randn(5, 3, 4)),
            lambda: ("3d_4", RepeatModule([4, 2, 1, 5, 2, 10]), torch.randn(6, 3, 4)),
        ]
    )
    def test_repeat(self, _, module, tensor):
        utils.compare_tracing_methods(module, tensor, fusible_ops={"aten::repeat"})