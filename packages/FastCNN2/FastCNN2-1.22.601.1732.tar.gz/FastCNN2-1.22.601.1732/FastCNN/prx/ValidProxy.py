from FastCNN.prx.DatasetProxy import DatasetProxy
from FastCNN.prx.PathProxy import PathProxy2 as PathProxy
from FastCNN.nn.neuralnets import getNeuralNet
from IutyLib.file.files import CsvFile
from IutyLib.commonutil.config import JConfig
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Layer
from PIL import Image,ImageStat,ImageEnhance
import numpy as np

import random
import matplotlib.pyplot as plt
import shutil
import time
import json
import datetime



np.set_printoptions(threshold=np.inf)

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1 import GPUOptions

tfconfig = ConfigProto()
tfconfig.gpu_options.per_process_gpu_memory_fraction = 0.8

tfconfig.gpu_options.allow_growth = True
session = InteractiveSession(config=tfconfig)


def getImageBright(img):
    im = img.convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def readBmp(files,imgw=None,imgh=None,imgf=None):
    
    if not imgw:
        imgw = 1000
    if not imgh:
        imgh = 1000
    if not imgf:
        imgf = "bmp"
    
    image_group = []
    
    for file in files:
        img = Image.open(file)
        img = img.resize([imgw,imgh])
        
        lv = getImageBright(img)
        evalue = 100.0/lv
        img = ImageEnhance.Brightness(img).enhance(evalue)
        
        img = np.array(img)
        #print(img[0][0][0])
        img = img / 255.
        #img = img * 255.0
        #print(img.astype(int)[0][0][0])
        
        #print(img)
        if len(list(img.shape)) == 2:
            img = np.reshape(img,(imgw,imgh,1))
        #img = tf.image.resize(img,[imgw,imgh])
        """
        img = Image.fromarray(img,"RGB")
        img.save(r"./1.jpg")
        img.show()
        input()
        """
        image_group.append(img)
    image_group = np.array(image_group)
        #load_image_group = np.array(image_group).reshape(len(image_group),imgw,imgh,3)
        #load_image_group = tf.image.resize(image_group,[len(image_group),imgw,imgh,3])
        
    return image_group


def get_train_batch(X_train, y_train, batch_size, img_w, img_h,img_f,endless = True):
    '''
    参数：
        X_train：所有图片路径列表
        y_train: 所有图片对应的标签列表
        batch_size:批次
        img_w:图片宽
        img_h:图片高
        color_type:图片类型
        is_argumentation:是否需要数据增强
    返回: 
        一个generator，x: 获取的批次图片 y: 获取的图片对应的标签
    '''
    queue_x = []
    queue_y = []
    
    
    
    seed = random.randint(1,30)
    random.seed(seed)
    random.shuffle(X_train)
    
    random.seed(seed)
    random.shuffle(y_train)
    
    queue_x += X_train
    queue_y += y_train
    
    while 1:
        
        while (len(queue_x) < batch_size):
            queue_x += X_train
            queue_y += y_train
            
        
        
        x = queue_x[0:batch_size]
        
        x = readBmp(x,img_w,img_h,img_f)
       # queue_x = queue_x[batch_size:]
        
        y = queue_y[0:batch_size]
        #queue_y = queue_y[batch_size:]
        
        queue_x = queue_x[batch_size:]
        queue_y = queue_y[batch_size:]
        
        #yield({'input': np.array(x)}, {'output': np.array(y)})
        yield(np.array(x), np.array(y))

def getInputBalence(data,label,count):
    out_data = []
    out_label = []
    for i in range(count):
        out_data += data
        out_label += label
        if len(out_data) > count:
            break
    return out_data[:count],out_label[:count]



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

def predictPSingle2(projectid,modelid,imagepath,ckpttype):
    try:
        s = time.time()
        
        config = getConfig(projectid,modelid)
        
        width = int(config["Width"])
        height = int(config["Height"])
        
        formatter = config["Formatter"]
        
        types = config["LabelList"]
        superparam = getSuperParam(projectid,modelid)
        model = getNeuralNet(config,superparam)
        
        train_ckpt = PathProxy.getTrainCKPT(projectid,modelid)
        if ckpttype == "valid":
            train_ckpt = PathProxy.getValidCKPT(projectid,modelid)
        
        if os.path.exists(train_ckpt + '.index'):
            print('-------------load the model-----------------')
            model.load_weights(train_ckpt)
        else:
            raise Exception("model is not exists at [{}]".format(checkpoint_path))
        
                
                
        
        if not os.path.exists(imagepath):
            
            raise Exception("picture is not exists at [{}]".format(imagepath))
        
        x = readBmp([imagepath],width,height,formatter)
        
        stream = np.array(x)
        
        result = model.predict(stream,use_multiprocessing=True)
        result_index = tf.argmax(result, axis=1)
        imagename = os.path.basename(imagepath)
        maybe = result_index[0]
        percent = result[0][maybe]
        e = time.time()
        maybetype = "unknown"
        if maybe < len(types):
            maybetype = types[maybe]
        
        result = "name:{},maybe:{},percent:{}%,spend:{}s".format(imagename,maybetype,round(100.0*percent,2),round(e-s,2))
        #result = "maybe:{},{},{}".format(maybe,round(percent,2),round(e-s,2))
        
        result = {
            "name":imagename,
            "maybetype":maybetype,
            "percent":str(round(percent,2)),
            "spend":str(round(e-s,2))
            }
        
        return result
        
    except Exception as err:
        
        return {"error":str(err)}

def predictPicture(imagepath,ckptpath = None):
    try:
        s = time.time()
        imagepath = r"{}".format(imagepath)
        #model = Baseline()
        
        
        if ckptpath:
            checkpoint_path = os.path.join(modelpath,modeltag,"ckpt")
            if os.path.exists(checkpoint_path + '.index'):
                print('-------------load the model-----------------')
                model.load_weights(checkpoint_path)
            else:
                return "error:model is not exists at [{}]".format(checkpoint_path)
        
        if not os.path.exists(imagepath):
            return "error:picture is not exists at [{}]".format(imagepath)
        
        x = readBmp([imagepath],150,150,"bmp")
        stream = np.array(x)
        
        result = model.predict(stream,use_multiprocessing=True)
        result_index = tf.argmax(result, axis=1)
        imagename = os.path.basename(imagepath)
        maybe = result_index[0]
        percent = result[0][maybe]
        e = time.time()
        
        result = "name:{},maybe:{},percent:{}%,spend:{}s".format(imagename,maybe,round(100.0*percent,2),round(e-s,2))
        #result = "maybe:{},{},{}".format(maybe,round(percent,2),round(e-s,2))
        
        return result
    except Exception as err:
        return "error:{}".format(err)



if __name__ == "__main__":
    #predictPicture("E:/FastCNN/Projects/GongDa/train/OK/MyImage - 20210421095238381.bmp","D:/FastCNN/Projects/GongDa/models/ss/ckpt")
    #predictSingle("E:/FastCNN/Projects/GongDa/train/OK/MyImage - 20210421095238381.bmp","ss")
    #predictDirectory("OK","ss")
    pass