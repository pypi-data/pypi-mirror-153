import os

class logs:
    def __init__(self):
        print("mlOS Logs - Session initialized...")
    def logtext(self,fn,msg,vb):
        # valx= str(msg).replace(config._wp,'')
        with open(fn, 'a') as f1:
            f1.write('\n')
            f1.write(str(msg))
        if vb:
            print(str(msg))