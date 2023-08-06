import torch
import torch.nn as nn
from PIL import Image
import random
import numpy as np
import os

from torch.autograd import Variable

class TorchNet:
    _model = None
    def initModel(self,class_num):
        raise NotImplementedError
    
    def loadModel(self,modelpath):
        if self._model == None:
            raise RuntimeError("Model is not initialed")
        if os.path.exists(modelpath):
            
            self._model = torch.load(modelpath)
            #.load_state_dict(state_dict)
        
        return self._model
    
    def saveModel(self,modelpath):
        if self._model == None:
            raise RuntimeError("Model is not initialed")
        if os.path.exists(os.path.dirname(modelpath)):
            
            torch.save(self._model,modelpath)
        pass
    
    def getDefaultBatchSize(self):
        raise NotImplementedError
    
    def trainEpcho(self,epchor,optimizer,criterion):
        """
        train trainset with epchor yield (called by for .. in net.trainEpcho)
        
        inputs:
            epchor: a DataLoader like: torch.utils.data.DataLoader
            criterion: loss function
            
        """
        if self._model == None:
            raise RuntimeError("Model is not initialed")
        
        use_gpu=torch.cuda.is_available()
        self._model.train(True)
        #running_loss = 0.0
        #running_corrects = 0
        
        for batch in epchor:
            
            inputs, labels = batch
            labels = torch.squeeze(labels.type(torch.LongTensor))
            if use_gpu:
                inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            else:
                inputs, labels = Variable(inputs), Variable(labels)
            outputs = self._model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs.data, 1)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            #running_loss += loss.item() * inputs.size(0)
            #running_corrects += torch.sum(preds == labels.data)
            
            yield loss.item(),torch.sum(preds == labels.data)
        
        #epoch_loss = running_loss / data_count
        #epoch_acc = running_corrects.double() / data_count
        
        
        pass
    
    def validEpcho(self,epchor,criterion):
        """
        valid validset with epchor yield (called by for .. in net.validEpcho)
        
        inputs:
            epchor: a DataLoader like: torch.utils.data.DataLoader
            criterion: loss function
            
        """
        if self._model == None:
            raise RuntimeError("Model is not initialed")
        
        use_gpu=torch.cuda.is_available()
        self._model.eval()
        #running_loss = 0.0
        #running_corrects = 0
        
        with torch.no_grad():
            for batch in epchor:
            
                inputs, labels = batch
                labels = torch.squeeze(labels.type(torch.LongTensor))
                if use_gpu:
                    inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
                else:
                    inputs, labels = Variable(inputs), Variable(labels)
                outputs = self._model(inputs)
                loss = criterion(outputs, labels)
                _, preds = torch.max(outputs.data, 1)
            
            
                yield loss.item() * inputs.size(0),torch.sum(preds == labels.data)
        
    def predictSingle(self,imgpath):
        pass
    pass