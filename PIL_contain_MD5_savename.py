import os,sys
from PIL import Image,ImageOps,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from io import BytesIO
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import shutil
import hashlib

file_path = "P:/file_path/"
save_to_path = "P:/save_to_path/"

constrain_w_h = (1280,1280)

def iptc_quick(file):
    try:
        with open(file_path+file,"rb") as fi:
            file_bytes = fi.read()
        md5_calc = str(hashlib.md5(file_bytes).hexdigest())
        img_buf = BytesIO(file_bytes)
        img = Image.open(img_buf)
        img = img.convert('RGB')
        img = ImageOps.contain(img, constrain_w_h)
        img.save(save_to_path+md5_calc+".jpg", "JPEG", quality=95)
        f_name = file
        t_name = file_path+f_name[:(len(f_name))-1-len(f_name[-(f_name[::-1].find('.')):])]+".txt"
        shutil.copy(t_name,save_to_path+md5_calc+".txt")
        os.remove(file_path+file)
        os.remove(t_name)
    except Exception as e:
        print(e)
        pass
    finally: pass

file_list = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) \
            and f[-(f[::-1].find('.')):] in[str(f).replace('.','') for f,u in Image.registered_extensions().items()]] 

def main():
    try:
        status_bar = tqdm(total= len(file_list), desc='Images')
        with ThreadPoolExecutor(16) as executor:
            futures = [executor.submit(iptc_quick, i) for i in file_list]
            for _ in as_completed(futures):
                status_bar.update(n=1)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
    finally: pass



main()
