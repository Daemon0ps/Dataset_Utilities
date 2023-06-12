#Threaded -- tested on AMD Ryzen 9 5950X + "SanDisk PRO-BLADE SCSI" NVME

# vit = ~65 it/s
# moat = ~45 it/s
# swinv2 = ~33 it/s
# convnext = ~50 it/s
# convnextv2 = ~45 it/s

# https://note.com/kohya_ss/n/nbf7ce8d80f29
#https://huggingface.co/SmilingWolf
# - [SmilingWolf/wd-v1-4-moat-tagger-v2](https://huggingface.co/SmilingWolf/wd-v1-4-moat-tagger-v2)
# - [SmilingWolf/wd-v1-4-swinv2-tagger-v2](https://huggingface.co/SmilingWolf/wd-v1-4-convnext-tagger-v2)
# - [SmilingWolf/wd-v1-4-convnext-tagger-v2](https://huggingface.co/SmilingWolf/wd-v1-4-convnext-tagger-v2)
# - [SmilingWolf/wd-v1-4-convnextv2-tagger-v2](https://huggingface.co/SmilingWolf/wd-v1-4-convnextv2-tagger-v2)
# - [SmilingWolf/wd-v1-4-vit-tagger-v2](https://huggingface.co/SmilingWolf/wd-v1-4-vit-tagger-v2)

from __future__ import annotations
import os
import cv2
import argparse
from PIL import Image,ImageFile,ImageOps
from huggingface_hub import hf_hub_download
from traceback_with_variables import activate_by_import
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
import huggingface_hub
import numpy as np
import onnxruntime as rt
import pandas as pd
import keyring
from time import sleep
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from termcolor import cprint

print("")
cuda_check = str(rt.get_device())
print(str(cuda_check))
print("")
assert cuda_check == str("GPU")

IMAGE_SIZE = 448
HF_TOKEN = keyring.get_password("hf","hf_key")
MOAT_MODEL_REPO = "SmilingWolf/wd-v1-4-moat-tagger-v2"
SWIN_MODEL_REPO = "SmilingWolf/wd-v1-4-swinv2-tagger-v2"
CONV_MODEL_REPO = "SmilingWolf/wd-v1-4-convnext-tagger-v2"
CONV2_MODEL_REPO = "SmilingWolf/wd-v1-4-convnextv2-tagger-v2"
VIT_MODEL_REPO = "SmilingWolf/wd-v1-4-vit-tagger-v2"
MODEL_FILENAME = "model.onnx"
LABEL_FILENAME = "selected_tags.csv"
EP_LIST = ['CUDAExecutionProvider']
GEN_THRESH:float = 0.35

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
def cp_c(x): 
    try:
        cs =  cprint(x, "cyan",end="")
        return cs
    except Exception as e:pass
    finally:pass

def load_model(model_repo: str, model_filename: str) -> rt.InferenceSession:
    path = huggingface_hub.hf_hub_download(
        model_repo, model_filename, use_auth_token=HF_TOKEN)
    model = rt.InferenceSession(path,providers=EP_LIST)
    return model

def load_labels() -> list[str]:
    path = huggingface_hub.hf_hub_download(
        MOAT_MODEL_REPO, LABEL_FILENAME, use_auth_token=HF_TOKEN)
    df = pd.read_csv(path)
    tag_names = df["name"].tolist()
    general_indexes = list(np.where(df["category"] == 0)[0])
    return tag_names,general_indexes

def txt_write(t_name,tags):
    with open(t_name,"wt") as fi:
        fi.write(tags)
        fi.close

def model_pred(
                image
                ,t_name
                ,general_threshold
                ,tag_names
                ,general_indexes
                ,model
                ):
    input_name = model.get_inputs()[0].name
    label_name = model.get_outputs()[0].name
    probs = model.run([label_name], {input_name: image})[0]
    labels = list(zip(tag_names, probs[0].astype(float)))
    general_names = [labels[i] for i in general_indexes]
    general_res = [x for x in general_names if x[1] > general_threshold]
    general_res = dict(general_res)
    b = dict(sorted(general_res.items(), key=lambda item: item[1], reverse=True))
    a = ",".join(list(b.keys())).replace("_", " ").replace("(", "\(").replace(")", "\)")
    c = ", ".join(list(b.keys()))
    txt_write(t_name,a)

