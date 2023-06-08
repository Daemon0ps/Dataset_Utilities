import os
import whisper
import torch
from unidecode import unidecode
import codecs
import unicodedata
import json
from tqdm import tqdm


tr_model = [
                'tiny.en',  #0
                'tiny',     #1
                'base.en',  #2
                'base',     #3
                'small.en', #4
                'small',    #5
                'medium.en',#6
                'medium',   #7
                'large'     #8
            ]

print(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
cuda_check = str(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
assert cuda_check == str("cuda")

def audio_transcribe(file_path:str, save_path:str, f:str):
    print(file_path+f)
    model = whisper.load_model(
                                tr_model[8]
                                ,device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    print(f)
    result = model.transcribe(
                                file_path+f,
                                verbose=True,
                                compression_ratio_threshold=1.4,
                                condition_on_previous_text=False,
                                temperature=0.8,
                                word_timestamps=False
                            )
    f_name = str(f).replace(f[-(f[::-1].find('.')):],'')+".json"
    txt_data = []
    res_dict = dict(result)
    res_segments = res_dict['segments']
    for segment in res_segments:
        text_res = str('')
        segment = dict(segment)
        text_res = text_res + str(f"[{str(float(segment['start']))}-{str(float(segment['end']))}]: {str(codecs.decode(unicodedata.normalize('NFKD', codecs.decode(bytes(segment['text'],encoding='utf-8'))).encode('ascii', 'ignore')))}")+str('\n')
        txt_data.append(text_res)
    print("saving json")
    with open(save_path+f_name,"wt") as fi:
        fi.write(json.dumps(result,indent=4,ensure_ascii=True))
    print("saving txt")
    f_name = str(f).replace(f[-(f[::-1].find('.')):],'')+".txt"
    with open(save_path+f_name,"wt") as fi:
        for tr in txt_data:
            fi.write(tr)     

file_path = "P:/documents/av/"
save_path = "P:/documents/av/"
# file_types = ['mp3','mp4','mkv']
file_types = ['aac']
all_files = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) and f[-(f[::-1].find('.')):] in file_types]
files = [file for file in all_files if file[:(len(file))-1-len(file[-(file[::-1].find('.')):])]+".txt" not in all_files]

for f in tqdm(all_files):
    audio_transcribe(file_path, save_path, f)

# text_files = [f for f in os.listdir(file_path[:-1:]) if os.path.isfile(file_path+f) and f[-(f[::-1].find('.')):] in ['txt']]

# for tf in text_files:
#     with open(file_path+tf,"rt") as fi:
#         segment_list = fi.readlines()
#     segment_parse = [
#                     [str(re.findall("[\[]{1}(.*?\d)[\]]{1}",str(x))),
#                     str(re.findall("[]][ ]{2}(.*?)[\n]",str(x)))
#                     ] for x in segment_list]
#     for x in segment_parse:
#             fi.write(x[0])
#             fi.write(x[1])    
#     with open(file_path+tf,"wt") as fi:
#         for x in segment_parse:
#             fi.write(x[0])
#             fi.write(x[1])
