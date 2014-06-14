#!/usr/bin/env python
# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import os.path
def list_current_data_files(path_this):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [ f for f in listdir(path_this) if isfile(join(path_this,f)) ]
    return onlyfiles

def extract_file(_path, _fn):
    from zipfile import ZipFile
    try:
        with ZipFile(file=os.path.join(_path,_fn), mode='r') as z:   
            info = z.extractall(os.path.join(_path,''))
            print ">>>Succesfully extracted: "+'\t'.join('{}---{}'.format(*k) for k in enumerate(z.namelist(),start=1))
        return z.namelist()
    except:
        print '>>>ERROR: remove the downloaded file {0} and try again'.format(_fn)

###MAIN###

# ==PREPARING==
# ====download location: by default the sister folder "data" to the current script folder====
path_local_script = os.path.dirname(os.path.realpath(__file__))
path_local_data = os.path.abspath(os.path.join(path_local_script, os.pardir, "data"))
print ">>Current script folder:{0}".format(path_local_script)
print ">>Default data folder:{0}".format(path_local_data)
if not os.path.exists(path_local_data):
    print ">>Data folder does not exist yet...please run GDELT_data_download.py first"
else:
    print ">>Data folder exists, including"
    files_data_existing=list_current_data_files(path_local_data)
    print ">>>", files_data_existing

# ====file lists====
file_list_2extract = [item for item in files_data_existing if item[-4:]==".zip"]
print ">>Number of files to be extracted: {0}, including...".format(len(file_list_2extract))
print ">>>", file_list_2extract

for fn in file_list_2extract:
    extract_file(path_local_data, fn)

