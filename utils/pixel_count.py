import os
import rasterio
import numpy as np

dir_path = r'/Users/shreyaschopra/Desktop/BushFireDetection/patches/patches/'
PATCHES_PATTERN = '*.tif'

def mask(mask):
    with rasterio.open(mask) as img:
        image = img.read().transpose((1, 2, 0))
        area = np.array(image, dtype=int)
        return area[:, :, 0]


if __name__ == '__main__':
    total_pixels = 0
    for i in os.listdir(path):
        image = os.path.join(path,i)
        pixel = mask(image)
        total_pixels += (pixel > 0).sum()
    print(f'Total number of Fire Pixels: {total_pixels}')