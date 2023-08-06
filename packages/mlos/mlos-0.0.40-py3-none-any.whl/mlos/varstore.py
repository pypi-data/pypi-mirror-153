import json
import os



class varstore:
    def __init__(self):
        print("mlOS Logs - Session initialized...")
        self.wp="/root/wp/mos"
        _uhome=os.path.expanduser('~')
        _wp = os.path.join(_uhome, 'wp',"mos")
        uinfohere=os.path.join(_wp,"users")
        self.wp=_wp
        if(os.path.exists(uinfohere)):
            self.wp=_wp
    def getwp(self):
        _uhome=os.path.expanduser('~')
        _wp = os.path.join(_uhome, 'wp',"mos")
        uinfohere=os.path.join(_wp,"users")
        self.wp=_wp
        if(os.path.exists(uinfohere)):
            return _wp
        else:
            return self.wp
    def addvariable(self,varinfo):
        try:
            wp=self.getwp()
            if "wp" in varinfo:
                wp=varinfo["wp"]
            uname= varinfo["uname"]
            varname= varinfo["varname"]
            vartype= varinfo["vartype"]
            # dtype= varinfo["datatype"]
            vver= varinfo["varversions"]

            if(vartype=="local"):
                vver= varinfo["varowner"]

            varpath=os.path.join(wp,"varstore")
            if(os.path.exists(varpath)==False):
                os.mkdir(varpath)
            
            if(vartype=="local"):
                vpath=os.path.join(varpath,"local")
                vver= varinfo["varowner"]
                varnamedr= os.path.join(vpath,vver,varname)
                if(os.path.exists(varnamedr)==False):
                    os.mkdir(varnamedr)
                    confn=os.path.join(varnamedr,"conf.json")
                    with open(confn,"w") as outfile:
                        json.dump(varinfo,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Already Exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            elif(vartype=="global"):
                vpath=os.path.join(varpath,"global")
                varnamedr= os.path.join(vpath,varname)
                if(os.path.exists(varnamedr)==False):
                    os.mkdir(varnamedr)
                    confn=os.path.join(varnamedr,"conf.json")
                    with open(confn,"w") as outfile:
                        json.dump(varinfo,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Already Exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            else:
                tmp={
                    "msg":"Not proper varibale type.",
                    "success":False,
                    "error":True,
                }
                return tmp

            tmp={
                    "msg":"Not proper varibale type.",
                    "success":False,
                    "error":True,
                }
            return tmp
        except:
            tmp={
                "msg":"Variable can not initiated.",
                "success":False,
                "error":True,
            }
            return tmp

    
    def getvariable(self,varinfo):
        try:
            wp=self.getwp()
            if "wp" in varinfo:
                wp=varinfo["wp"]
            varname= varinfo["varname"]
            vartype= varinfo["vartype"]
            
            vowner= "global"

            varpath=os.path.join(wp,"varstore")

            if(os.path.exists(varpath)==False):
                os.mkdir(varpath)
                tmp={
                    "msg":"Variable does not exists.",
                    "success":False,
                    "error":True,
                }
                return tmp
            if(vartype=="local"):
                vpath=os.path.join(varpath,"local")
                vver= varinfo["varowner"]
                varnamedr= os.path.join(vpath,vver,varname)
                if(os.path.exists(varnamedr)):
                    confn=os.path.join(varnamedr,"conf.json")
                    _cursor= varinfo["cursor"]
                    _curfile=os.path.join(varnamedr,_cursor+".json")
                    if(os.path.exists(_curfile)):
                        with open(_curfile,"r") as infile:
                            var_i=json.load(infile)
                        tmp={
                            "value":var_i,
                            "msg":"Created",
                            "success":True,
                            "error":False,
                        }
                        return tmp
                    else:
                        _curfile=os.path.join(varnamedr,"1.json")
                        if(os.path.exists(_curfile)):
                            with open(_curfile,"r") as infile:
                                var_i=json.load(infile)
                            tmp={
                                "value":var_i,
                                "warning":"yes",
                                "msg":"Specific cursor not found",
                                "msg":"Created",
                                "success":True,
                                "error":False,
                            }
                            return tmp
                        else:
                            tmp={
                                "msg":"Variable does not exists.",
                                "success":False,
                                "error":True,
                            }
                            return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            elif(vartype=="global"):
                vpath=os.path.join(varpath,"global")
                varnamedr= os.path.join(vpath,varname)
                if(os.path.exists(varnamedr)==False):
                    confn=os.path.join(varnamedr,"conf.json")
                    _cursor= varinfo["cursor"]
                    _curfile=os.path.join(varnamedr,_cursor+".json")
                    if(os.path.exists(_curfile)):
                        with open(_curfile,"r") as infile:
                            var_i=json.load(infile)
                        tmp={
                            "value":var_i,
                            "msg":"Created",
                            "success":True,
                            "error":False,
                        }
                        return tmp
                    else:
                        _curfile=os.path.join(varnamedr,"1.json")
                        if(os.path.exists(_curfile)):
                            with open(_curfile,"r") as infile:
                                var_i=json.load(infile)
                            tmp={
                                "value":var_i,
                                "msg":"Created",
                                "success":True,
                                "error":False,
                            }
                            return tmp
                        else:
                            tmp={
                                "msg":"Variable does not exists.",
                                "success":False,
                                "error":True,
                            }
                            return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
        except:
            tmp={
                "msg":"Variable not found",
                "success":False,
                "error":True,
            }
            return tmp


    def setvariable(self,varinfo,value,cursor):
        try:
            wp=self.getwp()
            if "wp" in varinfo:
                wp=varinfo["wp"]
            varname= varinfo["varname"]
            vartype= varinfo["vartype"]
            
            vowner= "global"

            varpath=os.path.join(wp,"varstore")

            if(os.path.exists(varpath)==False):
                os.mkdir(varpath)
                tmp={
                    "msg":"Variable does not exists.",
                    "success":False,
                    "error":True,
                }
                return tmp
            if(vartype=="local"):
                vpath=os.path.join(varpath,"local")
                vver= varinfo["varowner"]
                varnamedr= os.path.join(vpath,vver,varname)
                if(os.path.exists(varnamedr)):
                    confn=os.path.join(varnamedr,"conf.json")
                    _cursor= varinfo["cursor"]
                    _curfile=os.path.join(varnamedr,_cursor+".json")
                    with open(_curfile,"w") as outfile:
                        json.dump(value,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            elif(vartype=="global"):
                vpath=os.path.join(varpath,"global")
                varnamedr= os.path.join(vpath,varname)
                if(os.path.exists(varnamedr)):
                    confn=os.path.join(varnamedr,"conf.json")
                    _cursor= varinfo["cursor"]
                    _curfile=os.path.join(varnamedr,_cursor+".json")
                    with open(_curfile,"w") as outfile:
                        json.dump(value,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
        except:
            tmp={
                "msg":"Variable not found",
                "success":False,
                "error":True,
            }
            return tmp