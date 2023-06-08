#https://github.com/gurugaurav/bing_image_downloader
# MIT License

# Copyright (c) 2020 Guru Prasad Singh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

img_types = [ str(f).replace('.','') for f,u in Image.registered_extensions().items()]

vid_types = ["gif","gifv","m4v","mkv","mpg","mpeg","mp4","avi","wmv","mov","webm","mp2","mpe","mpv","qt","m4p","avchd","ogg"]

@dataclass
class CFG:
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

class Bing:
    def __init__(self, config: CFG):
        try:
            with open("error_log.txt","w") as fi:
                fi.write("start\n")
            self.config = config
            self.download_count = self.config.limit
            self.output_dir = self.config.output_dir
            self.adult = self.config.adult_filter
            self.filter = self.config.filter
            self.timeout = self.config.timeout
            self.query = str(self.config.query).replace(chr(32),chr(43))
            self.limit = self.config.limit
            self.filter = self.config.filter
            self.cust_w = self.config.cust_w
            self.cust_h = self.config.cust_h
            self.page_counter = 0
            self.page_counter = 0
            self.download_count = 0
            self.headers = {'User-Agent': "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.6) Gecko/20040206 Firefox/0.8",
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            'Accept-Encoding': 'none',
                            'Accept-Language': 'en-US,en;q=0.8',
                            'Connection': 'keep-alive'}
            alpha_whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_+') 
            clean_query = []
            clean_query = [''.join(l for l in x+" " if l in alpha_whitelist) for x in self.query.replace(chr(32),chr(95))]
            query_sanitized = ""
            for x in clean_query:
                query_sanitized = query_sanitized + x
            print(re.sub(r'[^A-Za-z0-9_+]+/g','', str(query_sanitized)))
            self.image_dir = Path(self.output_dir[:-1:]).joinpath(re.sub(r'[^A-Za-z0-9_ ]+/g','', str(query_sanitized).replace(chr(32),chr(95)))).absolute()
            try:
                if not Path.is_dir(self.image_dir):
                    Path.mkdir(self.image_dir, parents=True)
            except Exception as e:
                print('[Error]Failed to create directory.', e)
                sys.exit(1)
            cprint("[%] Downloading Images to {}".format(str(self.image_dir.absolute())),"blue")
            self.seen = set([f[:(len(f))-len(f[-(f[::-1].find('.')):])] \
                            for f in os.listdir(str(self.image_dir)) \
                                if os.path.isfile(str(self.image_dir)+f) \
                                    and f[-(f[::-1].find('.')):] in img_types])
            self.run()
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            logging.error(traceback.format_exc())
            with open("error_log.txt","a") as fi:
                fi.write(str(logging.error(traceback.format_exc())))
        finally:
            pass

    def save_image(self, link):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            request = urllib.request.Request(link[0], None, self.headers)
            image = urllib.request.urlopen(request, timeout=self.timeout, context=ctx).read()
            cprint("[!] Request-Get!","red")
            if not imghdr.what(None, image):
                print(f"[Error]Invalid image, not saving {link[0]}\n")
                raise ValueError(f"[Error]Invalid image, not saving {link[0]}\n")
            md5_calc = hashlib.md5(image).hexdigest()
            cprint(md5_calc,"green")
            img_buf = BytesIO(image)
            if link[0][-(link[0][::-1].find('.')):] in img_types and link[0][-(link[0][::-1].find('.')):] not in vid_types:
                img = Image.open(img_buf).convert("RGB")
                img.save(f"{self.image_dir}/{str(md5_calc)}.jpg", "JPEG", quality=95)
                cprint(f"[!!] ACTUAL SAVE GET:\n{str(self.image_dir).replace(chr(92),chr(47))}/{md5_calc}.jpg","blue")
                with open(f"{self.image_dir}/{str(md5_calc)}.txt", 'w') as f:
                    f.write(str(link[1]))
                self.download_count = self.download_count + 1
                return           
            elif link[0][-(link[0][::-1].find('.')):] in vid_types:
                    img_byte_array = bytearray(image)
                    with open(f"{self.image_dir}/{str(md5_calc)}.{link[0][-(link[0][::-1].find('.')):]}", 'wb') as f:
                        x = f"{self.image_dir}/{str(md5_calc)}.{link[0][-(link[0][::-1].find('.')):]}"
                        f.write(img_byte_array)                
                    with open(f"{self.image_dir}/{str(md5_calc)}.txt", 'w') as f:
                        f.write(str(link[1]))                  
                    vidcap = cv2.VideoCapture(f"{self.image_dir}/{str(md5_calc)}.{link[0][-(link[0][::-1].find('.')):]}",)
                    success,image = vidcap.read()
                    count = 0
                    while success:
                        try:
                            if not Path.is_dir(Path(f"{str(self.image_dir)}/{str(md5_calc)}")):
                                Path.mkdir(Path(f"{self.image_dir}/{str(md5_calc)}"), parents=True)                             
                            cv2.imwrite(f"{self.image_dir}/{str(md5_calc)}/{str(md5_calc)}_{count}.jpg", image)
                            success,image = vidcap.read()
                            count += 1
                        except KeyboardInterrupt:
                            sys.exit()
                        except Exception as e:
                            logging.error(traceback.format_exc())
                            with open("error_log.txt","a") as fi:
                                fi.write(str(logging.error(traceback.format_exc())))
                        finally: pass
                    for i in range (0,count):
                        with open(f"{self.image_dir}/{str(md5_calc)}/{str(md5_calc)}_{count}.txt", 'w') as f:
                            f.write(str(link[1]))  
                    self.download_count = self.download_count + 1
                    count = 0
                    return
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            logging.error(traceback.format_exc())
            with open("error_log.txt","a") as fi:
                fi.write(str(logging.error(traceback.format_exc())))
        finally:
            pass
    
    def download_image(self, link):
        self.download_count += 1
        try:
            self.save_image(link)
            print("[%] File Downloaded !\n")
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            logging.error(traceback.format_exc())
            with open("error_log.txt","a") as fi:
                fi.write(str(logging.error(traceback.format_exc())))
    
    def html_request_gen(self,page_counter):
        self.pg_count = self.page_counter * 35
        f_wh_cust = f"+filterui:imagesize-custom_{self.cust_w}_{self.cust_h}+"
        f_hw_cust = f"+filterui:imagesize-custom_{self.cust_h}_{self.cust_w}+"
        self.query = self.query.replace(chr(32),chr(95))
        rq_wh_url = f"https://www.bing.com/images/async?q={str(self.query)}&first={self.pg_count}&count={str(self.limit)}&adlt={self.adult}&qft={self.filter}{f_wh_cust}"
        rq_hw_url = f"https://www.bing.com/images/async?q={str(self.query)}&first={self.pg_count}&count={str(self.limit)}&adlt={self.adult}&qft={self.filter}{f_hw_cust}"
        return [rq_wh_url,rq_hw_url]

    def link_list_gen(self,html):
        try:
            link_list = []
            link_list.clear()          
            links = re.findall('url&quot;:&quot;(.*?)&quot;}"', html)
            for link in links:
                link = link + r"&quot;}"
                s_link = re.findall(r"murl&quot;:&quot;(.*?)&quot",link)[0]
                tags_1 = bytes(re.findall(r"&quot;,&quot;t&quot;:&quot;(.*?)&quot;,&quot",link)[0],'utf-8')
                tags_1 = codecs.decode(unicodedata.normalize('NFKD', codecs.decode(tags_1)).encode('ascii', 'ignore'))
                tags_1 = re.sub(r'[^A-Za-z0-9_ ]+/g','', str(tags_1))
                tags_2 = bytes(re.findall(r"desc&quot;:&quot;(.*?)&quot;}",link)[0],'utf-8')
                tags_2 = codecs.decode(unicodedata.normalize('NFKD', codecs.decode(tags_2)).encode('ascii', 'ignore'))
                tags_2 = re.sub(r'[^A-Za-z0-9_ ]+/g','', str(tags_2))
                tags = tags_1 + chr(32) + tags_2
                tags = tags.replace(
                                    "respond","").replace(
                                    "comment","").replace(
                                    "related","").replace(
                                    "posts","").replace(
                                    "flags","").replace(
                                    "notes","").replace(
                                    "edit","").replace(
                                    "...","")
                link_list.append([s_link, tags])                
            link_list = [x for x in link_list]
            self = link_list
            return self
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            logging.error(traceback.format_exc())
            with open("error_log.txt","a") as fi:
                fi.write(str(logging.error(traceback.format_exc())))
        finally:
            pass

    def html_gen(self,page_counter):
        try:
            self.page_counter = page_counter
            ret_link_list = []
            ret_link_list.clear()
            request_list = []
            request_list.clear()
            sleep(1)
            request_list = self.html_request_gen(self.page_counter)
            link_list = []        
            for request_url in request_list:
                link_list.clear()
                sleep(3)
                request = urllib.request.Request(request_url, None, headers=self.headers)
                response = urllib.request.urlopen(request, context=self.ctx)
                html = response.read().decode('utf8')
                if html ==  "":
                    print("[%] No more images are available")
                    break
                ret_link_list = self.link_list_gen(html)
                ret_link_list = [link_list.append(x) for x in ret_link_list]
            return link_list
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            logging.error(traceback.format_exc())
            with open("error_log.txt","a") as fi:
                fi.write(str(logging.error(traceback.format_exc())))
        finally:
            pass

    def run(self):
        try:
            self.ctx = ssl.create_default_context()
            self.ctx.check_hostname = False
            self.ctx.verify_mode = ssl.CERT_NONE
            self.page_counter = 1
            while True:
                try:
                    cprint(f"\n\n[!!]Indexing page: {self.page_counter}\n","yellow")
                    link_list = []
                    link_list.clear()
                    link_list = self.html_gen(self.page_counter)
                    link_list = [x for x in link_list if x[0] not in self.seen]
                    cprint(f"[%] Indexed {len(link_list)} Images on Page {self.page_counter + 1}","green")
                    cprint("\n===============================================\n","yellow")
                    try:
                        with concurrent.futures.ThreadPoolExecutor(3) as executor:
                            executor.map(self.download_image, link_list)
                        for link in link_list:
                            if self.download_count < self.limit and link[0] not in self.seen:
                                self.seen.add(str(link[0]))
                    except KeyboardInterrupt:
                        sys.exit()
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        with open("error_log.txt","a") as fi:
                            fi.write(str(logging.error(traceback.format_exc())))
                        pass
                    finally:
                        pass                                   
                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e:
                    logging.error(traceback.format_exc())
                    with open("error_log.txt","a") as fi:
                        fi.write(str(logging.error(traceback.format_exc())))
                    pass
                finally:
                    pass                            
                self.page_counter = self.page_counter + 1
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            logging.error(traceback.format_exc())
            with open("error_log.txt","a") as fi:
                fi.write(str(logging.error(traceback.format_exc())))
        finally:
            pass

Bing(config=CFG)

