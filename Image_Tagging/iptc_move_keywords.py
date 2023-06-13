import os
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from iptcinfo3 import IPTCInfo
import codecs
import unicodedata
import shutil
import numpy as np
from tqdm import tqdm
from traceback_with_variables import activate_by_import
from concurrent.futures import ThreadPoolExecutor, as_completed

from dataclasses import dataclass
@dataclass
class CFG:
    src_path = "D:/4chan/d/"
    dest_path = "D:/4chan/d/"
    #img_types = [str(f).replace('.','') for f,u in Image.registered_extensions().items()]
    txt_types = ['txt','cap']
    txt_kw = []
    kw_copy_bool = True
    kw_move_bool = False
    move_kw = ['no humans']
    list_gen = "walk" #"list"
    img_types = [
            'blp', 'bmp', 'dib', 'bufr', 'cur'
            , 'pcx', 'dcx', 'dds', 'ps', 'eps'
            , 'fit', 'fits', 'fli', 'flc', 'ftc'
            , 'ftu', 'gbr', 'gif', 'grib', 'h5'
            , 'hdf', 'png', 'apng', 'jp2', 'j2k'
            , 'jpc', 'jpf', 'jpx', 'j2c', 'icns'
            , 'ico', 'im', 'iim', 'tif', 'tiff'
            , 'jfif', 'jpe', 'jpg', 'jpeg', 'mpg'
            , 'mpeg', 'mpo', 'msp', 'palm', 'pcd'
            , 'pxr', 'pbm', 'pgm', 'ppm', 'pnm'
            , 'psd', 'bw', 'rgb', 'rgba', 'sgi'
            , 'ras', 'tga', 'icb', 'vda', 'vst'
            , 'webp', 'wmf', 'emf', 'xbm', 'xpm'
            ,'nef'
            ]
    all_words = []
    file_list = []
    def __post_init__(self):
        self.img_files = CFG.img_types
        self.txt_types = CFG.txt_types
        self.txt_kw = CFG.txt_kw
        self = self
        self.src_path = CFG.src_path
        self.dest_path = CFG.dest_path
        self.kw_copy_bool = CFG.kw_copy_bool
        self.kw_move_bool = CFG.kw_move_bool
        self.list_gen = CFG.list_gen
        self.img_types = CFG.img_types
        self.all_words = CFG.all_words
        self.file_list = CFG.file_list
        super().__setattr__('attr_name', self)

def left(s:str, amt:int)->str:
    return s[:amt]

def kw_list():

    def kw_proc(file:str)->list:
        txt_list = []
        txt_list.clear()
        iptc_info = IPTCInfo(file, force=True)
        txt_list = iptc_info['keywords']
        for kw in txt_list:
            CFG.all_words.append(kw)


    if CFG.list_gen == "walk":
        for r, d, f in os.walk(CFG.src_path[:-1:]):
            for file in f:
                if ((file[-(file[::-1].find('.')):]).lower()) in CFG.img_types:
                    CFG.file_list.append(os.path.join(r, file))
    elif CFG.list_gen == "list":
        CFG.file_list = [CFG.src_path+f for f in os.listdir(CFG.src_path[:-1:]) if os.path.isfile(CFG.src_path+f) \
                    and f[-(f[::-1].find('.')):] in CFG.img_types]
    l_bar='{desc}: {percentage:3.0f}%|'
    r_bar='| {n_fmt}/{total_fmt} [elapsed: {elapsed} / Remaining: {remaining}] '
    bar = '{rate_fmt}{postfix}]'
    with ThreadPoolExecutor(8) as executor:
        status_bar = tqdm(total=len(CFG.file_list), desc='Image Tagging',bar_format=str(f'{l_bar}{bar}{r_bar}'),colour='#6495ED')
        futures = [executor.submit(kw_proc, f) for f in CFG.file_list]
        for _ in as_completed(futures):
            status_bar.update(n=1)
        status_bar.close()
    txt_uniq = np.unique(np.array(CFG.all_words)).tolist()

    with open(CFG.dest_path+"keywords.txt","wt") as fi:
        for x in txt_uniq:
            fi.write(str(codecs.decode(x)).strip() + "\n")

kw_list()
