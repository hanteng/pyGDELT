#!/usr/bin/env python
# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
# Filename: GDELT_easy.py

import os.path
import numpy as np
import csv
import pandas as pd

def list_current_data_files(path_this):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [ f for f in listdir(path_this) if isfile(join(path_this,f)) ]
    return onlyfiles

def import_from_csv(im_filename,index_col=False, sep=',', **kwargs):
    import csv
    return pd.io.parsers.read_csv(im_filename, index_col=index_col, sep=sep, encoding='utf-8', **kwargs)

def export_to_csv(df, ex_filename, sep=','):
    if sep==',':
        df.to_csv(ex_filename, sep=sep, quoting=csv.QUOTE_ALL, na_rep='{na}', encoding='utf-8')  #+'.csv'
    if sep=='\t':
        df.to_csv(ex_filename, sep=sep, quoting=csv.QUOTE_NONE, na_rep='{na}', encoding='utf-8')  #+'.tsv'  , escapechar="'", quotechar=""

##Dictionary of codebooks
##The constructor by default uses the flattened and shortened field names as keys to the dictionaries of Notes and original names of the Fields.
##Orginal fieldnames lookup: e.g. dict_meta['Fields']['ti_id']  produces GlobalEventID
##Orginal fieldnames lookup: e.g. dict_meta['Fields']['ti_y'] produces Year
##Orginal Notes lookup: e.g. dict_meta['Fields']['ti_y'] produces "(integer) Alternative formatting of the event date, in YYYY format."
def dict_meta_constructor(df_meta, column_key=0):
    key=[]
    value=[]
    columns_list=df_meta.columns.tolist()
    fieldname_key=columns_list[column_key]  # 0 -->'flattened_shortened'
    for i,column_name in enumerate(columns_list):
        if i==column_key:
            pass
        else:
            key.append(column_name)
            value.append(df_meta.set_index(fieldname_key)[column_name].to_dict())
    dict_outcome=dict(zip(key,value))
    return dict_outcome


# ==PREPARING==
# ====download location: by default the sister folder "data" to the current script folder====
path_local_script = os.path.dirname(os.path.realpath(__file__))
path_local_data = os.path.abspath(os.path.join(path_local_script, os.pardir, "data"))

def path_script():
    global path_local_script
    return path_local_script

def path_data():
    global path_local_data
    return path_local_data

def load_meta(fn="GDELT_meta.tsv"):
    # ===load meta data information information for the GDELT dataset===
    # meta data information is scraped from Philip A. Schrodt's "CAMEO Conflict and Mediation Event Observations Event and Actor Codebook"
    # filename: CAMEO.Manual.1.1b3.pdf
    df_meta=import_from_csv(os.path.join(path_local_script,fn), sep='\t', header=0)         
    dict_meta=dict_meta_constructor(df_meta, column_key=df_meta.columns.get_loc(u'flattened_shortened'))
    return df_meta,dict_meta

def load(path=path_local_data, fn="GDELT_working.tsv", column_key=0):
    fn_df_working = os.path.join(path_local_data, fn)
    if not os.path.exists(path_local_data):
        print ">>Data folder does not exist yet...please run GDELT_data_download.py first"
    else:
        if not os.path.exists(fn_df_working):
            print ">>Data file {0}, is expected but does not exist".format(fn_df_working)
        else:
            meta_df, meta_dict=load_meta()
            
            list_flattened_shortened=meta_df['flattened_shortened'].tolist()
        
 
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
                        u'ac_geo_lat': np.float32,
                        u'ac_geo_long': np.float32,
                        u'da_dateadded': np.int32,
                        u'da_sourceurl': np.dtype((str, 255))            
                        }
            print ">>Data file {0}, is expected and loaded now".format(fn_df_working)
            df_working=import_from_csv(fn_df_working, sep='\t', header=0, parse_dates = ['ti_d'], infer_datetime_format= True, na_values=["{na}"])      #, , dtype =dict_dtype   
            
    return df_working
