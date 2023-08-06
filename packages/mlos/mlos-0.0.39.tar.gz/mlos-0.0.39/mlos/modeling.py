
import os
import pickle
import numpy as np
import pandas as pd
import json
import sys
import os
import requests
import mlos
import re
from flask import Flask, jsonify, request
import os
import time
import socket
import pickle
import uuid
import tensorflow as tf

import base64
import cv2
from PIL import Image 
import fasttext
from io import BytesIO
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing

class mlosmodeling:
    def __init__(self): 
        print("mlOS Model Deployment - Initialized...")
    def tst(self,v):
        print("Testing_modeling_:"+v)
    def getdbset(self,_init):
        try:
            if(os.path.exists(_init["fn_ds_conf"])==True):
                with open(_init["fn_ds_conf"], 'r') as infile:
                    dbset= json.load(infile)
                return dbset
            else:
                return None
        except:
            return None
    def getmconf(self,_init):
        try:
            wp=_init["wp"]
            org=_init["org"]
            project=_init["project"]
            sid=_init["sid"]
            gener=_init["gener"]
            key=_init["key"]
            fnmdl_1=os.path.join(wp ,org,project,"models",gener,sid,key , "ini"+key+".json" )  
            mconf=[]
            if(os.path.exists(fnmdl_1)):
                with open(fnmdl_1, 'r') as infile:
                    mconf= json.load(infile)
                return mconf
            else:
                return None
        except:
            return None
        

    def getmodel(self,_init):
        try:
            wp=_init["wp"]
            org=_init["org"]
            project=_init["project"]
            sid=_init["sid"]
            gener=_init["gener"]
            key=_init["key"]
            mconf=self.getmconf(_init)
            model_ext=mconf["ext_model"]
            mname="model-" + key + "." +model_ext
            if(model_ext=="_noext_"):
                mname="model-" + key 
            fpmodel = os.path.join(wp,org,project,"models", gener,sid, key, mname )
            model=[]
            print(model_ext)
            print(fpmodel)
            if os.path.exists(fpmodel):
                if (model_ext=="bin"): 
                    model= fasttext.load_model(fpmodel)
                elif (model_ext=="h5"):
                    model = tf.keras.models.load_model(fpmodel)
                elif (model_ext=="_noext_"):
                    print("=======HERE MODEL========")
                    model = tf.keras.models.load_model(fpmodel)
                    print(model)
                else:
                    with open(fpmodel, 'rb') as infile:  
                        model = pickle.load(infile)
                fndbset=os.path.join("volumedata","dbs","dbset.json")
                return model
            else:
                return None
        except:
            return None


    

        


           