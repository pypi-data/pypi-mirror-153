import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Layer
from PIL import Image
import numpy as np

import random
import matplotlib.pyplot as plt
import shutil
import time
import json
import datetime

from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Dropout, Flatten, Dense

projpath = r"D:/FastCNN/Projects/GongDa"
datapath = r"E:/FastCNN/Projects/GongDa"
trainpath = datapath + r"/train/"
testpath = datapath + r"/test/"
modelpath = projpath+ r"/models/"

np.set_printoptions(threshold=np.inf)

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1 import GPUOptions

tfconfig = ConfigProto()
tfconfig.gpu_options.per_process_gpu_memory_fraction = 1

tfconfig.gpu_options.allow_growth = True
session = InteractiveSession(config=tfconfig)

def readInput(path,dis = "OK",num = 0):
    data = []
    label = []
    for mdir,subdir,filename in os.walk(path):
        if len(filename) > 0:
            for f in filename:
                data.append(os.path.abspath(os.path.join(mdir,f)))
                label.append(num)
    
    return data, label
    
def _decode_and_resize(filename):
    tf.print(filename)
    image_string = tf.io.read_file(filename)
    print(image_string)
    image_decode = tf.image.decode_bmp(image_string)
    image_resized = tf.image.resize(image_decode, [1000, 1000])/255.0
    return image_resized

class ReadBmp(Layer):
    def __init__(self):
        super(ReadBmp,self).__init__()
        pass
    
    #@tf.function
    def _decode_and_resize(filenames):
        images = []
        for filename in filenames:
            
            image_string = tf.io.read_file(filename[0])
            
            image_decode = tf.io.decode_bmp(image_string,3)
            images.append(images)
        #image_resized = tf.image.resize(image_decode, [1000, 1000])/255.0
        return images
    
    #@tf.function
    def readBmp(files,imgw=None,imgh=None,imgf=None):
        print(files)
        if not imgw:
            imgw = 1000
        if not imgh:
            imgh = 1000
        if not imgf:
            imgf = "bmp"
        
        image_group = []
        
        for file in files:
            print(tf.cast(file,tf.string))
        #print(tf.cast(files,"string"))
            img = Image.open(tf.cast(file,tf.string))
            img = np.array(img)
            img = img / 255.
            img = tf.image.resize(img,[imgw,imgh])
            image_group.append(img)
        #image_group = tf.reshape(image_group,[imgw,imgh,len(img_group)])
        #load_image_group = np.array(image_group).reshape(len(image_group),imgw,imgh,3)
        #load_image_group = tf.image.resize(image_group,[len(image_group),imgw,imgh,3])
        
        return image_group
    
    def call(self,inputs):
        return ReadBmp._decode_and_resize(inputs)

class Baseline(Model):
    def __init__(self):
        super(Baseline, self).__init__()
        
        self.c1 = Conv2D(filters=6, kernel_size=(5, 5), padding='same')  # 卷积层
        self.b1 = BatchNormalization()  # BN层
        self.a1 = Activation('relu')  # 激活层
        self.p1 = MaxPool2D(pool_size=(2, 2), strides=2, padding='same')  # 池化层
        self.d1 = Dropout(0.2)  # dropout层

        self.flatten = Flatten()
        self.f1 = Dense(64, activation='relu')
        self.d2 = Dropout(0.2)
        self.f2 = Dense(2, activation='softmax')

    def call(self, x):
        x = self.c1(x)
        x = self.b1(x)
        x = self.a1(x)
        x = self.p1(x)
        x = self.d1(x)

        x = self.flatten(x)
        x = self.f1(x)
        x = self.d2(x)
        y = self.f2(x)
        return y

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
        img = np.array(img)
        #print(img[0][0][0])
        img = img / 255.
        #img = img * 255.0
        #print(img.astype(int)[0][0][0])
        
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

def getInputBalence(data,label,count):
    out_data = []
    out_label = []
    for i in range(count):
        out_data += data
        out_label += label
        if len(out_data) > count:
            break
    return out_data[:count],out_label[:count]

def getClasses():
    cs = os.listdir(trainpath)
    classes = {}
    for ci in range(len(cs)):
        classes[cs[ci]] = ci
    return classes

def initTag(tag):
    tpath = modelpath + tag
    if not os.path.exists(tpath):
        os.makedirs(tpath)
    pass
    
def getClassify(tag):
    initTag(tag)
    fpath = modelpath+tag+"/classes.json"
    
    if os.path.exists(fpath):
        f = open(fpath,'r')
        classify = json.load(f)
        f.close()
    else:
        classify = getClasses()
        f = open(fpath,'w')
        json.dump(classify,f)
        f.close()
    return classify
    
model = Baseline()
classify = {}

