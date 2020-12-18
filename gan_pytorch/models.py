# Copyright 2020 Dakewe Biotech Corporation. All Rights Reserved.
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
from torch.hub import load_state_dict_from_url

__all__ = [
    "Discriminator", "Generator", "discriminator",
    "mnist", "fmnist", "cifar"
]

model_urls = {
    "mnist": "",
    "fashion-mnist": "",
    "cifar": ""
}


class Discriminator(nn.Module):
    r""" An Discriminator model.

    `Generative Adversarial Networks model architecture from the One weird trick...
    <https://arxiv.org/abs/1406.2661>`_ paper.
    """

    def __init__(self, image_size: int = 28, channels: int = 1):
        """
        Args:
            image_size (int): The size of the image. (Default: 28).
            channels (int): The channels of the image. (Default: 1).
        """
        super(Discriminator, self).__init__()

        self.main = nn.Sequential(
            nn.Linear(channels * image_size * image_size, 256),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Linear(256, 256),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        r""" Defines the computation performed at every call.

        Args:
          input (tensor): input tensor into the calculation.

        Returns:
          A four-dimensional vector (NCHW).
        """
        input = torch.flatten(input, 1)
        out = self.main(input)
        return out


class Generator(nn.Module):
    r""" An Generator model.

    `Generative Adversarial Networks model architecture from the One weird trick...
    <https://arxiv.org/abs/1406.2661>`_ paper.
    """

    def __init__(self, image_size: int = 28, channels: int = 1):
        """
        Args:
            image_size (int): The size of the image. (Default: 28).
            channels (int): The channels of the image. (Default: 1).
        """
        super(Generator, self).__init__()
        self.image_size = image_size
        self.channels = channels

        self.main = nn.Sequential(
            nn.Linear(100, 256),
            nn.ReLU(inplace=True),

            nn.Linear(256, 256),
            nn.ReLU(inplace=True),

            nn.Linear(256, channels * image_size * image_size),
            nn.Tanh()
        )

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        r"""Defines the computation performed at every call.

        Args:
          input (tensor): input tensor into the calculation.

        Returns:
          A four-dimensional vector (NCHW).
        """
        out = self.main(input)
        out = out.reshape(out.size(0), self.channels, self.image_size, self.image_size)
        return out


def discriminator(**kwargs) -> Discriminator:
    r"""GAN model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1406.2661>`_ paper.
    """
    model = Discriminator(**kwargs)
    return model


def mnist(pretrained: bool = False, progress: bool = True, **kwargs) -> Generator:
    r"""GAN model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1406.2661>`_ paper.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    model = Generator(**kwargs)
    if pretrained:
        state_dict = load_state_dict_from_url(model_urls["mnist"], progress=progress)
        model.load_state_dict(state_dict)
    return model


def fmnist(pretrained: bool = False, progress: bool = True, **kwargs) -> Generator:
    r"""GAN model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1406.2661>`_ paper.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    model = Generator(**kwargs)
    if pretrained:
        state_dict = load_state_dict_from_url(model_urls["fashion-mnist"], progress=progress)
        model.load_state_dict(state_dict)
    return model


def cifar(pretrained: bool = False, progress: bool = True, **kwargs) -> Generator:
    r"""GAN model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1406.2661>`_ paper.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    model = Generator(**kwargs)
    if pretrained:
        state_dict = load_state_dict_from_url(model_urls["cifar"], progress=progress)
        model.load_state_dict(state_dict)
    return model