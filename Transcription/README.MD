# Whisper Transcription

Uses OpenAI Whisper to transcribe, saves to .TXT / .JSON

## Prerequisites

```
CUDA

import os
import whisper
import torch
from unidecode import unidecode
import codecs
import unicodedata
import json
from tqdm import tqdm
```

### Options

Set your model, file path, save path, and choose the file types to parse

```
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
    model = whisper.load_model(
                                tr_model[8]
                                ,device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

file_path = "P:/documents/av/"
save_path = "P:/documents/av/"
# file_types = ['mp3','mp4','mkv']
file_types = ['aac']
