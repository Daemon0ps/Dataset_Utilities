import os
from PIL import Image
from tqdm import tqdm
from termcolor import cprint
from concurrent.futures import ThreadPoolExecutor, as_completed
img_list = []
file_list = []
imgfiles = ['HEIC','HEIF']
import pillow_heif
pillow_heif.register_heif_opener()

def img_proc(img_list,file_path):
        for imgfile in tqdm(img_list):
            img = Image.open(imgfile)
            f_name = os.path.basename(imgfile)
            s_name = file_path+f_name[:(len(f_name))-len(f_name[-(f_name[::-1].find('.')):])]+"jpg"
            img.save(s_name, "JPEG", quality=95)

def __main__():
        file_path = ""
        cprint("Enter Source Path:", "red",end="")
        file_path = input("")
        file_path = file_path+"/"
        file_path = file_path.replace('\\','/')
        print(file_path)
        print(file_path[::1])
        if os.path.isdir(file_path[:-1:]) == False:
            cprint("Please enter a valid path","white",attrs=['bold','underline'])
            file_path = ""
        elif os.path.isdir(file_path[:-1:]) == True:
            file_list = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f)]
            for file in file_list:
                if (file[-(file[::-1].find('.')):] in imgfiles):
                    img_list.append(file_path+file)
        fl_len = len(img_list)
        status_bar = tqdm(total=fl_len, desc='Images')
        with ThreadPoolExecutor(8) as executor:
            futures = [executor.submit(img_proc,file_path, i) for i in file_list]
            for _ in as_completed(futures):
                status_bar.update(n=1)                    
            img_proc(img_list,file_path)
__main__()



