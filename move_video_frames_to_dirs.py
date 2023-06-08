#CD P:/VIDEOS/
#FOR /F "tokens=*" %G IN ('dir /b *.mov') DO ffmpeg -skip_frame nokey -i "%G" -vsync 0 -qscale:v 2 -f image2 "P:\VIDEOS\FRAMES\%~nG_%07d.jpg"

import os
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from tqdm import tqdm
import re
from unidecode import unidecode
import string
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

def rm_punct(s:str)->str:
    return s.translate(str.maketrans('', '', string.punctuation))

def rm_white(s:str)->str:
    return  " ".join(str(s).split())

def rm_spec(s:str)->str:
    return re.sub('\s+', ' ', (re.sub('_', '', (re.sub('[^a-zA-z0-9\s]', '', unidecode(str(s))))))).strip().lower()

file_path = "P:/VIDEOS/FRAMES/"
vid_path = "P:/VIDEOS/"
save_to_path = "P:/wat/VIDEOS/FRAMES/"

vid_list = [f for f in os.listdir(vid_path[:-1:]) if os.path.isfile(vid_path+f) \
             and f[-(f[::-1].find('.')):] in ['avi','mp4']]

def vid_dir_proc(file:str):
    f_left = str(file[:-12])
    img_list = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) \
                and f.find(f_left)!=-1 and f[-(f[::-1].find('.')):] in[str(f).replace('.','') \
                for f,u in Image.registered_extensions().items()]]
    f_dir = rm_white(rm_spec(rm_punct(f_left.replace(chr(32),"_"))))
    if not os.path.isdir(file_path+f_dir):
        os.makedirs(file_path+f_dir,exist_ok=True)
    for img_f in img_list:
        shutil.move(file_path+img_f,file_path+f_dir)



def main(vid_list):
    with ThreadPoolExecutor(16) as executor:
        futures = [executor.submit(vid_dir_proc, i) for i in vid_list]
        for _ in as_completed(futures):
            status_bar.update(n=1)

vl_len = len(vid_list)

status_bar = tqdm(total=vl_len, desc='Images')

main(vid_list)
