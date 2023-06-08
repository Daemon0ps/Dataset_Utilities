import os,sys
import cv2
import numpy as np
from PIL import Image,ImageFile,ImageOps,ImageFilter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from tqdm import tqdm
import pandas as pd
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from math import ceil

file_path = "P:/from_path/"
save_to_path = "P:/save_to_path/"
img_types = [str(f).replace('.','') for f,u in Image.registered_extensions().items()]
img_files = [file_path+f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) 
             and f[-(f[::-1].find('.')):] in [str(f).replace('.','') for f,u in Image.registered_extensions().items()]]

def main(img_files, i_f):
    w,h = (64,64)
    img = cv2.imread(img_files[i_f])
    img_buf = cv2.imencode(str('.'+img_files[i_f][-(img_files[i_f][::-1].find('.')):]),img)[1]
    md5_calc = str(hashlib.md5(img_buf).hexdigest())
    pil_arr = cv2.blur(img,(10,10))
    img_thumb = ImageOps.contain(Image.fromarray(cv2.cvtColor(pil_arr ,cv2.COLOR_BGR2RGB)),(w,h))
    img_conv = img_thumb.convert(mode="RGB",palette=Image.ADAPTIVE,colors=256).convert(mode="RGBA")
    ifin = cv2.cvtColor(np.array(img_conv),cv2.COLOR_RGB2BGR)
    pil_arr = cv2.cvtColor(np.array(cv2.blur(ifin,(3,3))), cv2.COLOR_BGR2RGB)
    img_arr = np.array(pil_arr).astype('uint8')
    h, w, c = img_arr.shape
    arr_list = [str(('{:02X}' * 3).format(r, g, b))+chr(32) for r,g,b,a in img_arr.reshape(-1,4)]
    pix_list = np.array_split(np.array(arr_list),64)
    pixel_lines = []
    pixel_lines=[" ".join(str(y) for y in [x for x in pix_list])]
    for i, line in enumerate(pixel_lines):
        pixel_lines[i] = " ".join([x for x in word_tokenize(line)])
    vectorizer = CountVectorizer(ngram_range = (2,2))
    count_vect = vectorizer.fit_transform(pixel_lines) 
    features = (vectorizer.get_feature_names_out())
    vectorizer = TfidfVectorizer(ngram_range = (16,16))
    tfidf_vect = vectorizer.fit_transform(pixel_lines)
    sums = tfidf_vect.sum(axis = 0)
    data1 = []
    for col, term in enumerate(features):
        data1.append( (term, sums[0,col] ))
    ranking = pd.DataFrame(data1, columns = ['term','rank'])
    words = (ranking.sort_values('rank', ascending = False))
    f_head = [x for x in list(words.iloc[0:10,0])]
    f_name = ''.join(str(x).split(' ')[0] for x in np.unique(np.array(f_head)).tolist())[:64]
    f_id = str(os.path.basename(img_files[i_f])).replace(img_files[i_f][-(img_files[i_f][::-1].find('.'))-1:],'')
    f_nn = str(file_path+f_name+md5_calc+str(i_f).zfill(4)+'.'+img_files[i_f][-(img_files[i_f][::-1].find('.')):])
    os.rename(img_files[i_f],f_nn)

fl_len = len(img_files)
status_bar = tqdm(total=fl_len, desc='Images')
with ThreadPoolExecutor(16) as executor:
    futures = [executor.submit(main, img_files, i_f) for i_f in range(0,len(img_files)-1)]
    for _ in as_completed(futures):
        status_bar.update(n=1)
