#!/usr/bin/env python
# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import os.path
import requests
import lxml.html as html
from urlparse import urljoin
from urlparse import urlparse

def list_current_data_files(path_this):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [ f for f in listdir(path_this) if isfile(join(path_this,f)) ]
    return onlyfiles
    
# ==DOWNLOADING==
def download_file(_file_list, _url_path, _local_path):
    for fn in _file_list:
        url_2download = urljoin(_url_path, fn)
        r = requests.get(url_2download, stream=True)
        print ">>Try downloading {0} to {1}...".format(url_2download,_local_path)
        with open(os.path.join(_local_path,fn), 'wb') as foutput:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    foutput.write(chunk)
                    foutput.flush()
        if r.status_code==200:
            print ">>>Succesfully downloaded: {0}".format(fn)
        else:
            print ">>>Issue: http request status code ({0}){1}".format(r.status_code,fn)


###MAIN###

# ==PREPARING==
# ===start to get the latest file list from the GDELT project===
url_start='http://data.gdeltproject.org/events/index.html'
datafile_list = requests.get(url_start)
link_list = html.fromstring(datafile_list.content).xpath("//li/a/@href")

# ===choose your choice of files===
# for those with filename begins with four digits (years).===
file_list = [x for x in link_list if str.isdigit(x[0:4])]
# ====one example: filter the data file list by time periods====
file_list = [f for f in file_list if f[0:8]<="20140605" and f[0:8]>="20140504"]
print ">>Number of files required for the selected time period: {0}, including...".format(len(file_list)) 
print ">>>",file_list
# ====download location: by default the sister folder "data" to the current script folder====
path_local_script = os.path.dirname(os.path.realpath(__file__))
path_local_data = os.path.abspath(os.path.join(path_local_script, os.pardir, "data"))
print ">>Current script folder:{0}".format(path_local_script)
print ">>Default data folder:{0}".format(path_local_data)
if not os.path.exists(path_local_data):
    print ">>Data folder does not exist yet...creating one"
    os.makedirs(path_local_data)
    files_data_existing=[]
else:
    print ">>Data folder exists, including"
    files_data_existing=list_current_data_files(path_local_data)
    print ">>>", files_data_existing

# ====file lists====
file_list_2download = [item for item in file_list if item not in files_data_existing]
print ">>Number of files to be downloaded: {0}, including...".format(len(file_list_2download))
print ">>>", file_list_2download

download_file(file_list_2download, url_start, path_local_data)

    
