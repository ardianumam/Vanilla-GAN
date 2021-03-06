# Copyright 2021 Dakewe Biotech Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import torch
import torch.nn as nn


class DiscriminatorForMNIST(nn.Module):
    r""" It is mainly based on the mobile net network as the backbone network discriminator.

    Args:
        image_size (int): The size of the image. (Default: 28)
        channels (int): The channels of the image. (Default: 1)
    """

    def __init__(self, image_size: int = 28, channels: int = 1) -> None:
        super(DiscriminatorForMNIST, self).__init__()

        self.main = nn.Sequential(
            nn.Linear(channels * image_size * image_size, 512),
            nn.LeakyReLU(negative_slope=0.2, inplace=True),

            nn.Linear(512, 256),
            nn.LeakyReLU(negative_slope=0.2, inplace=True),

            nn.Linear(256, 1),
            nn.Sigmoid()
        )

        # Initializing all neural network weights.
        self._initialize_weights()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = torch.flatten(x, 1)
        out = self.main(out)

        return out

    def _initialize_weights(self) -> None:
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight)
                m.weight.data *= 0.1
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.normal_(m.weight, 1.0, 0.02)
                m.weight.data *= 0.1
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight)
                m.weight.data *= 0.1
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)


def discriminator_for_mnist(image_size: int = 28, channels: int = 1) -> DiscriminatorForMNIST:
    r"""GAN model architecture from the `"One weird trick..." <https://arxiv.org/abs/1406.2661>` paper.
    """
    model = DiscriminatorForMNIST(image_size, channels)

    return model
