import os
import tensorflow as tf
from tensorflow.keras.callbacks import Callback
from tensorflow.keras import Model
import numpy as np

from FastCNN.prx.PathProxy import PathProxy,PathProxy2
from FastCNN.utils.Logs import tlog

from IutyLib.file.files import CsvFile

class MACallBack(Callback):
    train_acc_history = []
    valid_acc_history = []
    
    max_train_acc = 0.0
    max_valid_acc = 0.0
    
    project_name = None
    model_tag = None
    
    ma_period = 10
    
    def init(self,projectname,modeltag,model):
        self.project_name = projectname
        self.model_tag = modeltag
        self.set_model(model)
        
        
        pass
    
    def saveLog(self,modelpath,value):
        
        pass
    
    def saveModel(self,modelpath):
        
        self.model.save_weights(modelpath)
        pass
    
    def on_epoch_end(self,epoch, logs=None):
        train_loss = logs['loss']
        train_acc = logs['sparse_categorical_accuracy']
        
        valid_loss = logs['val_loss']
        valid_acc = logs['val_sparse_categorical_accuracy']
        
        train_acc_history = self.train_acc_history
        valid_acc_history = self.valid_acc_history
        
        max_train_acc = self.max_train_acc
        max_valid_acc = self.max_valid_acc
        
        projectname = self.project_name
        model_tag = self.model_tag
        ma_period = self.ma_period
        
        train_acc_history.append(train_acc)
        valid_acc_history.append(valid_acc)
        
        if len(train_acc_history) > ma_period:
            train_acc_history.pop(0)
        
        if len(valid_acc_history) > ma_period:
            valid_acc_history.pop(0)
        
        train_mean = np.mean(train_acc_history)
        valid_mean = np.mean(valid_acc_history)
        
        if model_tag:
            trainlog = PathProxy.getTrainLogPath(projectname,model_tag+"_train")
            validlog = PathProxy.getTrainLogPath(projectname,model_tag+"_valid")
            
            trainmodel = PathProxy.getSaverPath(projectname,model_tag+"_train")
            validmodel = PathProxy.getSaverPath(projectname,model_tag+"_valid")
            
            if train_mean > max_train_acc:
                #save model here
                self.saveModel(trainmodel)
                self.max_train_acc = train_mean
            
            if valid_mean > max_valid_acc:
                #save model here
                self.saveModel(validmodel)
                self.max_valid_acc = valid_mean
            
            tlog.add(trainlog,(train_loss,train_acc,train_mean,valid_loss,valid_acc,valid_mean))
            tlog.add(validlog,(train_loss,train_acc,train_mean,valid_loss,valid_acc,valid_mean))
        pass



class MACallBack2(Callback):
    train_acc_history = []
    valid_acc_history = []
    
    max_train_acc = 0.0
    max_valid_acc = 0.0
    
    project_name = None
    model_tag = None
    
    ma_period = 100
    
    def init(self,projectname,modeltag,model):
        self.project_name = projectname
        self.model_tag = modeltag
        self.set_model(model)
        
        path = PathProxy2.getTrainProcessValues(projectname,modeltag)
        tpv = CsvFile("tpv",os.path.dirname(path))
        self.epcho = len(tpv.getData())
        pass
    
    def saveLog(self,modelpath,value):
        
        pass
    
    def saveModel(self,modelpath):
        
        self.model.save_weights(modelpath)
        pass
    
    def saveModelEpoch(modelpath,epoch):
        f = open(modelpath,'w')
        f.write(str(epoch))
        f.close()
        pass
    
    def on_epoch_end(self,epoch, logs=None):
        train_loss = logs['loss']
        train_acc = logs['sparse_categorical_accuracy']
        
        valid_loss = logs['val_loss']
        valid_acc = logs['val_sparse_categorical_accuracy']
        
        train_acc_history = self.train_acc_history
        valid_acc_history = self.valid_acc_history
        
        max_train_acc = self.max_train_acc
        max_valid_acc = self.max_valid_acc
        
        projectname = self.project_name
        model_tag = self.model_tag
        ma_period = self.ma_period
        
        train_acc_history.append(train_acc)
        valid_acc_history.append(valid_acc)
        
        if len(train_acc_history) > ma_period:
            train_acc_history.pop(0)
        
        if len(valid_acc_history) > ma_period:
            valid_acc_history.pop(0)
        
        train_mean = np.mean(train_acc_history)
        valid_mean = np.mean(valid_acc_history)
        
        if model_tag:
            trainlog = PathProxy2.getTrainProcessValues(projectname,model_tag)
            
            tlog.add(trainlog,(train_loss,train_acc,train_mean,valid_loss,valid_acc,valid_mean))
            
            if epoch < 10:
                return
            
            trainmodel = PathProxy2.getTrainCKPT(projectname,model_tag)
            validmodel = PathProxy2.getValidCKPT(projectname,model_tag)
            
            trainmodelpath = PathProxy2.getTrainCKPTPath(projectname,model_tag)
            validmodelpath = PathProxy2.getValidCKPTPath(projectname,model_tag)
            
            if train_mean > max_train_acc:
                #save model here
                self.saveModel(trainmodel)
                self.max_train_acc = train_mean
                
                MACallBack2.saveModelEpoch(trainmodelpath,epoch+self.epcho)
            
            if valid_mean > max_valid_acc:
                #save model here
                self.saveModel(validmodel)
                self.max_valid_acc = valid_mean
                
                MACallBack2.saveModelEpoch(validmodelpath,epoch+self.epcho)
            
            
            
        pass