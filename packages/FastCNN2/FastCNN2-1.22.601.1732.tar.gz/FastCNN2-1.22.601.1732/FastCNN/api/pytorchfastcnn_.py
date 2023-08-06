from flask_restful import Resource
from flask import request
from FastCNN.prx.ValidProxy2 import insValider
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
    
    def getProjectTags():
        rtn = {'success':False}
        
        data = PathProxy.getProjectTags("GongDa")
        rtn['data'] = data
        rtn['success'] = True
        
        return rtn
    
    def setModel():
        rtn = {'success':False}
        projectid = request.form.get("projectid")
        if not projectid:
            rtn["error"] = "projectid is nesserary"
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
            data = insValider.setModel(projectid,modeltag,ckpt)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def predictSingle():
        rtn = {'success':False}
        
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        try:
            data = insValider.predictSingle(imagepath)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def predictPicture():
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
            rtn["error"] = "modeltag is nesserary"
            return rtn
        
        ckpt = request.form.get("ckpt")
        if not ckpt:
            rtn["error"] = "ckpt type is nesserary"
            return rtn
        
        try:
            data = insValider.predictPicture(imagepath,projectid,modeltag,ckpt)
        except Exception as err:
            rtn['data'] = str(err)
            print(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def post(self):
        _cmd = request.form.get('cmd')
        
        if _cmd == "getProjectNames":
            return FastCNNApi.getProjectNames()
        
        if _cmd == "getProjectTags":
            return FastCNNApi.getProjectTags()
        
        if _cmd == "predictPicture":
            return FastCNNApi.predictPicture()
        
        if _cmd == "setModel":
            return FastCNNApi.setModel()
        
        if _cmd == "predictSingle":
            return FastCNNApi.predictSingle()
