"""
import below
---------------------------
"""
import os,sys


debug = False
if os.path.exists("./debug"):
    sys.path.insert(0,os.path.abspath("../../"))
    debug = True
from FastCNN.prx.GongDaProxy import predictPicture,predictSingle,predictDirectory,train,predictDirectory
"""
function below
--------------------------
"""
def getArg():
    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv.pop(1)
    return arg

def getKwargs():
    """
    get kwargs by formatter["key=value"]
    call before getArg
    """
    kwargs = {}
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        arg_split = arg.split('=')
        if len(arg_split) > 1:
            kwargs[arg_split[0].strip()] = kwargs[arg_split[1].strip()]
            sys.argv.pop(i)
    return kwargs

"""
class below(if need)
---------------------------
"""
def printHelp():
    print("-"*20+"help below"+"-"*20)
    print("\tpredictPicture [picturepath] [modelpath]")
    print("\tpredictSingle [picturepath] [modeltag(directory in models)]")
    print("\tpredict [dirtag(directory in testset)] [modeltag(directory in models)]")
    print("\ttrain [modeltag,nullable]")

def callPredictPicture():
    modelpath = getArg()
    picturepath = getArg()
    
    if modelpath:
        if picturepath:
            rtn = predictPicture(picturepath,modelpath)
            print(rtn)
            return
        else:
            print("error:picturepath can not be null on predictPicture process")
    else:
        print("error:modelpath can not be null on predictPicture process")
    
    print("call predict error")

def callTrain():
    modeltag = getArg()
    
    rtn = train(modeltag)
    print("call train error")

def predictSingle():
    picturepath = getArg()
    modeltag = getArg()
    
    if modeltag:
        if picturepath:
            rtn = predictSingle(picturepath,modeltag)
            print(rtn)
            return
        else:
            print("error:picturepath can not be null on predictSingle process")
    else:
        print("error:modeltag can not be null on predictSingle process")
    
    print("call predict error")

def callPredict():
    dirtag = getArg()
    modeltag = getArg()
    
    if modeltag:
        if dirtag:
            rtn = predictDirectory(dirtag,modeltag)
            print(rtn)
            return
        else:
            print("error:dirtag can not be null on predict process")
    else:
        print("error:modeltag can not be null on predict process")
    
    print("call predict error")

"""
main below
---------------------------
"""

def main():
    if len(sys.argv) == 1:
        printHelp()
        return
    cmd = getArg()
    if cmd == "predictPicture":
        callPredictPicture()
    elif cmd == "train":
        callTrain()
    elif cmd == "predictSingle":
        callPredictSingle()
    elif cmd == "predict":
        callPredict()
    else:
        print("command {} is not recorgnised".format(cmd))
    pass

if __name__ == "__main__":
    main()
