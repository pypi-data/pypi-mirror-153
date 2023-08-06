import glob
import os
import pandas as pd
from PIL import Image

def _return_ordered_img_index(img_filepaths):
    ordered_img_idx = []
    for path in img_filepaths:
        order_idx = int(path.split(".")[-2])
        ordered_img_idx.append(order_idx)
    
    return ordered_img_idx

def _return_ordered_img_list(img_filepaths):
    
    ordered_img_idx = _return_ordered_img_index(img_filepaths)
    
    img_df = pd.DataFrame([img_filepaths, ordered_img_idx]).T
    img_df = img_df.sort_values(1).reset_index(drop=True)
    
    return img_df[0].tolist()

class _GIF:
    
    def __init__(self):
        """"""
        
    def get_image_paths(self, glob_path):
        
        """/path/to/imgs/dir/png.N.png"""
        
        self._img_filepaths = glob.glob(glob_path)
        print("{} image files".format(len(self._img_filepaths)))
        self._ordered_img_list = _return_ordered_img_list(self._img_filepaths)
        
    def make(self, gif_outpath="saved_pygif.gif", duration=40, n_loops=0):
        
        self._img_files = (Image.open(f) for f in self._ordered_img_list)
        img = next(self._img_files)
        img.save(fp=gif_outpath, format='GIF',
                 append_images=self._img_files,
                 save_all=True,
                 duration=duration,
                 loop=n_loops)
        
        print("GIF saved to {}".format(gif_outpath))
        
        
def _make_GIF(glob_path, gif_outpath="saved_pygif.gif", duration=40, n_loops=0):
    
    """Make a GIF from a list of images"""
    
    gif = _GIF()
    gif.get_image_paths(glob_path)
    gif.make(gif_outpath, duration, n_loops)