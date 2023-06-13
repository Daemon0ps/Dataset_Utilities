# Bing_Downloader_with_Tags

download bing images by keyword(s), and save titles/meta data as .txt files
Also extracts keyframes from video files

## Prerequisites

```
import numpy as np
import hashlib
import ssl
from pathlib import Path
import urllib.request
import urllib
import imghdr
import re
import logging
import traceback
import os, sys
from pathlib import Path
import concurrent.futures
from io import BytesIO
from PIL import Image
import codecs
from time import sleep
from random import randint
import unicodedata
from dataclasses import dataclass
from termcolor import cprint
import cv2
```

### Options

```
    query: str = f"Steampunk Portraits"
    output_dir: str = "p:/bing/" #yes, put the slash at the end
    adult_filter: str = "off" # or "on"
    timeout: int = 10
    filter: str = ""
                # "+filterui:photo-animatedgif"
                # "+filterui:photo-photo"
                # "+filterui:photo-linedrawing"
                # "+filterui:photo-photo"4
                # "filterui:photo-clipart"
                # "+filterui:photo-animatedgif"
                # "+filterui:photo-transparent"
    limit: int = 1000
    cust_w = 576 # Custom Width Filter
    cust_h = 640
     # Custom Width Filter
```
