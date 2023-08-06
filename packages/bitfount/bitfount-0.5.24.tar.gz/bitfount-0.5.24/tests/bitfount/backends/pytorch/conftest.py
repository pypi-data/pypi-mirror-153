"""PyTorch backend test config settings."""
import inspect

from _pytest.monkeypatch import MonkeyPatch
from pytest import fixture

import bitfount.config


@fixture(autouse=True)
def env_fix(monkeypatch: MonkeyPatch) -> None:
    """Fix the environment into a known state for tests."""
    # Overrides the default fixture in tests/conftest.py
    monkeypatch.setenv("BITFOUNT_ENGINE", bitfount.config._PYTORCH_ENGINE)
    monkeypatch.setattr(
        "bitfount.config.BITFOUNT_ENGINE", bitfount.config._PYTORCH_ENGINE
    )


@fixture
def pytorch_bitfount_model_correct_structure() -> str:
    """Example good PytorchBitfountModel."""
    return inspect.cleandoc(
        """
        from torchmetrics.functional import accuracy
        import torch
        from torch import nn as nn
        from torch.nn import functional as F

        from bitfount.backends.pytorch.models.bitfount_model import (
            PyTorchBitfountModel,
        )
        from bitfount.backends.pytorch.models.base_models import (
            PyTorchClassifierMixIn,
        )

        class DummyModel(PyTorchClassifierMixIn, PyTorchBitfountModel):

            def __init__(self, epochs=5, **kwargs):
                super().__init__(epochs=epochs, **kwargs)
                self.learning_rate=0.01

            def create_model(self):
                self.input_size = self.datastructure.input_size

                return nn.Sequential(
                    nn.Linear(self.input_size, 500),
                    nn.ReLU(),
                    nn.Dropout(0.1),
                    nn.Linear(500, self.n_classes),
                )

            def forward(self, x):
                x, sup = x
                x = self._model(x.float())
                return x

            def training_step(self, batch, batch_idx):
                x, y = batch
                return F.cross_entropy(self(x), y)

            def validation_step(self, batch, batch_idx):
                x, y = batch
                preds = self(x)
                loss = F.cross_entropy(preds, y)
                preds = F.softmax(preds, dim=1)
                acc = accuracy(preds, y)

                # Calling self.log will surface up scalars for you in TensorBoard
                # self.log("val_loss", loss, prog_bar=True)
                # self.log("val_acc", acc, prog_bar=True)

                return {
                    "val_loss": loss,
                    "val_acc": acc,
                }

            def test_step(self, batch, batch_idx):
                x, y = batch
                preds = self(x)
                loss = F.cross_entropy(preds, y)
                self.targs.extend(y.tolist())
                self.preds.extend(F.softmax(preds, dim=1).tolist())
                return loss

            def configure_optimizers(self):
                optimizer = torch.optim.AdamW(self.parameters(), lr=self.learning_rate)
                return optimizer
        """
    )


