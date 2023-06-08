import os, sys
from termcolor import cprint
import codecs
import unicodedata
from unidecode import unidecode
import string
import re
import nltk
import shutil
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from concurrent.futures import ThreadPoolExecutor, as_completed
from traceback_with_variables import activate_by_import
from iptcinfo3 import IPTCInfo
from PIL import Image,ImageOps,ImageFile,ExifTags

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from PIL.Image import Resampling, Transpose
from datetime import datetime
import numpy as np
from time import sleep
from tqdm import tqdm

from dataclasses import dataclass
@dataclass
class CFG:
    src_path = "P:/file_path/"
    dest_path = "P:/save_to_path/"
    bool_padding = True
    bool_resize_only = False
    bool_sequential_rename = False
    bool_transpose_images = True
    bool_no_text_copy = False
    add_text_src = ""
    add_text_data_front = ""
    add_text_data_back = ""
    append_sequence = ""
    replace_text_src = ""
    text_data_replace = ""
    text_data_replacement = ""
    replace_list = []
    resize_w = "512"
    resize_h = "512"
    resize_src = ""
    resize_dest = ""
    replace_text_file = ""
    img_types = [str(f).replace('.','') for f,u in Image.registered_extensions().items()]
    txt_types = ['txt','cap']
    txt_kw = []
    txt_kw_uniq = []
    move_kw = []
    kw_copy_bool = True
    kw_move_bool = False
    kw_mvcp_text_bool = True
    kw_mvcp_iptc_bool = True
    kw_mvcp_exif_bool = True
    img_exif_transpose_bool = True
    tag_page = 0
    tag_count = 0
    tag_array_split = []
    tag_table_change = []
    kw_save_bool = False

    def __post_init__(self):
        self = self
        self.src_path = CFG.src_path
        self.dest_path = CFG.dest_path
        self.bool_padding = CFG.bool_padding
        self.bool_resize_only = CFG.bool_resize_only
        self.bool_sequential_rename = CFG.bool_sequential_rename
        self.bool_transpose_images = CFG.bool_transpose_images
        self.bool_no_text_copy = CFG.bool_no_text_copy
        self.add_text_src = CFG.add_text_src
        self.add_text_data_front = CFG.add_text_data_front
        self.add_text_data_back = CFG.add_text_data_back
        self.append_sequence = CFG.append_sequence
        self.replace_text_src = CFG.replace_text_src
        self.text_data_replace = CFG.text_data_replace
        self.text_data_replacement = CFG.text_data_replacement
        self.replace_list = CFG.replace_list
        self.resize_w = CFG.resize_w
        self.resize_h = CFG.resize_h
        self.resize_src = CFG.resize_src
        self.resize_dest = CFG.resize_dest
        self.replace_text_file = CFG.replace_text_file
        self.img_files = CFG.img_types
        self.txt_types = CFG.txt_types
        self.txt_kw = CFG.txt_kw
        self.txt_kw_uniq = CFG.txt_kw_uniq
        self.move_kw = CFG.move_kw
        self.kw_copy_bool = CFG.kw_copy_bool
        self.kw_move_bool = CFG.kw_move_bool
        self.kw_mvcp_text_bool = CFG.kw_mvcp_text_bool
        self.kw_mvcp_iptc_bool = CFG.kw_mvcp_iptc_bool
        self.img_exif_transpose_bool = CFG.img_exif_transpose_bool
        self.tag_page = CFG.tag_page
        self.tag_count = CFG.tag_count
        self.tag_array_split = CFG.tag_array_split
        self.tag_table_change = CFG.tag_table_change
        self.kw_save_bool = CFG.kw_save_bool
        super().__setattr__('attr_name', self)



def rm_punct(s:str)->str:
    return s.translate(str.maketrans('', '', string.punctuation))

def rm_white(s:str)->str:
    return  " ".join(str(s).split())

def rm_sw(s:str)->str:
    sw = set(stopwords.words("english"))
    wt = word_tokenize(str(s))
    t = ' '.join(w for w in wt if w not in sw)
    return t

def rm_spec(s:str)->str:
    return re.sub('\s+', ' ', (re.sub('_', '', (re.sub('[^a-zA-z0-9\s]', '', unidecode(str(s))))))).strip().lower()

def left(s:str, amt:int)->str:
    return s[:amt]

def right(s:str, amt:int)->str:
    return s[-amt:]

def mid(s:str, offset:int, amt:int)->str:
    return s[offset:offset+amt]

def brk():
    def __init__(s):
        return s

def try_utf8(f_txt_data):
    try:
        return codecs.decode(f_txt_data,encoding="utf-8")
    except Exception:
        return None

def no_ext(file:str)->str:
    f_name = file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]
    return str(f_name)

