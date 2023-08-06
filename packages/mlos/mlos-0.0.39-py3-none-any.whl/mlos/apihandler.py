import os
import pickle
import json
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
import time
class mlosapi:
    def __init__(self):
        print("mlOS API Handeler - Session Initialized...")

 

    def getapistatus(self,ismodelokay,model_key):
        if ismodelokay==False:
            vt={
                "msg":"In memory model is not found for the api call. Please slect a model and redeploy.",
                "appststus":"Running",
                "modelstatus":"Not running",
                "apperror":"No",
                "modelerror":"Yes",
                "model":model_key
            }
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result
        vt={
                "msg":"Model is running.",
                "appststus":"Running",
                "modelstatus":"Running",
                "apperror":"No",
                "modelerror":"No",
                "model":model_key
        }
        result={'results':vt,"status":"OK","success":True,"error":False}
        return result
    def saveapicallstatus(self,countfile, apiid,code,tm):
        with open(countfile, 'r') as inpfile:  
            data=json.load(inpfile)
        predict_rt=data["predict_rt"]
        getinfo_rt=data["getinfo_rt"]
        count_getinfo_err=data["getinfo_e"]
        count_getinfo_sucess=data["getinfo_s"]

        count_predict_err=data["predict_e"]
        count_predict_sucess=data["predict_s"]
        
        if(apiid=='getinfo' and code =='error'):
            count_getinfo_err=count_getinfo_err+1
            if (tm>0):
                getinfo_rt=tm

        if(apiid=='getinfo' and code =='success'):
            count_getinfo_sucess=count_getinfo_sucess+1   
            if (tm>0):
                getinfo_rt=tm
        if(apiid=='predict' and code =='error'):
            count_predict_err=count_predict_err+1 
            if (tm>0):
                predict_rt=tm
        if(apiid=='predict' and code =='success'):
            count_predict_sucess=count_predict_sucess+1
            if (tm>0):
                predict_rt=tm 
        data={
            "getinfo_e":count_getinfo_err,
            "getinfo_s":count_getinfo_sucess,
            "predict_e":count_predict_err,
            "predict_s":count_predict_sucess,
            "predict_rt":predict_rt,
            "getinfo_rt":getinfo_rt,
        }
        with open(countfile, 'w') as outfile:  
            json.dump(data,outfile)

    def getinfo(self,rq,ismodelokay, modelinfo):
        if ismodelokay==False:
            vt={
                "msg":"In memory model is not found for the api call. Please slect a model and redeploy."
            }
            self.saveapicallstatus(countfile, 'getinfo','error',0)
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result
        try:
            countfile =modelinfo["api_status_file"]  
            model_key=modelinfo["model_key"]  
            model_gener=modelinfo["model_gener"]  
            model_base=modelinfo["model_base"]  
            if rq=='model_info':
                tm=time.time()
                dbsfn=os.path.join("volumedata","dconfig-"+model_key+".json")
                with open(dbsfn, 'r') as inpfile:  
                    dtx=json.load(inpfile)
                dbsfn=os.path.join("volumedata","mresult-"+model_key+".json")
                with open(dbsfn, 'r') as inpfile:  
                    mres=json.load(inpfile)
                smplfn=os.path.join("volumedata","msample-"+model_key+".json")
                with open(smplfn, 'r') as inpfile:  
                    msmpl=json.load(inpfile)

                if model_gener=="clsify":
                    data={
                        "base":model_base,
                        "version":model_key,
                        "type":model_gener,
                        "project":dtx["project"],
                        "dbconfig":dtx,
                        "_dash_1_value":mres["accuracy"],
                        "_dash_2_value":mres["error"],
                        "_dash_3_value":mres["precision_score"],
                        "_dash_4_value":mres["recall_score"],
                        "_dash_1_name":"ACCURACY",
                        "_dash_2_name": "ERROR",
                        "_dash_3_name":"PRECISION",
                        "_dash_4_name":"RECALL",
                        "performance":mres,
                        "data":msmpl["data"],
                        "title":dtx["project"].upper() +"  Dashboard"
                    }
                elif model_gener=="regr":
                    data={
                        "base":model_base,
                        "version":model_key,
                        "type":model_gener,
                        "project":dtx["project"],
                        "dbconfig":dtx,
                        "_dash_1_value":mres["mean_squared_error"],
                        "_dash_2_value":mres["mean_absolute_error"],
                        "_dash_3_value":mres["mean_squared_log_error"],
                        "_dash_4_value":mres["median_absolute_error"],
                        "_dash_1_name":"Mean Square Error",
                        "_dash_2_name": "Mean Absolute Error",
                        "_dash_3_name":"Mean Squared Log Error",
                        "_dash_4_name":"Median Absolute Error",
                        "performance":mres,
                        "data":msmpl["data"],
                        "title":dtx["project"].upper() +"  Dashboard"
                    }

                elif model_gener=="usl":
                    data={
                        "base":model_base,
                        "version":model_key,
                        "type":model_gener,
                        "project":dtx["project"],
                        "dbconfig":dtx,
                        "_dash_1_value":mres["davies_bouldin_score"],
                        "_dash_2_value":mres["silhouette_score"],
                        "_dash_3_value":mres["variance_ratio_criterion"],
                        "_dash_4_value":mres["wlaccuracy"],
                        "_dash_1_name":"Davies Bouldin Score (DB Score)",
                        "_dash_2_name": "Silhouette Score",
                        "_dash_3_name":"Variance Ratio Criterion",
                        "_dash_4_name":"Fowlkes-Mallows Scores",
                        "performance":mres,
                        "data":msmpl["data"],
                        "title":dtx["project"].upper() +"  Dashboard"
                    }
                elsp = time.time() - tm

                
                self.saveapicallstatus(countfile,'getinfo','success',elsp)
                result={'results':data , "callback": rq, "status":"OK","success":True,"error":False}
                return result
            elif rq=="model_param":
                tm=time.time()
                dbsfn=os.path.join("volumedata","dconfig-"+model_key+".json")
                with open(dbsfn, 'r') as inpfile:  
                    dtx=json.load(inpfile)
                data={
                    "base":model_base,
                    "version":model_key,
                    "type":model_gener,
                    "project":dtx["project"],
                    "title":dtx["project"].upper() +"  Dashboard"
                }
                elsp = time.time() - tm
                self.saveapicallstatus(countfile,'getinfo','success',elsp)
                result={'results':data , "callback": rq, "status":"OK","success":True,"error":False}
                return result
            else:
                dt={
                    "msg":"nothing"
                }
            result={'results':data,"status":"OK","success":True,"error":False}
            return result
        except:
            raise
            vt={
                "msg":"API executioon error."
            }
            self.saveapicallstatus(countfile,'getinfo','error',0)
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result

    def getsamples(self,is_model_loaded,modelinfo):
        if is_model_loaded==False:
            vt={
                "msg":"In memory model is not found for the api call. Please slect a model and redeploy."
            }
            result={'results':vt,"status":"OK","success":True,"error":False}
            return  result
        try:
            # fntmp=os.path.join("volumedata","dbs","msample.json")
            fntmp= modelinfo["sample_fn"]
            with open(fntmp, 'r') as infile:
                sample = json.load(infile)
            vt = {
                "sts":"ok",
                "data":sample["data"],
                "fratures":sample["columns"]
            }
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result
        except:
            vt={
                "msg":"API executioon error."
            }
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result

    def getfeatures (self,is_model_loaded,modelinfo):
        if is_model_loaded==False:
            vt={
                "msg":"In memory model is not found for the api call. Please slect a model and redeploy."
            }
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result
        try:
            vt = {
                "sts":"ok",
                "trn":modelinfo["dbset"]["trn"],
                "trg":modelinfo["dbset"]["tst"]
            }
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result
        except:
            vt={
                "msg":"API executioon error."
            }
            result={'results':vt,"status":"OK","success":True,"error":False}
            return result
