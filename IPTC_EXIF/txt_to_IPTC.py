#iptc_quick.py
import os,sys
from PIL import Image,ImageOps,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from io import BytesIO
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from PIL import Image,ImageOps,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from tqdm import tqdm
from iptcinfo3 import IPTCInfo
import codecs
import unicodedata

file_path = "L:/datasets/all/proc/iptc/"
save_to_path = "L:/datasets/all/proc/iptc/"
constrain_w_h = (1280,1280)

def iptc_quick(file):
    try:
        with open(file_path+file,"rb") as fi:
            file_bytes = fi.read()
        img_buf = BytesIO(file_bytes)
        img = Image.open(img_buf)
        exif_info = img.getexif()
        img = img.convert('RGB')
        try:
            img = ImageOps.exif_transpose(img)
        except Exception as e:
            print(e)
            pass
        finally: pass
        img = ImageOps.contain(img, constrain_w_h)
        img.save(save_to_path+file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]+".jpg", "JPEG", quality=95, exif=exif_info)
        s_name = save_to_path+file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]+".jpg"
        t_name = file_path+file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]+".txt" 
        with open(t_name,'rt') as fi:
            txt_data = fi.read()
        txt_data = bytes(txt_data,'utf-8')
        txt_data = codecs.decode(unicodedata.normalize('NFKD', codecs.decode(txt_data)).encode('ascii', 'ignore'))  
        txt_data = str(txt_data)
        txt_list = txt_data.split(",")    
        iptc_info = IPTCInfo(s_name, force=True)
        iptc_info['keywords'] = txt_list
        iptc_info.save()
    except Exception as e:
        print(e)
        pass
    finally: pass

def main(file_list):
    try:
        with ThreadPoolExecutor(32) as executor:
            futures = [executor.submit(iptc_quick, i) for i in file_list]
            for _ in as_completed(futures):
                status_bar.update(n=1)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
    finally: pass

file_list = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) \
            and f[-(f[::-1].find('.')):] in[str(f).replace('.','') \
            for f,u in Image.registered_extensions().items()]] 

fl_len = len(file_list)

status_bar = tqdm(total=fl_len, desc='Images')

main(file_list)