@fixture
def pytorch_bitfount_model_tab_image_data() -> str:
    """Pytorch Model which handles both tabular and image data."""
    return inspect.cleandoc(
        """
        from collections import defaultdict
        from torchmetrics.functional import accuracy
        import torch
        from torch import nn as nn
        from torch.nn import functional as F

        from bitfount.backends.pytorch.models.bitfount_model import (
            PyTorchBitfountModel,
        )
        from bitfount.backends.pytorch.models.base_models import (
            PyTorchClassifierMixIn,
        )

        class DummyModelTabImg(PyTorchClassifierMixIn, PyTorchBitfountModel):

            def __init__(self, epochs=50, **kwargs):
                super().__init__(epochs=epochs, **kwargs)
                self.batch_size = 32
                self.learning_rate = 0.01
                self.num_workers = 0

            def create_model(self):

                class TabImg(nn.Module):

                    def __init__(self):
                        super().__init__()
                        self.conv1 = nn.Sequential(
                            nn.Conv2d(3, 16, (3, 3)),
                            nn.ReLU(),
                            nn.BatchNorm2d(16),
                            nn.MaxPool2d((2, 2)),
                        )
                        self.conv2 = nn.Sequential(
                            nn.Conv2d(16, 32, (3, 3)),
                            nn.ReLU(),
                            nn.BatchNorm2d(32),
                            nn.MaxPool2d((2, 2)),
                        )
                        self.conv3 = nn.Sequential(
                            nn.Conv2d(32, 64, (3, 3)),
                            nn.ReLU(),
                            nn.BatchNorm2d(64),
                            nn.MaxPool2d((2, 2)),
                        )
                        self.ln1 = nn.Linear(64 * 26 * 26, 16)
                        self.relu = nn.ReLU()
                        self.batchnorm = nn.BatchNorm1d(16)
                        self.dropout = nn.Dropout2d(0.5)
                        self.ln2 = nn.Linear(16, 5)

                        self.ln4 = nn.Linear(13, 10) #tabular input size
                        self.ln5 = nn.Linear(10, 10)
                        self.ln6 = nn.Linear(10, 5)
                        self.ln7 = nn.Linear(10, 1)

                    def forward(self, img, tab):
                        img = self.conv1(img)
                        img = self.conv2(img)
                        img = self.conv3(img)
                        img = img.reshape(img.shape[0], -1)
                        img = self.ln1(img)
                        img = self.relu(img)
                        img = self.batchnorm(img)
                        img = self.dropout(img)
                        img = self.ln2(img)
                        img = self.relu(img)

                        tab = self.ln4(tab)
                        tab = self.relu(tab)
                        tab = self.ln5(tab)
                        tab = self.relu(tab)
                        tab = self.ln6(tab)
                        tab = self.relu(tab)

                        x = torch.cat((img, tab), dim=1)
                        x = self.relu(x)

                        return self.ln7(x)

                return TabImg()

            def forward(self, img, tab):
                return self._model(img, tab)

            def training_step(self, batch, batch_idx):
                x, y = batch
                tabular, image, *support = self.split_dataloader_output(x)
                criterion = torch.nn.L1Loss()

                y_pred = torch.flatten(self(image, tabular))

                y_pred = y_pred.double()

                loss = criterion(y_pred, y)

                return loss

            def validation_step(self, batch, batch_idx):
                x, y = batch
                tabular, image, *support = self.split_dataloader_output(x)
                criterion = torch.nn.L1Loss()
                y_pred = torch.flatten(self(image, tabular))
                y_pred = y_pred.double()
                acc = accuracy(y_pred, y)
                val_loss = criterion(y_pred, y)

                return {
                    "validation_loss": val_loss,
                    "validation_accuracy": acc
                }

            def test_step(self, batch, batch_idx):
                x, y = batch
                tabular, image, *support = self.split_dataloader_output(x)
                criterion = torch.nn.L1Loss()
                y_pred = torch.flatten(self(image, tabular))
                y_pred = y_pred.double()
                loss = criterion(y_pred, y)
                return loss

            def split_dataloader_output(self, data):
                tab, images, sup = data
                weights = sup[:, 0].float()
                if sup.shape[1] > 2:
                    category = sup[:, -1].long()
                else:
                    category = None
                return tab.float(), images, weights, category

            def configure_optimizers(self):
                return torch.optim.Adam(self.parameters(), lr=(self.learning_rate))
        """
    )


