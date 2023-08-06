"""
import below
---------------------------
"""
import os,sys


debug = False
if os.path.exists("./debug"):
    sys.path.insert(0,os.path.abspath("../../"))
    debug = True
from FastCNN.prx.TrainProxy import TrainProxy
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
    print("\t projectid modelid")

def callTrain():
    projectid = getArg()
    modelid = getArg()
    if not projectid:
        print("projectid is not nullable")
    if not modelid:
        print("modelid is not nullable")
    
    rtn = TrainProxy.startTrainModel(projectid,modelid)
    


def main():
    if len(sys.argv) == 1:
        printHelp()
        return
    
    callTrain()
    
    pass

if __name__ == "__main__":
    main()
