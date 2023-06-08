import os
from PIL import Image,ImageOps,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

file_path = "P:/file_path/"
save_to_path = "P:/save_to_path/"

constrain_w_h = (640,640)

def img_contain(file):
    try:
        img = Image.open(file_path+file).convert('RGB')
        img = ImageOps.contain(img, constrain_w_h)
        img.save(save_to_path+file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]+".jpg", "JPEG", quality=95)
    except Exception as e:
        print(e)
        pass
    finally: pass

def main(file_list):
    status_bar = tqdm(total=len(file_list), desc='Images')
    with ThreadPoolExecutor(16) as executor:
        futures = [executor.submit(img_contain, i) for i in file_list]
        for _ in as_completed(futures):
            status_bar.update(n=1)

file_list = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) \
             and f[-(f[::-1].find('.')):] in[str(f).replace('.','') \
            for f,u in Image.registered_extensions().items()]]

main(file_list)
