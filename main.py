# importing torch libraries

import torch
import torch.nn as nn
import torchvision.transforms.functional as TF


# Defining a Double Convolutional Network

class DConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.conv(x)


# Aliging the Convolutional networks as per Unet Architechure

class UNET(nn.Module):
    def __init__(
            self, in_channels=3, out_channels=1, features=[64, 128, 256, 512],
            # Defining features to extract features - forward feed
    ):
        super(UNET, self).__init__()
        self.ups = nn.ModuleList()
        self.downs = nn.ModuleList()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Down - UNET
        for f in features:
            self.downs.append(DConv(in_channels, f))
            in_channels = f

        # Up - UNET
        for f in reversed(features):  # reversing the feature list for Upsampling
            self.ups.append(
                nn.ConvTranspose2d(
                    f * 2, f, kernel_size=2, stride=2,
                )
            )
            self.ups.append(DConv(f * 2, f))

        self.bottleneck = DConv(features[-1], features[-1] * 2)
        self.final_conv = nn.Conv2d(features[0], out_channels, kernel_size=1)

    def forward(self, x):
        skip_connections = []

        for down in self.downs:
            x = down(x)
            skip_connections.append(x)
            x = self.pool(x)

        x = self.bottleneck(x)
        skip_connections = skip_connections[::-1]

        for idx in range(0, len(self.ups), 2):
            x = self.ups[idx](x)
            skip_connection = skip_connections[idx // 2]

            if x.shape != skip_connection.shape:
                x = TF.resize(x, size=skip_connection.shape[2:])

            concat_skip = torch.cat((skip_connection, x), dim=1)
            x = self.ups[idx + 1](concat_skip)

        return self.final_conv(x)


def test():
    x = torch.randn((3, 1, 161, 161))
    model = UNET(in_channels=1, out_channels=1)
    preds = model(x)
    print(x.shape)
    print(preds.shape)
    assert preds.shape == x.shape


if __name__ == "__main__":
    test()