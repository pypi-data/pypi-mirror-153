from FastCNN.prx.DatasetProxy import DatasetProxy
from FastCNN.prx.PathProxy import PathProxy2 as PathProxy
from FastCNN.nn.neuralnets import getNeuralNet
from FastCNN.utils.CallBacks import MACallBack2 as MACallBack
from IutyLib.file.files import CsvFile
from IutyLib.commonutil.config import JConfig
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
import tensorflow as tf
from PIL import Image,ImageStat,ImageEnhance
import numpy as np

import random
import shutil
import time
import json
import datetime

np.set_printoptions(threshold=np.inf)

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1 import GPUOptions

tfconfig = ConfigProto()
tfconfig.gpu_options.per_process_gpu_memory_fraction = 1

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
        if len(list(img.shape)) == 2:
            img = np.reshape(img,(imgw,imgh,1))
        #print(img)
        
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


class TrainProxy:
    projectid = ""
    modelid = ""
    config = None
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
        projectid = projectid
        modelid = modelid
        config = TrainProxy.getConfig(projectid,modelid)
        trainset,validset,traintag,validtag = DatasetProxy.getData(projectid,modelid)
        
        superparam = TrainProxy.getSuperParam(projectid,modelid)
        epchos = int(superparam["Epcho"])
        batch = int(superparam["Batch"])
        width = int(config["Width"])
        height = int(config["Height"])
        learnrate = float(superparam["LearnRate"])
        formatter = config["Formatter"]
        
        train_batch = get_train_batch(trainset,traintag,batch,width,height,formatter)
        test_batch = get_train_batch(validset,validtag,int(batch/4)+1,width,height,formatter)
        
        model = getNeuralNet(config,superparam)
        
        train_ckpt = PathProxy.getTrainCKPT(projectid,modelid)
        valid_ckpt = PathProxy.getValidCKPT(projectid,modelid)
        
        if os.path.exists(train_ckpt + '.index'):
            print('-------------load the model-----------------')
            model.load_weights(train_ckpt)
        
        train_acc = tf.keras.metrics.SparseCategoricalAccuracy(name='train_acc')
        test_acc = tf.keras.metrics.SparseCategoricalAccuracy(name='test_acc')
        
        adam = tf.keras.optimizers.Adam(lr=learnrate)
        
        model.compile(optimizer=adam,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['sparse_categorical_accuracy'])
        
        ma_callback = MACallBack()
        ma_callback.init(projectid,modelid,model)
        
        result = model.fit_generator(generator=get_train_batch(trainset,traintag,batch,width,height,formatter), 
          steps_per_epoch=10, 
          epochs=epchos, verbose=1,
          validation_data=test_batch,
          validation_steps=1,
          #validation_freq = 1,
          callbacks=[ma_callback],
          max_queue_size=128,
          workers=1)
        pass

if __name__ == "__main__":
    pass