def image_resize(img, resize_w, resize_h):
    img_resized = ImageOps.contain(img,(resize_w, resize_h),method=Resampling.BICUBIC,reducing_gap=3.0)
    return img_resized

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
                                shutil.copy(CFG.src_path+file,CFG.dest_path+file)
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

def text_add(
            add_text_data_front:str
            ,add_text_data_back:str
            ):
    def txt_proc(f):
        with open(CFG.src_path+f,"rt") as fi:
            txt_data = fi.read()
        txt_data = bytes(txt_data,'utf-8')
        txt_data = str(codecs.decode(unicodedata.normalize('NFKD', codecs.decode(txt_data)).encode('ascii', 'ignore'))).replace('\r\n','\n')
        if len(txt_data.split('\n')) > len(txt_data.split(',')):
            if add_text_data_front is not None and len(add_text_data_front)>0:
                txt_data = add_text_data_front + "\n" + txt_data
            if add_text_data_back is not None and len(add_text_data_back)>0:
                txt_data = txt_data + "\n" + add_text_data_back
        elif len(txt_data.split(',')) > len(txt_data.split('\n')) :
            if add_text_data_front is not None and len(add_text_data_front)>0:
                txt_data = add_text_data_front + "," + txt_data
            if add_text_data_back is not None and len(add_text_data_back)>0:
                txt_data = txt_data + "," + add_text_data_back
        with open(CFG.src_path+f,"wt") as fi:
            fi.write(txt_data)
        return
    txt_files = [f for f in os.listdir(CFG.src_path[:-1:]) if os.path.isfile(CFG.src_path+f) and f[-(f[::-1].find('.')):] in CFG.txt_types]
    status_bar = tqdm(total=len(txt_files), desc='Images')
    with ThreadPoolExecutor(8) as executor:
        futures = [executor.submit(txt_proc, f) for f in txt_files]
        for _ in as_completed(futures):
            status_bar.update(n=1)
    return

def tag_dedup():
    def txt_proc(f):
        txt_split=[]
        txt_uniq = []
        with open(CFG.src_path+f,"rt") as fi:
            txt_data = fi.read()
        txt_data = bytes(txt_data,'utf-8')
        txt_data = str(codecs.decode(unicodedata.normalize('NFKD', codecs.decode(txt_data)).encode('ascii', 'ignore'))).replace('\r\n','\n')
        if len(txt_data.split('\n')) > len(txt_data.split(',')):
            txt_split = txt_data.split('\n')
            txt_uniq = np.unique(np.array([str(x).strip() for x in txt_split if len(x)>0])).tolist()
            with open(CFG.src_path+f,"wt") as fi:
                for i in range(0,len(txt_uniq)-1):
                    fi.write(txt_uniq[i]+str("\n"))
                fi.write(txt_uniq[len(txt_uniq)-1])
        elif len(txt_data.split(',')) > len(txt_data.split('\n')) :
            txt_split = txt_data.split(',')
            txt_uniq = np.unique(np.array([str(x).strip() for x in txt_split if len(x)>0])).tolist()
            with open(CFG.src_path+f,"wt") as fi:
                for i in range(0,len(txt_uniq)-2):
                    fi.write(txt_uniq[i]+str(", "))
                fi.write(txt_uniq[len(txt_uniq)-1])
        return
    txt_files = [f for f in os.listdir(CFG.src_path[:-1:]) if os.path.isfile(CFG.src_path+f) and f[-(f[::-1].find('.')):] in CFG.txt_types]
    status_bar = tqdm(total=len(txt_files), desc='Images')
    with ThreadPoolExecutor(8) as executor:
        futures = [executor.submit(txt_proc, f) for f in txt_files]
        for _ in as_completed(futures):
            status_bar.update(n=1)
    return