def train(tag = None):
    
    train_data = []
    train_label = []
    
    test_data = []
    test_label = []
    
    if not tag:
        tag = datetime.datetime.strftime(datetime.datetime.now(),'%y%m%d_%H%M%S')
    
    classify = getClassify(tag)
    
    for dis in classify:
        
        data,label = readInput("{}/{}/".format(trainpath,dis),dis,classify[dis])
        train_data += data
        train_label += label
    
        data,label = readInput("{}/{}/".format(testpath,dis),dis,classify[dis])
        test_data += data
        test_label += label
    
    train_batch = get_train_batch(train_data,train_label,32,150,150,"bmp")
    test_batch = get_train_batch(test_data,test_label,1,150,150,"bmp")
    
    
    model = Baseline()
    checkpoint_save_path = os.path.join(modelpath,tag,"ckpt","save.ckpt")
    log_dir = os.path.join(modelpath,tag,"logs/")
    
    if os.path.exists(checkpoint_save_path + '.index'):
        print('-------------load the model-----------------')
        model.load_weights(checkpoint_save_path)
    
    train_acc = tf.keras.metrics.SparseCategoricalAccuracy(name='train_acc')
    test_acc = tf.keras.metrics.SparseCategoricalAccuracy(name='test_acc')
    
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
                                                        #save_freq='epoch',
                                                        period = 1,
                                                        save_weights_only=True,
                                                        save_best_only=True)
        
    tensorboard = tf.keras.callbacks.TensorBoard(log_dir,histogram_freq=0)
    
    adam = tf.keras.optimizers.Adam(lr=0.0000001)
    
    model.compile(optimizer=adam,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['sparse_categorical_accuracy'])
    
    model.run_eagerly = True
    
    result = model.fit_generator(generator=get_train_batch(train_data,train_label,32,150,150,"bmp"), 
          steps_per_epoch=10, 
          epochs=10000, verbose=1,
          validation_data=test_batch,
          validation_steps=20,
          #validation_freq = 1,
          callbacks=[cp_callback],
          max_queue_size=128,
          workers=1)
    model.summary()

def predictDirectory(dirtag,modeltag):
    dirpath = os.path.join(testpath,dirtag)
    if not os.path.exists(dirpath):
        return "error:dirtag [{}] is not exists".format(dirtag)
    
    if modeltag:
        checkpoint_path = os.path.join(modelpath,modeltag,"ckpt","save.ckpt")
        if os.path.exists(checkpoint_path + '.index'):
            print('-------------load the model-----------------')
            model.load_weights(checkpoint_path)
            classify = getClassify(modeltag)
        else:
            return "error:model is not exists at [{}]".format(checkpoint_path)
    rtn = {
        "dir":dirpath,
        }
    imgs = os.listdir(dirpath)
    for img in imgs:
        imgpath = os.path.join(dirpath,img)
        result = predictSingle(imgpath,None,classify)
        print(result)
        if "maybetype" in result:
            maybetype = result["maybetype"]
            if not maybetype in rtn:
                rtn[maybetype] = 0
            rtn[maybetype] += 1
        else:
            if "error" in result:
                print("error occured stop predict directory process")
                return
    return rtn


def predictSingle(imagepath,modeltag = None,classify = None):
    try:
        s = time.time()
        #imagepath = r"{}".format(imagepath)
        #model = Baseline()
        
        if modeltag:
            checkpoint_path = os.path.join(modelpath,modeltag,"ckpt","save.ckpt")
            if os.path.exists(checkpoint_path + '.index'):
                print('-------------load the model-----------------')
                model.load_weights(checkpoint_path)
                classify = getClassify(modeltag)
            else:
                
                raise Exception("model is not exists at [{}]".format(checkpoint_path))
        
        if not os.path.exists(imagepath):
            
            raise Exception("picture is not exists at [{}]".format(imagepath))
        
        x = readBmp([imagepath],150,150,"bmp")
        
        stream = np.array(x)
        
        result = model.predict(stream,use_multiprocessing=True)
        result_index = tf.argmax(result, axis=1)
        imagename = os.path.basename(imagepath)
        maybe = result_index[0]
        percent = result[0][maybe]
        e = time.time()
        maybetype = "unknown"
        if maybe < len(classify.keys()):
            maybetype = list(classify.keys())[maybe]
        
        result = "name:{},maybe:{},percent:{}%,spend:{}s".format(imagename,maybetype,round(100.0*percent,2),round(e-s,2))
        #result = "maybe:{},{},{}".format(maybe,round(percent,2),round(e-s,2))
        result = {
            "name":imagename,
            "maybetype":maybetype,
            "percent":round(percent,2),
            "spend":round(e-s,2)
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
            checkpoint_path = os.path.join(ckptpath,"save.ckpt")
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