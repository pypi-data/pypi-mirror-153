"""Tests for the backends/pytorch/metrics.py."""

import numpy as np
import pytest
import torch

from bitfount.backends.pytorch.loss import SoftDiceLoss, soft_dice_loss
from tests.utils.helper import backend_test, unit_test


@backend_test
@unit_test
class TestSoftDiceLoss:
    """Tests the SoftDiceLoss."""

    def test_softdiceloss(self) -> None:
        """Test the SoftDiceLoss."""
        loss_fn = SoftDiceLoss()
        inp = torch.zeros((1, 3, 1, 1), requires_grad=True) + 0.1
        target = torch.zeros((1, 1, 1), dtype=torch.long) + 1
        loss = loss_fn(inp, target)
        loss.backward()
        assert isinstance(loss, torch.Tensor)
        # The value for the second tensor taken from the test for the
        # original implementation.
        assert torch.isclose(loss, torch.tensor(-0.79653674364089))

    def test_softdiceloss_with_weights(self) -> None:
        """Test the SoftDiceLoss with predefined weights."""
        loss_fn = SoftDiceLoss(weight=[0.33, 0.33, 0.33])
        assert loss_fn.weight is not None

    def test_softdiceloss_square_nom_denom(self) -> None:
        """Test the SoftDiceLoss with square_nom and denom."""
        loss_fn = SoftDiceLoss(square_nom=True, square_denom=True)
        inp = torch.zeros((1, 3, 1), requires_grad=True) + 0.1
        target = torch.zeros((1, 1), dtype=torch.long) + 1
        loss = loss_fn(inp, target)
        loss.backward()
        assert isinstance(loss, torch.Tensor)
        assert torch.isclose(loss, torch.tensor(-0.8292231))

    def test_softdiceloss_error_ndim_targets(self) -> None:
        """Test the SoftDiceLoss raises error with targetsndim less than 3."""
        loss_fn = SoftDiceLoss(square_nom=True, square_denom=True)
        inp = torch.zeros((1, 3, 1), requires_grad=True) + 0.1
        target = torch.zeros((1,), dtype=torch.long) + 1
        with pytest.raises(ValueError):
            loss_fn(inp, target)

    def test_softdiceloss_error_ndim_preds(self) -> None:
        """Test the SoftDiceLoss raises error with predictions.ndim less than 3."""
        loss_fn = SoftDiceLoss(square_nom=True, square_denom=True)
        inp = torch.zeros((1, 3), requires_grad=True) + 0.1
        target = torch.zeros((1, 1), dtype=torch.long) + 1
        with pytest.raises(ValueError):
            loss_fn(inp, target)


@backend_test
@unit_test
def test_func_soft_dice_loss() -> None:
    """Tests functional implementation of soft dice loss."""
    inp = np.zeros((1, 3, 1)) + 0.1
    target = np.zeros((1, 1)) + 1
    loss = soft_dice_loss(inp, target)
    assert isinstance(loss, torch.Tensor)
    assert torch.isclose(loss, torch.tensor([-0.7381], dtype=torch.float64))
