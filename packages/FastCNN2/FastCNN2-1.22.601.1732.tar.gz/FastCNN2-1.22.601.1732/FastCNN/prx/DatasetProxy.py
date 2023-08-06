from FastCNN.prx.PathProxy import PathProxy2 as PathProxy
from IutyLib.file.files import CsvFile
from IutyLib.commonutil.config import JConfig
import os

class DatasetProxy:
    
    def getTags(projectid,modelid):
        cfgpath = PathProxy.getConfigPath(projectid,modelid)
        jfile = JConfig(cfgpath)
        data = jfile.get()
        return data["LabelList"]
    
    def getData(projectid,modelid):
        csvpath = PathProxy.getDatasetRecordPath(projectid,modelid)
        dirname = os.path.dirname(csvpath)
        filename = os.path.basename(csvpath)
        
        tags = DatasetProxy.getTags(projectid,modelid)
        
        csv = CsvFile(filename.split('.')[0],dirname)
        data = csv.getData()
        
        trainset = []
        validset = []
        
        traintag = []
        validtag = []
        for d in data:
            if d[1] == "训练集":
                trainset.append(d[0])
                traintag.append(tags.index(d[2]))
            if d[1] == "验证集":
                validset.append(d[0])
                validtag.append(tags.index(d[2]))
        return trainset,validset,traintag,validtag


