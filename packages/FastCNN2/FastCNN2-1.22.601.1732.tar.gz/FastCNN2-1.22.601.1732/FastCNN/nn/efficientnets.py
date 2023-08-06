import os,sys

import torch
import torch.nn as nn

from efficientnet_pytorch import EfficientNet
from FastCNN.prx.PathProxy import PathProxy3 as PathProxy
from FastCNN.nn.torchnn import TorchNet

from torchvision import datasets, transforms

from FastCNN.datasets.fastcsv import FastCsvT1

from PIL import Image

enetnames = {
    "ENB0":"efficientnet-b0",
    "ENB1":"efficientnet-b1",
    "ENB2":"efficientnet-b2",
    "ENB3":"efficientnet-b3",
    "ENB4":"efficientnet-b4",
    "ENB5":"efficientnet-b5",
    "ENB6":"efficientnet-b6",
    "ENB7":"efficientnet-b7",
}

input_sizes = {
    "ENB0":224,
    "ENB1":240,
    "ENB2":260,
    "ENB3":300,
    "ENB4":380,
    "ENB5":456,
    "ENB6":528,
    "ENB7":600,
}

batch_sizes = {
    "ENB0":28,
    "ENB1":24,
    "ENB2":20,
    "ENB3":16,
    "ENB4":12,
    "ENB5":10,
    "ENB6":8,
    "ENB7":6,
}

class ENet(TorchNet):
    
    def __init__(self,net_name):
        self.net_name = net_name
        super(ENet,self).__init__()
        pass
    
    def initModel(self,class_num):
        self._model = EfficientNet.from_name(enetnames[self.net_name])
        
        
        net_weight = os.path.join(PathProxy.getWeightsPath(),"{}.pth".format(self.net_name))
        state_dict = torch.load(net_weight)
        self._model.load_state_dict(state_dict)
        # 修改全连接层
        num_ftrs = self._model._fc.in_features
        self._model._fc = nn.Linear(num_ftrs, class_num)
        
        use_gpu=torch.cuda.is_available()
        if use_gpu:
            self._model = self._model.cuda()
        
        return self._model
        
    def getDefaultBatchSize(self):
        return batch_sizes[self.net_name]
    
    def getPreProcess(self,fliph = False):
        input_size = input_sizes[self.net_name]
        
        train = [
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
            
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]
        
        valid = [
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
                
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]
        #add preprocess below
        if fliph:
            train.insert(2,transforms.RandomHorizontalFlip())
        
        #output
        data_transforms = {
            'train': transforms.Compose(train),
            'valid': transforms.Compose(valid),
        }
        return data_transforms
    


def test():
    net = ENet("ENB0")
    batch_size = net.getDefaultBatchSize()
    assert batch_size == 28
    
    pre = net.getPreProcess(fliph=True)
    print(pre)
    
    trainpre = pre["train"]
    validset = FastCsvT1(r"D:\FastCNN\Projects\New_Project3\20210812_210246","验证集",trainpre)
    
    mdl = net.initModel(2)
    
    batch = torch.utils.data.DataLoader(validset,batch_size=3,shuffle=False, num_workers=0)
    
    print(len(validset))
    
    img = r"E:\yaoping1\Valid\OK\Grab3_0_1256445_074239.bmp"
    img=Image.open(img).convert('RGB')
    
    validpre = pre["valid"]
    img = validpre(img).unsqueeze(0).cuda()
    
    outputs = mdl(img).cuda()
    print(outputs)
    indices = torch.argmax(outputs,1)
    
    tags = sorted(["OK","NG"])
    print(tags[indices.item()])
    
    #percentage = outputs.item()[indices.item()]
    percentage = torch.softmax(outputs, dim=1)[0][indices.item()].item()
    print(percentage)
    
    

