import matplotlib.pyplot as plt
import os
from FastCNN.utils.Logs import tlog
import numpy as np

def main():
    path = "./tpv.csv"
    if not os.path.exists(path):
        print("当前目录中不存在训练过程数据记录，请在模型文件夹下运行当前命令")
        return
    
    values = tlog.get(path)
    
    train_loss = values[0]
    train_acc = values[1]
    train_mean = values[2]
    valid_loss = values[3]
    valid_acc = values[4]
    valid_mean = values[5]
    
    
    ax1 = plt.subplot(2, 1, 1)
    
    plt.plot(range(len(train_loss)),[round(float(v),2) for v in train_loss],'r')
    plt.plot(range(len(valid_loss)),[round(float(v),2) for v in valid_loss],'b')
    
    plt.title("loss")
    plt.xlabel('X:echpo*10')
    #plt.ylim(0, 2)
    
    ax2 = plt.subplot(2, 1, 2)
    
    #ax2.plot(range(len(train_acc)),[round(float(v),2) for v in train_acc],'r')
    ax2.plot(range(len(train_mean)),[round(float(v),2) for v in train_mean],'r--')
    
    #ax2.plot(range(len(valid_acc)),[round(float(v),2) for v in valid_acc],'b')
    ax2.plot(range(len(valid_mean)),[round(float(v),2) for v in valid_mean],'b--')
    
    plt.title("acc")
    plt.xlabel('X:echpo*10')
    #plt.ylim(0, 1)
    plt.show()

if __name__ == "__main__":
    main()