@fixture
def pytorch_bitfount_segmentation_model() -> str:
    """Pytorch UNet model for segmentation tasks."""
    # Based on https://github.com/milesial/Pytorch-UNet/tree/master/unet
    return inspect.cleandoc(
        """
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import torchmetrics

        from bitfount.backends.pytorch import PyTorchBitfountModel
        from bitfount.backends.pytorch.loss import SoftDiceLoss



        class DummyUnet(PyTorchBitfountModel):
         # Implementation of a UNet model, used for testing purposes.
            def __init__(self, n_channels, n_classes, **kwargs):
                super().__init__(**kwargs)

                self.n_channels = n_channels
                self.n_classes = n_classes
                self.bilinear = True
                self.dice_loss = SoftDiceLoss()
                self.ce_loss = torch.nn.CrossEntropyLoss()


                def double_conv(in_channels, out_channels):
                    return nn.Sequential(
                        nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
                        nn.BatchNorm2d(out_channels),
                        nn.ReLU(inplace=True),
                        nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
                        nn.BatchNorm2d(out_channels),
                        nn.ReLU(inplace=True),
                    )

                def down(in_channels, out_channels):
                    return nn.Sequential(
                        nn.MaxPool2d(2),
                        double_conv(in_channels, out_channels)
                    )

                class up(nn.Module):
                    def __init__(self, in_channels, out_channels, bilinear=True):
                        super().__init__()

                        if bilinear:
                            self.up = nn.Upsample(
                            scale_factor=2, mode='bilinear', align_corners=True
                            )
                        else:
                            self.up = nn.ConvTranpose2d(in_channels // 2, in_channels // 2, # noqa: B950
                                                        kernel_size=2, stride=2)

                        self.conv = double_conv(in_channels, out_channels)

                    def forward(self, x1, x2):
                        x1 = self.up(x1)
                        # [Batch size, Channels, Height, Width]
                        diffY = x2.size()[2] - x1.size()[2]
                        diffX = x2.size()[3] - x1.size()[3]

                        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                                        diffY // 2, diffY - diffY // 2])
                        x = torch.cat([x2, x1], dim=1)
                        return self.conv(x)

                self.inc = double_conv(self.n_channels, 64)
                self.down1 = down(64, 128)
                self.down2 = down(128, 256)
                self.down3 = down(256, 512)
                self.down4 = down(512, 512)
                self.up1 = up(1024, 256)
                self.up2 = up(512, 128)
                self.up3 = up(256, 64)
                self.up4 = up(128, 64)
                self.out = nn.Conv2d(64, self.n_classes, kernel_size=1)
            def create_model(self):
                pass
            def forward(self, x):
                x1 = self.inc(x)
                x2 = self.down1(x1)
                x3 = self.down2(x2)
                x4 = self.down3(x3)
                x5 = self.down4(x4)
                x = self.up1(x5, x4)
                x = self.up2(x, x3)
                x = self.up3(x, x2)
                x = self.up4(x, x1)
                return self.out(x)

            def split_dataloader_output(self, data):
                images, sup = data
                weights = sup[:, 0].float()
                if sup.shape[1] > 2:
                    category = sup[:, -1].long()
                else:
                    category = None
                return images, weights, category

            def training_step(self, batch, batch_nb):
                x, y = batch
                x, *sup = self.split_dataloader_output(x)
                y = y[:, 0].long()
                y_hat = self.forward(x)

                # Cross entropy loss
                ce_loss = F.cross_entropy(y_hat, y) if self.n_classes > 1 else F.binary_cross_entropy_with_logits(y_hat, y)  # noqa: B950

                return {'loss': ce_loss}

            def validation_step(self, batch, batch_nb):
                x, y = batch
                x, *sup = self.split_dataloader_output(x)
                # Get rid of the number of channels dimension and make targets of type `long`
                y = y[:, 0].long()
                y_hat = self.forward(x)
                softmax_y_hat = F.softmax(y_hat, dim=1)

                # Cross entropy loss
                ce_loss = F.cross_entropy(y_hat, y) if self.n_classes > 1 else F.binary_cross_entropy_with_logits(y_hat, y)  # noqa: B950
                # dice loss
                dice_loss = self.dice_loss(softmax_y_hat, y)
                # total loss
                total_loss = (ce_loss + dice_loss) / 2

                # torchmetrics dice score
                dice_pytorch = torchmetrics.functional.dice_score(softmax_y_hat,y)
                # torchmetrics Jaccard index/ IoU (intersection vs union)
                iou = torchmetrics.functional.jaccard_index(y_hat, y, num_classes=3)
                return {
                'ce_loss': ce_loss,
                'dice_loss': dice_loss,
                'loss': total_loss,
                'iou': iou,
                "dice_score": dice_pytorch
                }

            def validation_epoch_end(self, outputs):
                mean_outputs = {}
                for k in outputs[0].keys():
                    mean_outputs[k] = torch.stack([x[k] for x in outputs]).mean()
                # Add the means to the validation stats.
                self.val_stats.append(mean_outputs)

                # Also log out these averaged metrics
                for k, v in mean_outputs.items():
                    self.log(f"avg_{k}", v)

            def test_step(self, batch, batch_nb):
                x, y = batch
                x, *sup = self.split_dataloader_output(x)
                # Get rid of the number of channels dimension and make targets of type `long`
                y = y[:, 0].long()
                y_hat = self.forward(x)
                pred = F.softmax(y_hat, dim=1)
                loss = F.cross_entropy(pred, y)
                self.targs.extend(y.tolist())
                self.preds.extend(pred.tolist())
                return loss

            def configure_optimizers(self):
                return torch.optim.Adam(self.parameters(), lr=1e-4)
        """
    )
