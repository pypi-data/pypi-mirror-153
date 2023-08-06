#from FastCNN.nn.alexnet import AlexNet
#from FastCNN.nn.standard import Baseline
#from FastCNN.nn.lenet import LeNet
#from FastCNN.nn.vgg import VGG
#from FastCNN.nn.inspection import Inspection
#from FastCNN.nn.resnet import ResNet

from FastCNN.nn.efficientnets import ENet

nets = {
    #"AlexNet":AlexNet,
    #"Standard":Baseline,
    #"LeNet":LeNet,
    #"VGG":VGG,
    "ENB0":ENet,
    "ENB1":ENet,
    "ENB2":ENet,
    "ENB3":ENet,
    "ENB4":ENet,
    "ENB5":ENet,
    "ENB6":ENet,
    "ENB7":ENet,
}


def getNeuralNet(name):
    
    if name in nets:
        return nets[name](name)
    raise Exception("unrecorgnised name at call efficientnet")

def test():
    net = getNeuralNet("ENB0")
    net = net.initModel(2)
    print(net)