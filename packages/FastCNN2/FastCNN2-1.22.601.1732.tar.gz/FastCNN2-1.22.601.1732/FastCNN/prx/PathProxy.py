import os

app_path = r"d:/FastCNN/"
data_path = r"e:/FastCNN/"

class PathProxy:
    """
    path define here
    """
    app_path = r"d:\\FastCNN\\"
    project_path = app_path + r"Projects\\"
    def getConfigPath():
        return PathProxy.app_path + r"Config\Config.json"
    
    def getWeightsPath():
        return os.path.join(PathProxy.app_path,"Config","weights")
    
    def getProjectDir(projectname):
        return os.path.join(PathProxy.project_path , projectname )+"\\"
    
    def getSettingPath(projectname):
        return PathProxy.getProjectDir(projectname) + 'Setting.json'
    
    def getProjectTrainDir(projectname):
        return PathProxy.getProjectDir(projectname) + "train" + "\\"
    
    def getProjectTestDir(projectname):
        return PathProxy.getProjectDir(projectname) + "test" + "\\"
    
    def getClassDir(projectname,classname):
        return PathProxy.getProjectDir(projectname) + classname + "\\"
        
    def getModelDir(projectname):
        return os.path.join(PathProxy.getProjectDir(projectname) , "models\\")
    
    def getModelTagDir(projectname,tag):
        return os.path.join(PathProxy.getModelDir(projectname) , tag)
        
    def getModelParamPath(projectname,tag):
        return os.path.join(PathProxy.getModelTagDir(projectname,tag) , 'Param.json')
        
    def getProjectNames():
        return os.listdir(PathProxy.project_path)
    
    def getProjectTags(projectname):
        return os.listdir(os.path.join(PathProxy.project_path,projectname,"models"))
    
    def getTrainLogPath(projectname,tag):
        return os.path.join(PathProxy.getModelTagDir(projectname,tag) , 'tpv.csv')
    
    def getSaverPath(projectname,tag):
        return os.path.join(PathProxy.getModelTagDir(projectname,tag) , "ckpt")
    
    """
    method here
    """
    def mkdir(dir):
        if os.path.exists(dir):
            return
        os.makedirs(dir)
        pass
        
class PathProxy2:
    """
    path define here
    """
    app_path = r"d:/FastCNN/"
    data_path = r"d:/FastCNN"
    
    def getConfigPath(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid, "Config.json")
    
    def getWeightsPath():
        return os.path.join(PathProxy.app_path,"Config","weights")
    
    def getDatasetRecordPath(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid, "Dataset.csv")
    
    def getSuperParamConfigPath(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid, "SuperParam.json")
    
    def getTrainProcessValues(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid,"tpv.csv")
    
    def getSaverIndex(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid,"saver.index")
    
    def getTrainCKPT(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid,"TrainSaver", "save.ckpt")
    
    def getTrainCKPTPath(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid,"TrainSaver","model.epoch")
    
    def getValidCKPT(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid,"ValidSaver", "save.ckpt")
    
    def getValidCKPTPath(projectid,modelid):
        return os.path.join(PathProxy2.app_path,"Projects",projectid,modelid,"ValidSaver","model.epoch")
    
    def getProjectNames():
        return os.listdir(os.path.join(PathProxy2.app_path,"Projects"))
    
    def getProjectTags(projectname):
        return os.listdir(os.path.join(PathProxy2.project_path,projectname,"models"))
    
    
    def getSaverPath(projectname,tag):
        return os.path.join(PathProxy2.getModelTagDir(projectname,tag) , "ckpt")
    
    """
    method here
    """
    def mkdir(dir):
        if os.path.exists(dir):
            return
        os.makedirs(dir)
        pass
        
class PathProxy3:
    """
    path define here
    """
    
    
    def getConfigPath(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid, "Config.json")
    
    def getModelDir(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid)
    
    def getDatasetRecordPath(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid, "Dataset.csv")
    
    def getWeightsPath():
        return os.path.join(app_path,"Config","weights")
    
    def getSuperParamConfigPath(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid, "SuperParam.json")
    
    def getTrainProcessValues(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid,"tpv.csv")
    
    def getSaverIndex(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid,"saver.index")
    
    def getTrainCKPT(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid,"TrainSaver", "save.pth")
    
    def getTrainCKPTPath(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid,"TrainSaver","model.epoch")
    
    def getValidCKPT(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid,"ValidSaver", "save.pth")
    
    def getValidCKPTPath(projectid,modelid):
        return os.path.join(app_path,"Projects",projectid,modelid,"ValidSaver","model.epoch")
    
    def getProjectNames():
        return os.listdir(os.path.join(app_path,"Projects"))
    
    def getProjectTags(projectname):
        return os.listdir(os.path.join(project_path,projectname,"models"))
    
    
    def getSaverPath(projectname,tag):
        return os.path.join(getModelTagDir(projectname,tag) , "ckpt")
    
    """
    method here
    """
    def mkdir(dir):
        if os.path.exists(dir):
            return
        os.makedirs(dir)
        pass
    
if __name__ == "__main__":
    cp = PathProxy2.getConfigPath("New Project1","20210713_122853")
    print(cp,os.path.exists(cp))