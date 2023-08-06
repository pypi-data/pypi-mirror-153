import copy

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

from FastCNN.datasets.fastcsv import FastCsvT1

from efficientnet_pytorch import EfficientNet
from torch.autograd import Variable
import time
import os
import datetime
#os.environ["CUDA_VISIBLE_DEVICES"] = "7"

from IutyLib.file.files import CsvFile
from IutyLib.commonutil.config import JConfig

from FastCNN.utils.Logs import tlog

from FastCNN.prx.PathProxy import PathProxy3 as PathProxy
from FastCNN.nn.neuralnets import getNeuralNet



def exp_lr_scheduler(optimizer, epoch, init_lr=0.01, lr_decay_epoch=10):
    """Decay learning rate by a f#            model_out_path ="./model/W_epoch_{}.pth".format(epoch)
#            torch.save(model_W, model_out_path) actor of 0.1 every lr_decay_epoch epochs."""
    lr = init_lr * (0.8 ** (epoch // lr_decay_epoch))
    print('LR is set to {}'.format(lr))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

    return optimizer


def getLoaders(projectid,modelid,net):
    setloaders = {}
    modeldir = PathProxy.getModelDir(projectid,modelid)
    
    pre = net.getPreProcess(fliph=True)
    
    trainset = FastCsvT1(modeldir,"训练集",pre["train"])
    validset = FastCsvT1(modeldir,"验证集",pre["valid"])
    
    num_workers=1 if torch.cuda.is_available() else 0
    
    batch_size = net.getDefaultBatchSize()
    
    trainbatch = torch.utils.data.DataLoader(trainset,batch_size=batch_size,shuffle=True, num_workers=num_workers)
    validbatch = torch.utils.data.DataLoader(validset,batch_size=batch_size, num_workers=num_workers)
    setloaders = {
            "trainset":trainset,
            "validset":validset,
            "trainbatch":trainbatch,
            "validbatch":validbatch,
            }
    return setloaders

def saveModelEpoch(path):
    dirpath = os.path.dirname(path)
    csv = CsvFile("tpv",os.path.dirname(dirpath))
    epoch = len(csv.getData())
    f = open(os.path.join(dirpath,"model.epoch"),'w')
    f.write(str(epoch))
    f.close()

class TrainProxy:
    def getConfig(projectid,modelid):
        cfgpath = PathProxy.getConfigPath(projectid,modelid)
        jfile = JConfig(cfgpath)
        data = jfile.get()
        return data
    
    def getSuperParam(projectid,modelid):
        cfgpath = PathProxy.getSuperParamConfigPath(projectid,modelid)
        jfile = JConfig(cfgpath)
        data = jfile.get()
        return data
    
    
    def startTrainModel(projectid,modelid):
        config = TrainProxy.getConfig(projectid,modelid)
        superparam = TrainProxy.getSuperParam(projectid,modelid)
        
        net_name = config["Type"]
        
        epchos = int(superparam["Epcho"])
        #batch = int(superparam["Batch"])
        #width = int(config["Width"])
        #height = int(config["Height"])
        learnrate = float(superparam["LearnRate"])
        formatter = config["Formatter"]
        
        class_count = len(config["LabelList"])
        
        prestop = int(superparam["PreStop"])
        
        net = getNeuralNet(net_name)
        net.initModel(class_count)
        
        train_ckpt = PathProxy.getTrainCKPT(projectid,modelid)
        valid_ckpt = PathProxy.getValidCKPT(projectid,modelid)
        
        os.makedirs(os.path.dirname(train_ckpt),exist_ok=True)
        os.makedirs(os.path.dirname(valid_ckpt),exist_ok=True)
        
        model_ft = net.loadModel(valid_ckpt)
        
        loaders = getLoaders(projectid,modelid,net)
        
        criterion = nn.CrossEntropyLoss()
        
        if torch.cuda.is_available():
            model_ft = model_ft.cuda()
            criterion = criterion.cuda()
        
        optimizer = optim.SGD((model_ft.parameters()), lr=learnrate,momentum=0.9, weight_decay=0.0004)
        
        
        max_train_acc = 0.0
        max_valid_acc = 0.0
        
        save_epoch = 0
        
        trainlog = PathProxy.getTrainProcessValues(projectid,modelid)
        #train process
        for i in range(epchos):
            print("*"*20)
            optimizer = exp_lr_scheduler(optimizer,i)
            data_count = len(loaders["trainset"])
            running_loss = 0.0
            running_corrects = 0
            for loss,acc in net.trainEpcho(loaders["trainbatch"],optimizer,criterion):
                
                running_loss += loss
                running_corrects += acc
            epoch_loss = running_loss / data_count
            epoch_acc = running_corrects.double() / data_count
            
            if max_train_acc < epoch_acc:
                net.saveModel(train_ckpt)
                max_train_acc = epoch_acc
                saveModelEpoch(train_ckpt)
            print("[training] at epcho:{}/{},loss = {}, acc = {}".format(i,epchos,epoch_loss,epoch_acc))
            
            train_epoch_loss = epoch_loss
            train_epoch_acc = epoch_acc
            #valid per epcho
            
            data_count = len(loaders["validset"])
            running_loss = 0.0
            running_corrects = 0
            for loss,acc in net.validEpcho(loaders["validbatch"],criterion):
                
                running_loss += loss
                running_corrects += acc
            epoch_loss = running_loss / data_count
            epoch_acc = running_corrects.double() / data_count
            
            if max_valid_acc < epoch_acc:
                net.saveModel(valid_ckpt)
                max_valid_acc = epoch_acc
                saveModelEpoch(valid_ckpt)
                
                save_epoch = i
            
            
            
            print("[validing] at epcho:{}/{},loss = {}, acc = {}".format(i,epchos,epoch_loss,epoch_acc))
            
            valid_epoch_loss = epoch_loss
            valid_epoch_acc = epoch_acc
            tlog.add(trainlog,(train_epoch_loss,train_epoch_acc,0.0,valid_epoch_loss,valid_epoch_acc,0.0))
            
            if i - save_epoch > prestop:
                print("prestop because acc is not raise in the last 10 epoch")
                break
            
        pass

def test():
    TrainProxy.startTrainModel("New_Project3","20210812_210246")

if __name__ == '__main__':
    #main()
    #valid()
    pass