def all_keywords():
    def txt_proc(f):
        f_name = f[:(len(f))-1-len(f[-(f[::-1].find('.')):])]
        ext = str(f[-(f[::-1].find('.')):])
        txt_split=[]
        txt_split.clear()
        txt_uniq = []
        txt_uniq.clear()
        iptc_kw_list = []
        iptc_kw_list.clear()
        f_tags = []
        f_tags.clear()
        if os.path.isfile(CFG.src_path+f_name+".txt"):
            with open(CFG.src_path+f_name+".txt","rt") as fi:
                txt_data = fi.read()
            txt_data = bytes(txt_data,'utf-8')
            txt_data = str(codecs.decode(unicodedata.normalize('NFKD', codecs.decode(txt_data)).encode('ascii', 'ignore'))).replace('\r\n','\n')
            if len(txt_data.split('\n')) > len(txt_data.split(',')):
                txt_split = txt_data.split('\n')
                txt_uniq = np.unique(np.array(txt_split)).tolist()
                for tu in txt_uniq:
                    f_tags.append(str(tu).strip().lower())
                    CFG.txt_kw.append(str(tu).strip().lower())
            elif len(txt_data.split(',')) > len(txt_data.split('\n')) :
                txt_split = txt_data.split(',')
                txt_uniq = np.unique(np.array(txt_split)).tolist()
                for tu in txt_uniq:
                    f_tags.append(str(tu).strip().lower())
                    CFG.txt_kw.append(str(tu).strip().lower())
        if os.path.isfile(CFG.src_path+f_name+".jpeg"):
            os.rename(CFG.src_path+f_name+".jpeg",CFG.src_path+f_name+".jpg")
        if os.path.isfile(CFG.src_path+f_name+".jpg"):           
            iptc_info = IPTCInfo(CFG.src_path+f_name+".jpg", force=True)
            iptc_kw = iptc_info['keywords']
            print(iptc_kw)
            if iptc_kw is not None and len(iptc_kw)>0:
                iptc_kw_decode = [str(codecs.decode(x,encoding='utf-8')) for x in iptc_kw]
                iptc_kw_list = [str(x).strip().lower() for x in iptc_kw_decode if len(x)>0]
                txt_uniq = np.unique(np.array(iptc_kw_list)).tolist()
                if len(txt_uniq)>0:
                    for kw in txt_uniq:
                        f_tags.append(str(tu).strip().lower())
                        CFG.txt_kw.append(str(kw))
        txt_uniq.clear()
        txt_uniq = np.unique(np.array(f_tags)).tolist()
        with open(CFG.src_path+f_name+".txt","wt") as fi:
            for tag in txt_uniq:
                fi.write(str(tag)+"\n")
        return
    img_files = [f for f in os.listdir(CFG.src_path[:-1:]) if os.path.isfile(CFG.src_path+f) and f[-(f[::-1].find('.')):] in CFG.img_types]
    status_bar = tqdm(total=len(img_files), desc='Images')
    with ThreadPoolExecutor(8) as executor:
        futures = [executor.submit(txt_proc, f) for f in img_files]
        for _ in as_completed(futures):
            status_bar.update(n=1)
    CFG.txt_kw_uniq = np.unique(np.array(CFG.txt_kw)).tolist()
    CFG.txt_kw = []
    CFG.txt_kw.clear()
    CFG.tag_count = len(CFG.txt_kw_uniq)
    CFG.tag_array_split = np.array_split(CFG.txt_kw_uniq,len(CFG.txt_kw_uniq)/20)
    if CFG.kw_save_bool:
        with open(CFG.dest_path+"keyword_list.txt","wt") as fi:
            for kw in CFG.txt_kw_uniq:
                fi.write(str(kw) + str("\n"))
    return

def change_table_iter(chg:list,tag:str)->str:
    ch_idx = [x for x in [i for i in chg] if set(tag).issubset(set(x[0]))]
    return ch_idx[0]