def img_proc(i):
    img = Image.open(i).convert("RGBA")
    new_img = Image.new("RGBA", img.size, "WHITE")
    new_img.paste(img, mask=img)
    img = new_img.convert("RGB")
    img = np.asarray(img)
    img = img[:, :, ::-1]
    size = max(img.shape[0:2])
    pad_x = size - img.shape[1]
    pad_y = size - img.shape[0]
    pad_l = pad_x // 2
    pad_t = pad_y // 2
    img = np.pad(img, ((pad_t, pad_y - pad_t), (pad_l, pad_x - pad_l), (0, 0)), mode='constant', constant_values=255)
    interp = cv2.INTER_AREA if size > IMAGE_SIZE else cv2.INTER_LANCZOS4
    img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE), interpolation=interp)
    image = np.expand_dims(img, 0)
    image = image.astype(np.float32)
    return image

def predict(
            i
            ,t_name:str
            ,general_threshold: float
            ,tag_names: list[str]
            ,general_indexes: list[np.int64]
            ,model
            ):
    image = img_proc(i)
    model_pred(
                image
                ,t_name
                ,general_threshold
                ,tag_names
                ,general_indexes
                ,model
                )
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, default=None, help="File Path")
    parser.add_argument("--gen_thresh", type=float, default=0.35, help="General Tags Threshold - default: 0.35")
    parser.add_argument("--model_name", type=str, default="ViT", help="MOAT,SwinV2,ConvNext,ConvNextV2,ViT - default:ViT")
    parser.add_argument("--list_gen", type=str, default="list", help="[WALK] - all files in subdirs, [LIST] all files in ListDir directory - default: LIST")
    args = parser.parse_args()
    file_list=[]
    file_path = args.file_path
    file_path = file_path.replace(chr(92),"/")
    if file_path[-1:] != "/":
        file_path = file_path+"/"
    cp_g("File Path: ")
    cp_y(str(file_path))
    print("")
    model_name = str(args.model_name).lower()
    cp_g("Model Name: ")
    cp_y(str(model_name))
    print("")
    img_types = [str(f).replace('.','') for f,u in Image.registered_extensions().items()]
    cp_g("General Tags Threshold: ")
    cp_y(str(args.gen_thresh))
    print("")
    list_gen = str(args.list_gen).lower()
    cp_g("File List Gen: ")
    cp_y(str(list_gen).lower())
    print("")
    print("")
    if list_gen == "walk":
        for r, d, f in os.walk(file_path[:-1:]):
            for file in f:
                if ((file[-(file[::-1].find('.')):]).lower()) in img_types:
                    file_list.append(os.path.join(r, file))
    elif list_gen == "list":
        file_list = [file_path+f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) \
                    and f[-(f[::-1].find('.')):] in[str(f).replace('.','') \
                    for f,u in Image.registered_extensions().items()]]
    tag_names, general_indexes = load_labels()
    if model_name == "moat":
        model = load_model(MOAT_MODEL_REPO, MODEL_FILENAME)
    elif model_name == "swinv2":
        model = load_model(SWIN_MODEL_REPO, MODEL_FILENAME)
    elif model_name == "convnext":
        model = load_model(CONV_MODEL_REPO, MODEL_FILENAME)
    elif model_name == "convnextv2":
        model = load_model(CONV2_MODEL_REPO, MODEL_FILENAME)
    elif model_name == "vit":
        model = load_model(VIT_MODEL_REPO, MODEL_FILENAME)
    l_bar='{desc}: {percentage:3.0f}%|'
    r_bar='| {n_fmt}/{total_fmt} [elapsed: {elapsed} / Remaining: {remaining}] '
    bar = '{rate_fmt}{postfix}]'
    with ThreadPoolExecutor(8) as executor:       
        status_bar = tqdm(total=len(file_list), desc='Image_Tagging',bar_format=cp_c(f'{l_bar}{bar}{r_bar}'),colour='#6495ED')
        futures = [
            executor.submit(
                predict
                ,i
                ,i[:(len(i))-1-len(i[-(i[::-1].find('.')):])]+".txt" 
                ,args.gen_thresh
                ,tag_names
                ,general_indexes
                ,model
                )
            for i in file_list]
        for _ in as_completed(futures):
            status_bar.update(n=1)
        status_bar.close()

if __name__ == "__main__":
    main()
