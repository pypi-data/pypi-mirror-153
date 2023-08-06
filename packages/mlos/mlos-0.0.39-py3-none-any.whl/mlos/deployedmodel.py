import os

import json
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import time
import pickle
import numpy as np
import pandas as pd
import sys
import requests
import re
from flask import Flask, jsonify, request
import socket
import uuid
import tensorflow as tf 
import base64
import cv2
from PIL import Image 
import fasttext
from io import BytesIO
import shap
# import sys
# sys.path.append('.')
import mlos.mloslogs as mlgs
import mlos.invprocess as imvps
import texthero as hero
mloslgs = mlgs.logs()
invpsx = imvps.invproc()

class mlosmodel:
    def __init__(self):
        print("mlOS Deploy Model - Session Initialized...")
    def getmodelinfo (self,deploytype=None):
        ismodelokay=False
        volumedata='volumedata'
        _fn='deployedmodel.json'
        if(deploytype!=None):
            if(deploytype=="challenger"):
                volumedata='challengerdata'
                _fn='challengermodel.json'
        with open(_fn, 'r') as inpfile:  
            data=json.load(inpfile)
        model_key = data["key"]
        model_ext =  data["ext"]
        model_base=  data["id"]
        model_gener=data["gener"]
        formattestdata= data["formattestdata"]

        fnmodel="model-" + model_key + "." +model_ext
        if(model_ext=="_noext_"):
            fnmodel="model-" + model_key  
        fpmodel=os.path.join(volumedata,fnmodel)
        trans_dir= os.path.join(volumedata,"dbs","trans")
        dtypeinfofn= os.path.join(volumedata,"dbs","msample.json")
        dtypex=[]
        if os.path.exists(dtypeinfofn)==True:
            with open(dtypeinfofn, 'r') as infile:  
                dtypeinfo=json.load(infile)
            dtx=dtypeinfo["data"][0]
            for d in dtx:
                dtypex.append(type(d).__name__) 
        

        inifn="mconfig-" + model_key + ".json" 
        iniffn=os.path.join(volumedata,inifn)
        mlalgo="UN"
        if os.path.exists(iniffn)==True:
            with open(iniffn, 'r') as infile:  
                mconf=json.load(infile)
            mlalgo=mconf["algo"]
        cls_lbl=[]
        
        inifn= "class_label.json"
        clsfn=os.path.join(volumedata,inifn)
        if(os.path.exists(clsfn)):
            with open(clsfn, 'r') as infile:  
                cinfo=json.load(infile)
            cls_lbl =cinfo["class_label"]

        transformation_dir=os.path.join(volumedata,"dbs","trans")
        logpath= os.path.join(volumedata,"logs" )
        logfile= os.path.join(volumedata,"logs", 'log.txt' )
        fn_sample =os.path.join(volumedata,"msample-"+model_key+".json") 
        realtimecall=os.path.join(volumedata, 'realtime' )
        if os.path.exists(realtimecall)==False:
            os.mkdir(realtimecall)
        rtfullname =os.path.join(realtimecall,"realtimeprediction.csv")
        data={
            "rows":0
        }
        rtfnjson=rtfullname+".json"
        if os.path.exists(rtfnjson)==False:
            with open(rtfnjson, 'w') as outfile:  
                json.dump(data,outfile)
        apistatpath=os.path.join(volumedata, 'apistat' )
        if os.path.exists(apistatpath)==False:
            os.mkdir(apistatpath)

        countfile=os.path.join(volumedata, 'apistat',"count.json" )
        data={
            "predict_e":0,
            "getinfo_e":0,
            "predict_s":0,
            "getinfo_s":0,
            "predict_rt":0,
            "getinfo_rt":0,
        }
        if os.path.exists(countfile)==False:
            with open(countfile, 'w') as outfile:  
                json.dump(data,outfile)


        fn_mresult =os.path.join(volumedata,"mresult-"+model_key+".json") 
        feimp=[]
        if os.path.exists(fn_mresult)==True:
            with open(fn_mresult, 'r') as infile:  
                dtxc=json.load(infile)
            feimp=dtxc["feature_imp"]

        if os.path.exists(logpath)==False:
            os.mkdir(logpath)
                
        dbset=[]
        fndbset=os.path.join(volumedata,"dbs","dbset.json")
        if os.path.exists(fndbset):
            with open(fndbset, 'r') as infile:
                dbset = json.load(infile)

        modelinfo ={
            "volumedata":volumedata,
            "model_key":model_key,
            "model_gener":model_gener,
            "model_ext":model_ext,
            "formattestdata" :formattestdata,
            "model_base":model_base,
            "fn_model":fnmodel,
            "model_full_path":fpmodel,
            "transformation_dir":transformation_dir,
            "feature_data_types" : dtypex,
            "logpath":logpath,
            "feimp":feimp,
            "logfile":logfile,
            "realtime_dir":realtimecall,
            "realtime_data_file":rtfullname,
            "realtime_row_count_file":rtfnjson,
            "api_status_dir" :apistatpath,
            "api_status_file" :countfile,
            "dbset":dbset,
            "dbset_fn":fndbset,
            "sample_fn":fn_sample,
            "algo":mlalgo,
            "class_label":cls_lbl
        }
        return modelinfo
    def makelist(self,importance, felist,fenrm):
        inc=0
        lst=[]
        for fe in felist:
            tmpx={
                "feature": fe,
                "weight": round(importance[inc], 3),
                "normweight":round(fenrm[inc], 3)
            }
            inc=inc+1
            lst.append(tmpx)
        # print(lst)
        return lst


    def explainmodel(self,model,expinfo,trn_data, smpl, felist, feimp, mtype):
        itype="static"
        try:
            # print(expinfo)
            # mtype=  expinfo["mtype"]
            # if(mtype=="usl"):
            #     return "__unsupervised__" , "__unsupervised__"
            volumedata='volumedata'
            if("expinfo" in expinfo):
                volumedata=expinfo['volumedata']

            fenrm= preprocessing.minmax_scale(feimp, feature_range=(0, 1), axis=0, copy=True)
            explainerfn=os.path.join(volumedata, "explainer.json" )
            if(os.path.exists(explainerfn)):
                _dtype = expinfo["dbset"]["dtype"]
                if(_dtype=="nlp" or _dtype=="vision"):
                    itype="dynamic"
                    ret= self.makelist([1], felist,[1])
                    return itype, ret
                dbset= expinfo["dbset"]
                mtype=  expinfo["mtype"]
                algo= expinfo["algo"]
                ktype= expinfo["ktype"]

                x_trn=smpl.iloc[0,:]
                x_tst=smpl.iloc[0,:]
                single_trn_sh=smpl.iloc[0,:]
                single_trn=smpl.iloc[0,:]
                single_tst=smpl.iloc[0,:]
                f = ""
                try:
                    if(mtype=="clsify" and algo=="dt"):
                        f = lambda x: model.predict_proba(x)[0][:,1]
                    elif(mtype=="clsify" and algo=="tree"):
                        if(len(dbset["tst"])==1):
                            f = lambda x: model.predict_proba(x)[:,1]
                        else:
                            f = lambda x: model.predict_proba(x)[0][:,1]
                    elif(mtype=="clsify" and algo=="deeplcnn"):
                        if(len(dbset["tst"])==1):
                            f = lambda x: model.predict_proba(x)[:,1]
                        else:
                            f = lambda x: model.predict_proba(x)[0][:,1]
                    elif(mtype=="regr" and algo=="df"):
                        if(len(dbset["tst"])==1):
                            f = lambda x: model.predict(x) 
                        else:
                            f = lambda x: model.predict(x) 
                    elif(mtype=="clsify" and algo=="decision_function"):
                        f = lambda x: model.decision_function(x)[0][:,1]
                except:
                    pass
                med =np.array(expinfo["med"]).reshape((1,smpl.shape[1]))
                print(med)
                # try:
                #     if( trn_data!=0):
                #         med=trn_data
                # except:
                #     raise
                #     pass
                # print(med)
                explainer=""
                if(mtype=="clsify" and algo=="dt"):
                    print(med)
                    explainer = shap.KernelExplainer(f, med, feature_names = dbset["trn"])
                elif(mtype=="clsify" and algo =="tree"):
                    explainer = shap.KernelExplainer(f, med, feature_names = dbset["trn"])
                elif(mtype=="clsify" and algo=="decision_function"):
                    explainer = shap.KernelExplainer(f, med, feature_names = dbset["trn"])
                elif(mtype=="regr" and ktype =="tree"):
                    explainer=shap.KernelExplainer(f, med,feature_names = dbset["trn"])
                elif(mtype=="regr" and ktype =="other"):
                    explainer=shap.KernelExplainer(f, med,feature_names = dbset["trn"])
                elif(mtype=="clsify" and algo=="deeplcnn"):
                    explainer = shap.KernelExplainer(f, med, feature_names = felist)
                try:
                    single_trn_sh=smpl.iloc[0,:].values.reshape((1,smpl.shape[1]))
                    shap_values_single = explainer.shap_values(single_trn_sh)
                    shap_sum=np.abs(shap_values_single).mean(axis=0).tolist()
                    nval= preprocessing.minmax_scale(shap_sum, feature_range=(0, 1), axis=0, copy=True)
                    # scaler = MinMaxScaler()
                    # scaler.fit(np.array(shap_sum).reshape(-1, 1) )
                    # shap_sum_tr=scaler.transform(np.array(shap_sum).reshape( 1,-1)).tolist()
                    ret= self.makelist(shap_sum, felist,nval)
                    itype="dynamic"
                    return itype, ret
                except:
                    itype="static"
                    ret= self.makelist(feimp, felist,fenrm)
                    return itype, ret
            else:
                itype="static"
                ret= self.makelist(feimp, felist,fenrm)
                return itype, ret
            # impx=eli5.explain_prediction_df(model,smpl.iloc[0,:], feature_names = felist).to_json(orient='table')
        except:
            ret= self.makelist(feimp, felist,fenrm)
            return itype, ret
    def loadmodel(self,modelinfo):
        model=None
        is_model_loaded=False
        volumedata="volumedata"
        if ("volumedata" in  modelinfo):
            volumedata=modelinfo["volumedata"]
        fpmodel=modelinfo["model_full_path"]
        print(fpmodel)
        if os.path.exists(fpmodel):
            if (modelinfo["model_ext"]=="bin"): 
                model= fasttext.load_model(fpmodel)
            elif (modelinfo["model_ext"]=="h5"):
                model = tf.keras.models.load_model(fpmodel)
            elif (modelinfo["model_ext"]=="_noext_"):
                model = tf.keras.models.load_model(fpmodel)
            else:
                with open(fpmodel, 'rb') as infile:  
                    model = pickle.load(infile)
            fndbset=os.path.join(volumedata,"dbs","dbset.json")
            with open(fndbset, 'r') as infile:
                dbset = json.load(infile)
            # gn_dbset_info_stat=os.path.join("volumedata","datastat.json")
            # with open(gn_dbset_info_stat, 'r') as infile:
            #     info = json.load(infile)
            # tmpinfo = json.loads(info['info'])
            # tmpdtype = json.loads(info['dtype'])
            # nrows = tmpinfo['data'][0][0]
            # ncolumns = len(tmpinfo['columns'])
            is_model_loaded=True
            # tc = time.time()
            # # df = pd.read_csv(fno, encoding='latin-1', low_memory=False) #.to_csv(trnfn) #.to_pickle(trnfn)
            # #         mllib.mltext(df)
            # #         rows,cols=df.shape
        else:
            is_model_loaded=False
        
        return is_model_loaded, model
    def getexplainermodel(self,modelinfo):
        model=None
        is_model_loaded=False
        volumedata="volumedata"
        if("volumedata" in modelinfo):
            volumedata=modelinfo["volumedata"]
        fpmodel=os.path.join(volumedata, "explainer.pkl" )
        exptrnfn=os.path.join(volumedata, "xptrn.pkl" )
        trn_data=None
        expinfo={}
        if(os.path.exists(exptrnfn)):
            with open(exptrnfn, 'rb') as infile:  
                trn_data = pickle.load(infile)
        explainerfn=os.path.join(volumedata, "explainer.json" )
        if(os.path.exists(explainerfn)):
            with open (explainerfn,'r') as infile:
                expinfo= json.load(infile)
        if os.path.exists(fpmodel):
            if( expinfo["algo"]=="deeplcnn"):
                with open(fpmodel, 'rb') as infile:  
                    model = pickle.load(infile)
                is_model_loaded=True
            else:
                is_model_loaded=False
                model =None
        else:
            explainerfn=os.path.join(volumedata, "explainer.json" )
            if(os.path.exists(explainerfn)):
                with open (explainerfn,'r') as infile:
                    expinfo= json.load(infile)
                    expinfo["volumedata"]=volumedata
            is_model_loaded=False
        return is_model_loaded,expinfo, model, trn_data
    def prepare_test_data(self,data,modelinfo):
        feature_data_types= modelinfo["feature_data_types"]
        transformation_dir = modelinfo["transformation_dir"]
        realtimecall  = modelinfo["realtime_dir"]  
        dbset=modelinfo["dbset"]
        logfile= modelinfo["logfile"]
        vals={}
        cols=dbset["trn"]
        X_test=[]
        _saveX_test=[]
        image=[]
        if( dbset["dtype"] == "table" or dbset["dtype"] == "nlp"):
            for c in cols:
                vals[c]=[]
            for i in range(len(data)):
                for j in range(len(dbset["trn"])):
                    v=data[i][j]
                    if(feature_data_types[j]=='int'):
                        v= int(v)
                    elif (feature_data_types[j]=='float'):
                        v= float(v)
                    elif  (feature_data_types[j]=='str'):
                        v= str(v)
                    vals[cols[j]].append(v)
            X_test = pd.DataFrame(vals,columns=dbset["trn"])
            _saveX_test=X_test
            mloslgs.logtext(logfile,X_test,False) 

        elif ( dbset["dtype"] == "vision"):
            
            vdir=os.path.join(realtimecall,"vdata") 
            if(os.path.exists(vdir)==False):
                os.mkdir(vdir)
            fn=str(uuid.uuid4()) + ".png"
            fnx=os.path.join(vdir,fn)
            dx=data.split(",")
            # image_data = re.sub('^data:image/.+;base64,','', data)
            # image_data = re.sub('^data:application/.+;base64,','', data)
            image_data=data.replace(dx[0],"")
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image.save(fnx, 'PNG')
            _saveX_test=pd.DataFrame([fn],columns=dbset["trn"])
            # valx= np.array(image)
            # X_test = pd.DataFrame(valx)
            # _saveX_test=X_test
            # process.mltext(logfile,X_test,True) 

        # mllib.mltext("============================")
        # fno= os.path.join("volumedata","dbs","tst.csv")
        # df = pd.read_csv(fno, encoding='latin-1', low_memory=False)
        # X_test=df[dbset["trn"]]

        # kys=dbset["operation"]
        # process.mltext(logfile,kys,True)
        imtst=[]
        preselect=dbset["dtype"] 
        istfidf=False
        for opt in dbset["operation"]:
            if(opt["id"]=="tfidf_transform"):
                preselect="nlp"
                istfidf=False
        if(preselect == "table"):
            for opt in dbset["operation"]:
                applyon=opt["applyon"]
                colm=""
                if "feature" in opt.keys():
                    colm=opt["feature"]
                if(applyon=="ondb"):
                    colm="db"
                op=opt["id"]
                if applyon=="onfe" and colm in dbset["trn"]:
                    # mllib.mltext("============================")
                    tr_fn=os.path.join(transformation_dir,colm+"+"+op+ ".pkl")
                    mloslgs.logtext(logfile,tr_fn,False) 
                    if os.path.exists(tr_fn)==True:
                        X_test.loc[:,colm]=invpsx.gettransfromed(tr_fn,X_test[colm].values.reshape((len(X_test[colm]), 1)) )
                        # mllib.mltext("============================")
                mloslgs.logtext(logfile,X_test,False)
                if applyon=="db":
                    tr_fn=os.path.join(transformation_dir,colm+"+"+op+ ".pkl")
                    if os.path.exists(tr_fn)==True:
                        X_test.loc[:, :]= invpsx.gettransfromed(tr_fn,X_test.values)
            return _saveX_test,X_test
        elif  (preselect== "nlp"):
            cname=dbset["trn"][0]
            doc = hero.clean(X_test[cname])
            cvec_fn=os.path.join(transformation_dir,cname+"+"+"tfidf_transform"+ "_CountVectorizer.pkl")
            tfidf_fn=os.path.join(transformation_dir,cname+"+"+"tfidf_transform"+ "_tfidf.pkl")
            scaler =[]
            with open(cvec_fn, 'rb') as infile:  
                mlosVectorizer = pickle.load(infile)
            with open(tfidf_fn, 'rb') as infile:  
                tfidf_transformer = pickle.load(infile)
            tmpVal_ = mlosVectorizer.transform(X_test[dbset["trn"][0]])
            xTst = tfidf_transformer.transform(tmpVal_)  
            X_test = pd.DataFrame(xTst.toarray())
            return _saveX_test,X_test
        elif (preselect   == "vision"):
            # vdir=os.path.join(realtimecall,"vdata") 
            # if(os.path.exists(vdir)==False):
            #     os.mkdir(vdir)
            # fn="test.png"
            X_test=None
            # process.mltext(logfile,"vision started",True) 
            # imfn=os.path.join(vdir,fn)
            # process.mltext(logfile,imfn,True) 
            # image = Image.open(imfn)
            rs_image=image
            new_image=image
            flag=True
            for opt in dbset["operation"]:
                if opt["id"]=="resize_the_image":
                    kv=opt["keyval"]
                    _imh=int(kv["height"]) 
                    _imw=int(kv["width"])
                    nimg=image
                    arr=np.array(nimg) 
                    if(len(arr.shape)>2):
                        nimg= nimg.convert('L')
                    rs_image=nimg.resize((_imh, _imw)) 
                    new_image=rs_image
                    flag=False
            if(flag):
                _imh=48
                _imw=48
                nimg=image
                arr=np.array(nimg) 
                if(len(arr.shape)>2):
                    nimg= image.convert('L')
                rs_image=nimg.resize((_imh, _imw)) 
                new_image=rs_image

            for opt in dbset["operation"]:
                if opt["id"]=="im2gray":
                    rs_image= rs_image.convert('L')
                    new_image= rs_image
                if opt["id"]=="im2bw":
                    rs_image= rs_image.convert('1')
                    new_image=rs_image
                if opt["id"]=="rgb2r":
                    imrgb= np.array(rs_image)
                    isz=len(imrgb.shape)
                    if(isz==3):
                        rs_image= Image.fromarray(imrgb[:,:,0]) 
                        new_image=rs_image
                    else:
                        rs_image= rs_image.convert('L')
                        new_image=rs_image
                if opt["id"]=="rgb2g":
                    imrgb= np.array(rs_image)
                    isz=len(imrgb.shape)
                    if(isz==3):
                        rs_image= Image.fromarray(imrgb[:,:,1]) 
                        new_image=rs_image
                    else:
                        rs_image= rs_image.convert('L')
                        new_image=rs_image
                if opt["id"]=="rgb2b":
                    imrgb= np.array(rs_image)
                    isz=len(imrgb.shape)
                    if(isz==3):
                        rs_image= Image.fromarray(imrgb[:,:,2]) 
                        new_image=rs_image
                    else:
                        rs_image= rs_image.convert('L')
                        new_image=rs_image
            arr=np.array(new_image)/255
            sz=arr.size
            imtst.append(arr.reshape((sz)))
            X_test=pd.DataFrame(imtst)
            tr_fn=os.path.join(transformation_dir, opt["id"]+ ".pkl")
            if (os.path.exists(tr_fn)):
                X_test= pd.DataFrame(invpsx.visiontransform(tr_fn,X_test))   
            return _saveX_test,X_test 
        else:
            return _saveX_test,X_test  

    def predict_testdata(self,X_test,model, modelinfo):
        y_pred=[]
        y_prob=[]
        y_pred_tmp=[]
        print(modelinfo)
        dbset= modelinfo["dbset"]
        model_ext = modelinfo["model_ext"]
        formattestdata= modelinfo["formattestdata"]
        mtype= modelinfo["model_gener"] 
        if (model_ext=="bin"): 
            try:
                art=[]
                if (model_ext=="bin"):
                    arrx=X_test[dbset["trn"][0]].values
                    for a in arrx:
                        art.append(a) 
                    try:
                        y_pred_tmp = model.predict(art,k=1)
                    except:
                        try:
                            if(mtype=="usl"):
                                y_pred_tmp = model.fit_predict(art)
                        except:
                            pass
                    if(mtype=="clsify"):
                        y_prob = model.predict_proba(art)
            except:
                vt = {
                     "success":False,
                    "error":True,
                    "msg":"Error in data provided.",
                }
                result={'results':vt,"status":"OK","success":True,"error":False}
                return result

        elif (model_ext=="h5" or model_ext=="_noext_"):
            if formattestdata=="deepl1":
                try:
                    xtst_shape=X_test.shape
                    x_tst=X_test.values.reshape((xtst_shape[0], xtst_shape[1],1))
                    y_pred_tmp = model.predict_classes(x_tst)
                    if(mtype=="clsify"):
                        y_prob = model.predict_proba(x_tst)
                except:
                    vt = {
                        "success":False,
                        "error":True,
                        "msg":"Error in data provided.",
                    }
                    result={'results':vt,"status":"OK","success":True,"error":False}
                    return result
            else:
                try:
                    y_pred_tmp = model.predict_classes(X_test)
                    if(mtype=="clsify"):
                        y_prob = model.predict_proba(X_test)
                except:
                    vt = {
                        "success":False,
                        "error":True,
                        "msg":"Error in data provided.",
                    }
                    result={'results':vt,"status":"OK","success":True,"error":False}
                    return result
        else:
            try:
                try:
                    y_pred_tmp = model.predict(X_test)
                except:
                    if(mtype=="usl"):
                        y_pred_tmp = model.fit_predict(X_test)    
                    
                    
                if(mtype=="clsify"):
                    if(modelinfo["algo"]=="LinearSVC"):
                        try:
                            y_prob = model.decision_function(X_test)
                        except:
                            pass
                    else:
                        try:
                            y_prob = model.predict_proba(X_test)
                        except:
                            pass
            except:
                vt = {
                    "success":False,
                    "error":True,
                    "msg":"Error in data provided.",
                }
                result={'results':vt,"status":"OK","success":True,"error":False}
                return result

        
        if type(y_pred_tmp) is tuple:
            y_pred= np.asarray(y_pred_tmp[0]).ravel()
        else:
            y_pred=y_pred_tmp
        print("=====")
        print(y_prob)
        
        print("=====")
        tmp_prob=[]
        if(len(y_prob)>1):
            print("Multi Target")
            
            for v in y_prob:
                tmp_prob.append( np.around(v,2).tolist())
        else:
            tmp_prob=np.around(y_prob,2)


        vt = {
            "success":True,
            "error":False,
            "prediction":y_pred,
            "probability": np.array(tmp_prob)
        }
        result={'results':vt,"status":"OK","success":True,"error":False}
        return result



    def saverowcount(self,fn,ncount):
        try:
            with open(fn, 'r') as inpfile:  
                data=json.load(inpfile)
            count_rows=int(data["rows"])  + int(ncount)
            data={
                "rows":count_rows
            }
            with open(fn, 'w') as outfile:  
                json.dump(data,outfile)   
        except:
            
            pass

    def prepare_restored_response(self,y_pred,_saveX_test,modelinfo):
        try:
            colt=modelinfo["dbset"]["tst"]
            print(colt)
            logfile=modelinfo ["logfile"]
            ts_fn=os.path.join(modelinfo["transformation_dir"],colt[0]+ "+categorical_2_numeric"+ ".pkl")
            mloslgs.logtext(logfile,ts_fn,False) 
            out_con=[]
            reconstrcted_response=[]
            dfx=[]
            print("=========PRED===========")
            print(y_pred)
            ln=1
            lnSmpl=len(y_pred)
            for v in y_pred:
                try:
                    ln=len(v)
                except:
                    pass
            print(ln)
            _colnames=['predicted']
            _colnames_trns=['predicted_transformed']
            print("====================")
            if(ln==1):
                print("Single target")
                try:
                    if os.path.exists(ts_fn)==True:

                        out_con=invpsx.getinvtransfromed(ts_fn, y_pred)
                        mloslgs.logtext(logfile,out_con,False)
                except:
                    try:
                        valx=[]
                        for v in y_pred:
                            valx.append(int(v))
                        out_con=invpsx.getinvtransfromed(ts_fn, valx)
                        mloslgs.logtext(logfile,"ecepet",False)
                    except:
                        print("ERR IN CON")
                        raise
                        mloslgs.logtext(logfile,"ERRROR",False)
                        out_con=[]
            else:
                _colnames=[]
                _colnames_trns=[]
 
                print("Multi target")
                out_con=[]
                colt=modelinfo["dbset"]["tst"]
                inc=0
                tdx_ppx=[]
                print(y_pred)
                for cl in colt:
                    _colnames.append("predicted_"+cl)
                    _colnames_trns.append("predicted_trns_"+cl)
                    y_pred_new=[]
                    for px_prd in y_pred:
                        y_pred_new.append(px_prd[inc])
                    ts_fn=os.path.join(modelinfo["transformation_dir"],cl+ "+categorical_2_numeric"+ ".pkl")
                    
                    if os.path.exists(ts_fn)==True:
                        y_pred_new=[]
                        for px_prd in y_pred:
                            y_pred_new.append(int(px_prd[inc]))
                        try:
                            print(y_pred_new)
                            out_con=invpsx.getinvtransfromed(ts_fn, y_pred_new)
                            print(out_con)
                            mloslgs.logtext(logfile,out_con,False)
                        except:
                            print("ERROR INV ER")
                            raise
                            out_con=y_pred_new
                        tdx_ppx.append(np.array(out_con))
                    else:
                        tdx_ppx.append(np.array(y_pred_new) )
                    inc=inc+1
                
                print(tdx_ppx)
                new_pred_conv=[]
                for i in range(lnSmpl):
                    _new_vx=[]
                    for vx in tdx_ppx:
                        _new_vx.append(vx[i])
                    new_pred_conv.append(_new_vx)

                print(new_pred_conv)
                out_con=np.array(new_pred_conv)
            print("=========CON===========")
            print(out_con)
            print("====================")
            if len(out_con)>0:
                dfx=pd.concat([_saveX_test,pd.DataFrame(y_pred,columns=_colnames ),pd.DataFrame(out_con,columns=_colnames_trns )],axis=1)
                reconstrcted_response=out_con.tolist()
            else:
                dfx=pd.concat([_saveX_test,pd.DataFrame(y_pred,columns=_colnames ),pd.DataFrame(y_pred,columns=_colnames_trns )],axis=1)
                reconstrcted_response=y_pred.tolist()

            rows,cols=dfx.shape
            realtime_data_file= modelinfo["realtime_data_file"] 
            realtime_row_count_file =modelinfo["realtime_row_count_file"]
            if os.path.exists(realtime_data_file)==False:
                with open(realtime_data_file, 'w') as outfile:
                    dfx.to_csv(outfile,index=False)
                try:
                    rows,cols=dfx.shape
                    self.saverowcount(realtime_row_count_file,rows)
                except:
                    pass
            else:
                x = dfx.to_string(header=False,index=False,index_names=False).split('\n')
                vals = [','.join(ele.split()) for ele in x]
                with open(realtime_data_file,'a') as fd:
                    for vx in vals:
                        mloslgs.logtext(logfile,vx,False)  
                        fd.write("\n"+vx)
                mloslgs.logtext(logfile,vals,False)  
                self.saverowcount(realtime_row_count_file,rows)
            retval= reconstrcted_response
            try:
                retval=reconstrcted_response.tolist()
            except:
                pass
            return  retval
        except:
            raise
            # dfx=pd.concat([_saveX_test,pd.DataFrame(y_pred,columns=['predicted'] ),pd.DataFrame(y_pred,columns=['predicted_transformed'] )],axis=1)
            reconstrcted_response=y_pred
            try:
                reconstrcted_response=y_pred.tolist()
            except:
                pass
            return reconstrcted_response
            

       