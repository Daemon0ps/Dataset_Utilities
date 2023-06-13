
#iptc_to_txt_quick.py

import os
from PIL import Image, ImageFile
from tqdm import tqdm
from iptcinfo3 import IPTCInfo
ImageFile.LOAD_TRUNCATED_IMAGES = True
import codecs
from traceback_with_variables import activate_by_import
from concurrent.futures import ThreadPoolExecutor, as_completed
from unidecode import unidecode

file_path = "D:/datasets/cms_exp_cond_00/stage4/"
save_to_path = "D:/datasets/cms_exp_cond_00/stage4/"

file_list = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) \
             and f[-(f[::-1].find('.')):] in[str(f).replace('.','') \
            for f,u in Image.registered_extensions().items()]]

def iptc_proc(file):
    iptc_info = IPTCInfo(file_path+file,force=True)
    tag_list = []
    tag_list.clear()
    tag_list = [codecs.decode(x,encoding='utf-8') for x in iptc_info['keywords']]
    t_name = file_path+file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]+".txt" 
    if len(tag_list) > 0:
        with open(t_name,"wt") as fi:
            for i in range(0,len(tag_list)-1):
                if i < len(tag_list)-1:
                    fi.write(str(tag_list[i]))
                    fi.write(str(", "))
                elif i == len(tag_list)-1:
                    fi.write(str(tag_list[i]))

status_bar = tqdm(total=len(file_list), desc='Parsing Emails')

def main():
    with ThreadPoolExecutor(8) as executor:
        futures = [executor.submit(iptc_proc,f) for f in file_list]
        for _ in as_completed(futures):
            status_bar.update(n=1)

main()
