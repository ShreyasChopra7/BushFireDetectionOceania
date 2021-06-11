from tqdm import tqdm
import shutil
import rasterio
import os
from functools import reduce

dir = r'/Users/shreyaschopra/Desktop/BushFireDetection/data/masks'
algo = ['Schroeder', 'Murphy', 'Kumar-Roy']
dir_out = r'/Users/shreyaschopra/Desktop/BushFireDetection/data/masks'

size = (256,256)


def IntersectionMask(dataframes):
    join_end = reduce(lambda x, y: pd.merge(x, y, on='image_name'), df)
    cols = [col for col in join_end.columns if col.startswith('dir')]

    for index, row in tqdm(join_end.iterrows()):

        image_size = size
        if MASKS_FOR_COMPLETE_SCENE:
            mask, _ = get_mask_arr(row[cols[0]])
            image_size = mask.shape
        final_mask = (np.ones(image_size) == 1)

        for cols in cols:
            mask, profile = MaskArray(row[cols])
            final_mask = np.logical_and(final_mask, mask)

        has_fire = final_mask.sum() > 0
        if has_fire:
            write_mask(os.path.join(output_dir, row['image_name'].replace('_RT', '_RT_Intersection')), final_mask,
                       profile)

    # move files from temporary dir to output dir
    if intersect == dir_out:
        file_names = os.listdir(dir_out)
        for name in file_names:
            shutil.move(os.path.join(dir_out, file_name), dir_out)

        shutil.rmtree(dir_out)

def MaskArray(path):
    with rasterio.open(path) as src:
        img = src.read().transpose((1, 2, 0))
        seg = np.array(img, dtype=int)

        return seg[:, :, 0], src.profile

def output_mask(mask_path, mask, profile={}):
    profile.update({'dtype': rasterio.uint8,'count': 1})

    with rasterio.open(mask_path, 'w', **profile) as dst:
        dst.write_band(1, mask.astype(rasterio.uint8))
