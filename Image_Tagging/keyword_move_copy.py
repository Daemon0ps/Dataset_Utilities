import os
from PIL import Image,ImageOps,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from iptcinfo3 import IPTCInfo
import codecs
import unicodedata
import shutil
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from dataclasses import dataclass
@dataclass
class CFG:
    src_path = "P:/file_path/"
    dest_path = "P:/save_to_path/"
    img_types = [str(f).replace('.','') for f,u in Image.registered_extensions().items()]
    txt_types = ['txt','cap']
    txt_kw = []
    kw_copy_bool = True
    kw_move_bool = False
    move_kw = ['keyword1','keyword2']
    def __post_init__(self):
        self.img_files = CFG.img_types
        self.txt_types = CFG.txt_types
        self.txt_kw = CFG.txt_kw
        self = self
        self.src_path = CFG.src_path
        self.dest_path = CFG.dest_path
        self.kw_copy_bool = CFG.kw_copy_bool
        self.kw_move_bool = CFG.kw_move_bool
        super().__setattr__('attr_name', self)

def left(s:str, amt:int)->str:
    return s[:amt]

def kw_move():
        def kw_proc(file:str)->list:
            all_kw = []
            f_name = file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]
            ext = str(file[-(file[::-1].find('.')):])
            if os.path.isfile(CFG.src_path+f_name+".txt")\
                or os.path.isfile(CFG.src_path+f_name+".cap"):
                with open(CFG.src_path+f_name+".txt","rt") as fi:
                    txt_data = fi.read()
                txt_data = bytes(txt_data,'utf-8')
                txt_data = codecs.decode(unicodedata.normalize('NFKD', codecs.decode(txt_data)).encode('ascii', 'ignore'))
                if len(txt_data.split('\n')) > len(txt_data.split(',')):
                    txt_split = txt_data.split('\n')
                    tag_list = np.unique(np.array([str(x).strip().lower() for x in txt_split if len(x)>0])).tolist()
                    for t in tag_list:
                        all_kw.append(t)
                elif len(txt_data.split(',')) > len(txt_data.split('\n')) :
                    txt_split = txt_data.split(',')
                    tag_list = np.unique(np.array([str(x).strip().lower() for x in txt_split if len(x)>0])).tolist()
                    for t in tag_list:
                        all_kw.append(t)
            if ext == "jpg" or ext == "jpeg":
                iptc_info = IPTCInfo(CFG.src_path+file, force=True)
                iptc_kw = iptc_info['keywords']
                if len(iptc_kw)>0:
                    for i in iptc_kw:
                        all_kw.append(str(codecs.decode(i,encoding='utf-8')).strip().lower())
            if len(all_kw)>0:
                for ttm in CFG.move_kw:
                    if set(ttm).issubset(all_kw) or str(all_kw).find(str(ttm))!=-1:
                        try:
                            assert os.path.isdir(left(CFG.src_path,len(CFG.src_path)-1))
                            if CFG.kw_copy_bool:
                                shutil.copy(CFG.src_path+file,CFG.dest_path+file)
                            elif CFG.kw_move_bool:
                                shutil.move(CFG.src_path+file,CFG.dest_path+file)
                        except Exception as e:
                            print(e)
                            pass
                        finally: pass
        img_files = [f for f in os.listdir(CFG.src_path[:-1:]) if os.path.isfile(CFG.src_path+f) and f[-(f[::-1].find('.')):] in CFG.img_types]
        status_bar = tqdm(total=len(img_files), desc='Images')
        with ThreadPoolExecutor(8) as executor:
            futures = [executor.submit(kw_proc, f) for f in img_files]
            for _ in as_completed(futures):
                status_bar.update(n=1)