def ApplyChanges():

    def chg_proc(f:str):
        txt_split=[]
        txt_uniq = []
        iptc_kw_list = []
        replaced = []
        repl_uniq = []
        f_name = f[:(len(f))-1-len(f[-(f[::-1].find('.')):])]
        if os.path.isfile(CFG.src_path+f_name+".txt"):
            with open(CFG.src_path+f_name+".txt","rt") as fi:
                txt_data = fi.read()
            txt_data = bytes(txt_data,'utf-8')
            txt_data = str(codecs.decode(unicodedata.normalize('NFKD', codecs.decode(txt_data)).encode('ascii', 'ignore'))).replace('\r\n','\n')
            if len(txt_data.split('\n')) > len(txt_data.split(',')):
                txt_split = txt_data.split('\n')
                txt_uniq = np.unique(np.array(txt_split)).tolist()
                for tu in txt_uniq:
                    if tu in [x[0] for x in [i for i in CFG.tag_table_change]]:
                        tbl_chg = change_table_iter(CFG.tag_table_change,tu)
                        tu = tbl_chg[2]
                        if len(tu)>0:
                            replaced.append(tu)
            elif len(txt_data.split(',')) > len(txt_data.split('\n')) :
                txt_split = txt_data.split(',')
                txt_uniq = np.unique(np.array(txt_split)).tolist()
                for tu in txt_uniq:
                    if tu in [x[0] for x in [i for i in CFG.tag_table_change]]:
                        tbl_chg = change_table_iter(CFG.tag_table_change,tu)
                        tu = tbl_chg[2]
                        if len(tu)>0:
                            replaced.append(tu)
            with open(CFG.src_path+f_name+".txt","wt") as fi:
                for x in replaced:
                    fi.write(x)
        if os.path.isfile(CFG.src_path+f_name+".jpeg"):
            os.rename(CFG.src_path+f_name+".jpeg",CFG.src_path+f_name+".jpg")
        if os.path.isfile(CFG.src_path+f_name+".jpg"):
            iptc_info = IPTCInfo(CFG.src_path+f_name+".jpg", force=True)
            iptc_kw = iptc_info['keywords']
            if iptc_kw is not None and len(iptc_kw)>0:
                iptc_kw_decode = [str(codecs.decode(x,encoding='utf-8')) for x in iptc_kw]
                iptc_kw_list = [rm_white(str(x).strip().lower()) for x in iptc_kw_decode if len(x)>0]
                if len(iptc_kw_list)>0:
                    for kw in iptc_kw_list:
                        if set(kw).issubset(set(str(x[0]) for x in [i for i in CFG.tag_table_change])):
                            tbl_chg = change_table_iter(CFG.tag_table_change,tu)
                            print(tbl_chg)
                            tu = tbl_chg[2]
                            if len(tu)>0:
                                replaced.append(tu)
            repl_uniq = np.unique(np.array([str(x).strip().lower() for x in replaced if len(x)>0])).tolist()
            print(repl_uniq)
            iptc_info['keywords'] = repl_uniq
            iptc_info.save()
        if os.path.isfile(CFG.src_path+f_name+".txt"):
            with open(CFG.src_path+f_name+".txt","wt") as fi:
                for x in repl_uniq:
                    fi.write(x)
    img_files = [f for f in os.listdir(CFG.src_path[:-1:]) if os.path.isfile(CFG.src_path+f) and f[-(f[::-1].find('.')):] in CFG.img_types]
    status_bar = tqdm(total=len(img_files), desc='Images')
    with ThreadPoolExecutor(8) as executor:
        futures = [executor.submit(chg_proc, f) for f in img_files]
        for _ in as_completed(futures):
            status_bar.update(n=1)

@staticmethod
def cp_lf(): 
    try:
        cs =  cprint("", "black") 
        return cs
    except Exception as e: pass
    finally: pass
@staticmethod
def cp_bk(x): 
    try:
        cs =  cprint(x, "black",end="") 
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_r(x): 
    try:
        cs =  cprint(x, "red",end="") 
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_g(x): 
    try:
        cs =  cprint(x, "green",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_y(x): 
    try:
        cs =  cprint(x, "yellow",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_b(x): 
    try:
        cs =  cprint(x, "blue",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_m(x): 
    try:
        cs =  cprint(x, "magenta",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_c(x): 
    try:
        cs =  cprint(x, "cyan",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_w(x): 
    try:
        cs =  cprint(x, "white",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_lgr(x): 
    try:
        cs =  cprint(x, "light_grey",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_dg(x): 
    try:
        cs =  cprint(x, "dark_grey",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_lr(x): 
    try:
        cs =  cprint(x, "light_red",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_lg(x): 
    try:
        cs =  cprint(x, "light_green",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_ly(x): 
    try:
        cs =  cprint(x, "light_yellow",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_lb(x): 
    try:
        cs =  cprint(x, "light_blue",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_lm(x): 
    try:
        cs =  cprint(x, "light_magenta",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_lc(x): 
    try:
        cs =  cprint(x, "light_cyan",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_obk(x): 
    try:
        cs =  cprint(x, "on_black",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_or(x): 
    try:
        cs =  cprint(x, "on_red",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_og(x): 
    try:
        cs =  cprint(x, "on_green",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_oy(x): 
    try:
        cs =  cprint(x, "on_yellow",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod
def cp_ob(x): 
    try:
        cs =  cprint(x, "on_blue",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_om(x): 
    try:
        cs =  cprint(x, "on_magenta",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_oc(x): 
    try:
        cs =  cprint(x, "on_cyan",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_ow(x): 
    try:
        cs =  cprint(x, "on_white",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_olgr(x): 
    try:
        cs =  cprint(x, "on_light_grey",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_odg(x): 
    try:
        cs =  cprint(x, "on_dark_grey",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_olr(x): 
    try:
        cs =  cprint(x, "on_light_red",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_olg(x): 
    try:
        cs =  cprint(x, "on_light_green",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_oly(x): 
    try:
        cs =  cprint(x, "on_light_yellow",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_olb(x): 
    try:
        cs =  cprint(x, "on_light_blue",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_olm(x):
    try:
        cs =  cprint(x, "on_light_magenta",end="")
        return cs
    except Exception as e:pass
    finally:pass
@staticmethod    
def cp_olc(x): 
    try:
        cs =  cprint(x, "on_light_cyan",end="")
        return cs
    except Exception as e:pass
    finally:pass
