import os
import torch
import torch.nn.functional as F
from torchvision import transforms
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from unet import UNet
from utils.dataset import BasicDataset
from utils.plot_image import plot

#we are inputing the image along with the model weights through the U-Net architecture
#so that it can calculate the confidences of each pixel across the image
#if confidence > 0.5 : Fire pixel
def detect(net,
                total_img,
                device,
                scale_factor=1,
                out_threshold=0.5):
    net.eval()

    img = torch.from_numpy(BasicDataset.preprocess(total_img, scale_factor))

    img = img.unsqueeze(0)
    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = net(img)

        if net.n_classes > 1:
            probs = F.softmax(output, dim=1)
        else:
            probs = torch.sigmoid(output)

        probs = probs.squeeze(0)

        tf = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize(total_img.size[1]),
                transforms.ToTensor()
            ]
        )

        probs = tf(probs.cpu())
        full_mask = probs.squeeze().cpu().numpy()

    return full_mask > out_threshold

# for automating generation of output file names
def out_files(infiles):
    files = infiles
    output_file_name = []

    for file in files:
        split_file_name = os.path.splitext(file)
        output_file_name.append("{}_OUT{}".format(split_file_name[0], split_file_name[1]))
    return output_file_name

#inputting the  pixels with confidence > 0.5 and converting those pixels to RGB(255,255,255)
def image_mask(result):
    return Image.fromarray((result * 255).astype(np.uint8))


if __name__ == "__main__":
    input_file = r'/Users/shreyaschopra/Desktop/BushFireDetection'
    out_files = out_files(input_file)

    #here we are calling the unet architechture as a class object
    net = UNet(n_channels=3, n_classes=1)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net.to(device=device)

    #after training we have obtained the model weights(unet_semantic.pth)
    net.load_state_dict(torch.load('unet_semantic.pth', map_location=device))

    for i, file_nm in enumerate(os.listdir(input_file)):

        pil_img = Image.open(file_nm)

        pred = detect(net=net,
                           total_img=pil_img,
                           scale_factor=0.5,
                           out_threshold=0.5,
                           device=device)


        out = out_file_name[i]
        result = mask_to_image(pred)
        result.save(out_file_name[i])
        plot(img, result)
