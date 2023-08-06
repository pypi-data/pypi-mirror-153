from flask_restful import Resource
from flask import request
#from FastCNN.prx.GongDaProxy import predictSingle
from FastCNN.prx.ValidProxy2 import predictPSingle2
from FastCNN.prx.PathProxy import PathProxy

class FastCNNApi(Resource):
    
    
    def getStatus():
        rtn = {'success':False}
        
        
        rtn['success'] = True
        return rtn
    
    def getProjectNames():
        rtn = {'success':False}
        
        data = PathProxy.getProjectNames()
        rtn['data'] = data
        
        rtn['success'] = True
        return rtn
    
    
    def testPicture():
        rtn = {'success':False}
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        modeltag = request.form.get("modeltag")
        if not modeltag:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        try:
            data = predictSingle(imagepath,modeltag)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def predictPSingle2():
        rtn = {'success':False}
        projectid = request.form.get("projectid")
        if not projectid:
            rtn["error"] = "projectid is nesserary"
            return rtn
        
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        modeltag = request.form.get("modeltag")
        if not modeltag:
            rtn["error"] = "modelid is nesserary"
            return rtn
        
        ckpt = request.form.get("ckpt")
        if not ckpt:
            rtn["error"] = "ckpt type is nesserary"
            return rtn
        try:
            data = predictPSingle2(projectid,modeltag,imagepath,ckpt)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def post(self):
        _cmd = request.form.get('cmd')
        
        if _cmd == "getProjectNames":
            return FastCNNApi.getProjectNames()
        
        if _cmd == "testPicture":
            return FastCNNApi.testPicture()
        
        if _cmd == "predictPSingle2":
            return FastCNNApi.predictPSingle2()
