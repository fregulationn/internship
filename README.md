# Face_fusion_rest

### Installation
1. Get the code. We will call the cloned directory as `$FACE_FUSION_ROOT`.
  ```Shell
  git clone https://github.com/fregulationn/python-REST.git
  ```

2. Build the code. Please follow [FaceNet](http://caffe.berkeleyvision.org/installation.html) to install all necessary packages and build it.We will call FaceNet cloned directory as `$FACENET_ROOT`.
  ```Shell
  cd $FACE_FUSION_ROOT
  pip install -r requirements.txt
  export PATH=$PATH:FACENET_ROOT
  ```


## Pre-trained models
| Model name      | LFW accuracy | Training dataset | Architecture |
|-----------------|--------------|------------------|-------------|
| [20180408-102900](https://drive.google.com/open?id=1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz) | 0.9905        | CASIA-WebFace    | [Inception ResNet v1](https://github.com/davidsandberg/facenet/blob/master/src/models/inception_resnet_v1.py) |
| [20180402-114759](https://drive.google.com/open?id=1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55-) | 0.9965        | VGGFace2      | [Inception ResNet v1](https://github.com/davidsandberg/facenet/blob/master/src/models/inception_resnet_v1.py) |


## Interface
#### 1.根据OpenID检查用户是否存在, 不存在则添加新用户
    URL: checkUser
    Type: POST
    body：   
    {
      openId:'qk125463'
    }

    :return 
    {
      status:True/False  
    }

#### 2.人脸融合

    URL: fusion
    Type: POST
    body：   
    {
        user_Id:'qk125463'
        inputImage:
    }

    返回值：
    {
        user_Id:'qk125463',
        type:'fusion',
        time:'Fri, 19 Apr 2019 20:12:21 GMT',
        outputImage:
    }
 

#### 3.人脸检测

    URL: detect
    Type: POST
    body：   
    {
      user_Id:'qk125463'
      inputImage: 
    }
    返回值：
    {
          user_Id:'qk125463',
          type:'detect',
          time:'Fri, 19 Apr 2019 20:12:21 GMT',
          outputImage:
    }

 
#### 4.人脸匹配

    URL: recognize
    Type: POST
    body：   
    {
      user_Id:'qk125463'
      inputImage:
    }

    返回值：
    {
      user_Id:'qk125463',
      type:'recognize',
      time:'Fri, 19 Apr 2019 20:12:21 GMT',
      outputImage:
    }


#### 5.保存(TODO)
    URL: save
    Type: POST
    body：   
    {
      user_Id:'qk125463',
      history_id:'1',
      type:'fusion/detect/recognize',
      time:'Fri, 19 Apr 2019 20:12:21 GMT',
      outputImage:
    }
    返回值：
      true/false



#### 6.获取历史数据
    URL: user/getHistory
    Type: POST
    body：   
    {
      openId:'qk125463'
    }
    返回值：

    { 
      history：
      [
        {
          user_Id:'qk125463',
          history_id:'1',
          type:'fusion',
          time:'Fri, 19 Apr 2019 20:12:21 GMT',
          outputImage:
        },
        {
          user_Id:'qk125463',
          history_id:'1'
          type:'detect',
          time:'Fri, 19 Apr 2019 20:12:21 GMT',
          outputImage:
        }
      ] 
    }


## Dataset

    1.User 
      id 
      username 

    2.Log  
      id 
      username 
      datatime  
      imageres 
      type: 'fusion','detect','recognize' 

    3.Image 
      id  
      imagepath  
      feature  
      （把这个浮点数向量使用python的json模块进行序列化 json.dumps 成为一个字符串后以TEXT类型数据存储，取出的时候再使用json.load还原成向量，浮点数精度取了10位，粗略估计一下按20计算每一个维度，则每一个向量存储空间不大于20*128，TEXT类型能够存储下 [出处](https://www.jianshu.com/p/eead9790ea97)）



  
## Detect && Recognize 
检测和识别使用的框架来自FaceNet，[出处](https://github.com/davidsandberg/facenet)，检测所使用的方法为MTCNN，识别为FaceNet，详情见出处
