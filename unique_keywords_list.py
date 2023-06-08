import os
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from PIL.ExifTags import TAGS
from tqdm import tqdm
import codecs
import unicodedata
import numpy as np


file_path = "P:/file_path/"
save_to_path = "P:/save_to_path/"

txt_files = [file_path+f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) and f[-(f[::-1].find('.')):] in ['txt']]

all_words = []

for file in tqdm(txt_files):
    txt_data = ""
    txt_list = []
    txt_list.clear()
    txt_data_list = []
    txt_data_list.clear()  
    uniq_list = []
    uniq_list.clear()  
    with open(file,'rt') as fi:
        txt_data = fi.read()
    txt_data = bytes(txt_data,'utf-8')
    txt_data = codecs.decode(unicodedata.normalize('NFKD', codecs.decode(txt_data)).encode('ascii', 'ignore'))
    txt_list = txt_data.split(',')
    txt_data_list = [f.strip() for f in txt_list]
    for x in txt_data_list:
        all_words.append(x)

uniq_list = np.unique(np.array(all_words)).tolist()

with open(save_to_path+"keywords.txt",'wt') as fi:
    for x in uniq_list:
        fi.write(str(x).strip()+"\n")
