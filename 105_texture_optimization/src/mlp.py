import torch
import torch.nn as nn
from .positional_encoding import FourierFeatureTransform

class MLP(nn.Module):
    def __init__(
        self,
        depth,
        width,
        out_dim=3,
        input_dim=3,
        positional_encoding=True,
        sigma=12.0,
        clamp="sigmoid",
    ):
        super(MLP, self).__init__()
        self.clamp = clamp
        layers = []
        if positional_encoding:
            layers.append(FourierFeatureTransform(input_dim, width, sigma))
            layers.append(nn.Linear(width * 2 + input_dim, width))
            layers.append(nn.ReLU())
            layers.append(nn.LayerNorm([width]))
        else:
            layers.append(nn.Linear(input_dim, width))
            layers.append(nn.ReLU())
            layers.append(nn.LayerNorm([width]))
        for i in range(depth):
            layers.append(nn.Linear(width, width))
            layers.append(nn.ReLU())
            layers.append(nn.LayerNorm([width]))
        layers.append(nn.Linear(width, out_dim))

        self.netowrk = nn.ModuleList(layers)

    def forward(self, x):
        for layer in self.netowrk:
            x = layer(x)
        if self.clamp == "sigmoid":
            x = torch.sigmoid(x)
        elif self.clamp == "clamp":
            x = torch.clamp(x, 0, 1)
        elif self.clamp == "tanh":
            x = torch.tanh(x) * 0.5 + 0.5
        return x