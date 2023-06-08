import sys
import ssl
import urllib.request
import urllib
from time import sleep
from random import randint
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
save_path = "/mnt/t/save_to_path/"
headers = {'User-Agent': "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.6) Gecko/20040206 Firefox/0.8",
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


base_url = "https://yb.cmcdn.com/yearbooks/a/c/e/7/ace7696d4fa5b0db2a90fe8eff8422a3/1100/" #ihs1997 Irvine High School
# base_url = "https://yb.cmcdn.com/yearbooks/5/b/9/0/5b902c7d5d4a1dcbec3f8a76892c0e6a/1100/" #ihs1998 Irvine High School
# base_url = "https://yb.cmcdn.com/yearbooks/a/c/e/7/ace7696d4fa5b0db2a90fe8eff8422a3/1100/" #ihs1999 Irvine High School
# base_url = "https://yb.cmcdn.com/yearbooks/2/d/2/6/2d26f181bc108175adef7fb0714b8878/1100/" #ihs2000 Irvine High School

def yb_img(i):
    try:
        sleep(randint(10,15))
        req_url = base_url + str(i).zfill(4) + ".jpg"
        request = urllib.request.Request(req_url, None, headers=headers)
        response = urllib.request.urlopen(request, context=ctx)
        url_file = response.read()
        with open(save_path+str(i).zfill(4) + ".jpg","wb") as fi:
            fi.write(url_file)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
    finally: pass
status_bar = tqdm(total=500, desc='yb_img')

def main():
    try:
        with ThreadPoolExecutor(8) as executor:
            futures = [executor.submit(yb_img, i) for i in range(1,500)]
            for _ in as_completed(futures):
                status_bar.update(n=1)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
    finally: pass


try:
    main()
except KeyboardInterrupt:
    sys.exit()
except Exception as e:
    print(e)
    pass
finally: pass
