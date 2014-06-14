#!/usr/bin/env python
# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import os.path
import numpy as np
import csv

def list_current_data_files(path_this):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [ f for f in listdir(path_this) if isfile(join(path_this,f)) ]
    return onlyfiles

def import_from_csv(im_filename,index_col=False, sep=',', **kwargs):
    import csv
    import pandas as pd
#    return pd.DataFrame.from_csv(im_filename, index_col=index_col, sep=sep, encoding='utf-8', **kwargs)
    return pd.io.parsers.read_csv(im_filename, index_col=index_col, sep=sep, encoding='utf-8', **kwargs)

def export_to_csv(df, ex_filename, sep=',', **kwargs):
    if sep==',':
        df.to_csv(ex_filename, sep=sep, quoting=csv.QUOTE_ALL, na_rep='{na}', encoding='utf-8', **kwargs)  #+'.csv'
    if sep=='\t':
        df.to_csv(ex_filename, sep=sep, quoting=csv.QUOTE_NONE, na_rep='{na}', encoding='utf-8', **kwargs)  #+'.tsv'  , escapechar="'", quotechar=""

##Dictionary of codebooks
##The constructor by default uses the flattened and shortened field names as keys to the dictionaries of Notes and original names of the Fields.
##Orginal fieldnames lookup: e.g. dict_meta['Fields']['ti_id']  produces GlobalEventID
##Orginal fieldnames lookup: e.g. dict_meta['Fields']['ti_y'] produces Year
##Orginal Notes lookup: e.g. dict_meta['Fields']['ti_y'] produces "(integer) Alternative formatting of the event date, in YYYY format."
def dict_meta_constructor(df, column_key=0):
    key=[]
    value=[]
    columns_list=df.columns.tolist()
    fieldname_key=columns_list[column_key]  # 0 -->'flattened_shortened'
    for i,column_name in enumerate(columns_list):
        if i==column_key:
            pass
        else:
            key.append(column_name)
            value.append(df_meta.set_index(fieldname_key)[column_name].to_dict())
    dict_outcome=dict(zip(key,value))
    return dict_outcome


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
    print ">>Data folder exists, with csv files including"
    files_data_existing_csv=[fn for fn in list_current_data_files(path_local_data) if fn[-4:].lower()==".csv"]
    print ">>>", files_data_existing_csv

# ===load meta data information information for the GDELT dataset===
# meta data information is scraped from Philip A. Schrodt's "CAMEO Conflict and Mediation Event Observations Event and Actor Codebook"
# filename: CAMEO.Manual.1.1b3.pdf
df_meta=import_from_csv(os.path.join(path_local_script,"GDELT_meta.tsv"), sep='\t', header=0)         
dict_meta=dict_meta_constructor(df_meta, column_key=df_meta.columns.get_loc(u'flattened_shortened'))

df_list=[]
# loading the freshly extracted files
list_flattened_shortened=df_meta['flattened_shortened'].tolist()

#the following two lines need debugging with data
#list_dtype=[eval(x) for x in df_meta['dtype'].tolist()]
#dict_dtype1=dict(zip(list_flattened_shortened,list_dtype))
#print dict_dtype1

dict_dtype={u'ti_id': np.int32,
            u'ti_d': np.int32,
            u'ti_my': np.int32,
            u'ti_y': np.int32,
            u'ti_f': np.float64,
            u'a1_knowngroup': np.dtype((str, 16)),
            u'a2_knowngroup': np.dtype((str, 16)),
            u'a1_type1': np.dtype((str, 16)),
            u'a1_type2': np.dtype((str, 16)),
            u'a1_type3': np.dtype((str, 16)),
            u'a2_type1': np.dtype((str, 16)),
            u'a2_type2': np.dtype((str, 16)),
            u'a2_type3': np.dtype((str, 16)),
            u'a1_religion1': np.dtype((str, 255)),
            u'a1_religion2': np.dtype((str, 255)),
            u'a2_religion1': np.dtype((str, 255)),
            u'a2_religion2': np.dtype((str, 255)),
            u'a1_ethnic': np.dtype((str, 16)),
            u'a2_ethnic': np.dtype((str, 16)),
            u'da_dateadded': np.int32,
            u'da_sourceurl': np.dtype((str, 255))            
            }
#degugging 
#print dict_dtype


## Getting geography data: using "country" to filter actor1 actor2 and action
#fields_country=[x for x in df_meta['flattened_shortened'].tolist() if 'country' in x]
#fields_country_adm=[x for x in df_meta['flattened_shortened'].tolist() if 'country' in x or 'adm' in x]
#df_list[0][fields_country][:3]


for i, fn in enumerate(files_data_existing_csv,start=1):
    df=import_from_csv(os.path.join(path_local_data,fn), sep='\t', header=None, names=df_meta['flattened_shortened'].tolist(), parse_dates = ['ti_d'], infer_datetime_format= True, dtype=dict_dtype)

    # select only CHN
    df=df[(df['a1_country'] =='CHN') & (df['a2_country'] =='CHN')]
    if i==1:
        df_sel=df
    else:
        df_sel=df_sel.append(df,ignore_index=True)

export_to_csv(df_sel, ex_filename=os.path.join(path_local_data, "GDELT_working.tsv"), sep='\t', index=False)
