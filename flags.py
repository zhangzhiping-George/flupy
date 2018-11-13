import os
import sys
import time

import requests

'''
get_flag: request.get
save_flag: f.write('flags')
show_flag: print(cc), print flag name
download_many: for cc in cc_list: get_flag()
'''
cc_list= ('CN IN US ID BR PK NG BD RU '
'JP MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags/'
DEST_DIR = 'flags/'

def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename) 
    with open(path, 'wb') as f: 
        f.write(img)

def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content
    #save flags to <path>
    #path = os.path.join(DEST_DIR, cc.lower() + '.gif') 
    #with open(path, 'wb') as f: 
    #    f.write(resp.content)

def show_flag(text):
    print(text, end='=\n') 
    #sys.stdout.flush()

def download_many(cc_list):
    for cc in  sorted(cc_list):
       image = get_flag(cc) 
       show_flag(cc)
       save_flag(image, cc.lower() + '.gif')
    return len(cc_list)

def main(download_many):
    t0 = time.time() 
    count = download_many(cc_list) 
    elapsed = time.time() - t0
    print('{} flags downloaded in {:.2f}s'.format(count, elapsed))
    

if __name__ == '__main__':
    main(download_many)
