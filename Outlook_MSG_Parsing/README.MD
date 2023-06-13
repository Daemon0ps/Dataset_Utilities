# Outlook MSG File Parsing to MS-SQL Database

Still a Work In Progress. Had to organize about 10k emails real quick, and this helped categorize.
```
To do:
	NLP Summarizations
	Chronological MatPlot Graphs/Charts
	Social Networking Node Analysis
```

## Getting Started

You will need access to an instance of MS-SQL. This uses PYODBC to insert information into MS-SQL Tables.

### Prerequisites

What things you need to install the software and how to install them

```
import re
import traceback
import logging
import extract_msg
import numpy as np
import pandas as pd
import keyring
import tqdm
import pyodbc
import cv2
import hashlib
import codecs
import os,sys
import re
import string
import pypdfium2 as pdfium
import json
import matplotlib
import nltk
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from outlook_msg import Message
from termcolor import cprint
from PIL import Image,ImageOps,ImageFile
from traceback_with_variables import activate_by_import
from concurrent.futures import ThreadPoolExecutor, as_completed
from unidecode import unidecode
from datetime import datetime as dt, timedelta as td
from colormod import *
from io import BytesIO
nltk.download('stopwords')
nltk.download('punkt')
ImageFile.LOAD_TRUNCATED_IMAGES = True
from time import sleep
from timeit import timeit
import spacy
from spacy import displacy
from spacy import tokenizer
nlp = spacy.load('en_core_web_sm')
```

### MS-SQL Tables

Create a database called emails, or, whatever you want.

```
create table 
	email(
		[email] uniqueidentifier not null default newid()
		,[filename] varchar(255) null
		,[file_id] varchar(32) null
		,[date] varchar(14) null
		,[msg_class] varchar(32) null
		,[body_md5] varchar(32) null
		,[body] varchar(max) null
		,[all_uniques_pk] varchar(36) not null default newid()
		,[unique_words_pk] varchar(36) not null default newid()
		,[phone_numbers_pk] varchar(36) not null default newid()
		,[email_addresses_pk] varchar(36) not null default newid()
		,[sender] varchar(200) null
		,[to] varchar(500) null
		,[message_id] varchar(2048) null
		,[header] varchar(max) null
		,[subject] varchar(1024) null
		,[cc] varchar(1024) null
		,[bcc] varchar(1024) null
		,[attachments_pk] varchar(36) not null default newid()
		,[named_entities_pk] varchar(36) not null default newid()
	)
create table all_uniques(
		[all_uniques] uniqueidentifier not null default newid()
		,[email] varchar(36)
		,[word] varchar(100)
	)
create table
	unique_words(
		[unique_words] uniqueidentifier not null default newid()
		,[email] varchar(36)
		,[word] varchar(100)
	)
create table
	phone_numbers(
		[phone_numbers] uniqueidentifier not null default newid()
		,[email] varchar(36)
		,[phone_no] varchar(100)
	)
create table
	email_addresses(
		[email_addresses] uniqueidentifier not null default newid()
		,[email] varchar(36)
		,[email_address] varchar(100)
	)
create table 
	attachments(
		[attachments] uniqueidentifier not null default newid()
		,[email] varchar(36)
		,[attachment] varchar(100)
	)
create table
	named_entities(
		[named_entities] uniqueidentifier not null default newid()
		,[email] varchar(36)
		,[type] varchar(100)
		,[entity] varchar(1024)
	)
```
run the python binary
```
>>>import keyring
>>>username = keyring.set_password("lgl","user","MSSQL_USERNAME")
>>>password = keyring.set_password("lgl","pass","MSSQL_PASSWORD")
>>>server = keyring.set_password("lgl","srv","70.85.67.75:31337")
>>>database = keyring.set_password("lgl","db","MSSQL_DATABASE")
```
DO NOT SAVE THIS AS PLAINTEXT.

Edit the script for what you chose:
```
username = keyring.get_password("lgl","user")
password = keyring.get_password("lgl","pass")
server = keyring.get_password("lgl","srv")
database = keyring.get_password("lgl","db")
```

For Linux users, you CAN run keyring headless(WSL/etc):
```
DaemonOps@hostname:/home$ sudo apt install gnome-keyring
DaemonOps@hostname:/home$ dbus-run-session -- sh
$ ./home/username/miniconda3/envs/outlook_msg_sql/bin/python
>>> import keyring
>>> keyring.get_keyring()
<keyring.backends.SecretService.Keyring object at 0x0c0c0c0c0c0c>
>>> #if you see the object above, keyring should be good to go
>>>#you can also run with bash -c 'dbus-run-session -- sh; echo 'the_secret_password_is_squeemish_ossifrage' | gnome-keyring-daemon --unlock; /home/user/miniconda3/envs/outlook_msg_sql/bin/python /home/user/outlook_msg_sql/outlook_msg_parse_to_mssql.py
```
