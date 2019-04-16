# Face_fusion_rest

#### 1.根据OpenID检查用户是否存在, 不存在则添加新用户
    URL: user/checkUser?openId=123 
    Type: GET 
    返回值：null,表示不存在且创建失败 

#### 2.人脸融合

    URL: fusion
    Type: POST
    body：   
    {
        user_Id:'123'
        inputImage:
    }

    返回值：
    {
        user_Id:'123',
        history_id:'1'
        type:'fusion',
        time:'******',
        outputImage:
    }
 

#### 3.人脸检测

    URL: detect
    Type: POST
    body：   
    {
      user_Id:'123'
      inputImage:
    }
    返回值：
    {
          user_Id:'123',
    history_id:'1'
          type:'detect',
          time:'******',
          outputImage:

    }

 
#### 4.人脸匹配

    URL: recognize
    Type: POST
    body：   
    {
      user_Id:'123'
      inputImage:
    }

    返回值：
    {
      user_Id:'123',
      history_id:'1'
      type:'recognize',
      time:'******',
      outputImage:
    }


#### 5.保存
    URL: save
    Type: POST
    body：   
    {
      user_Id:'123',
      history_id:'1'
      type:'fusion/detect/recognize',
      time:'******',
      outputImage:
    }
    返回值：
      true/false



#### 6.获取历史数据
    URL: user/getHistory?openId=123
    Type: GET
    返回值：

    { 
      [
        {
          user_Id:'123',
          history_id:'1',
          type:'fusion',
          time:'******',
          outputImage:
        },
        {
          user_Id:'123',
          history_id:'1'
          type:'detect',
          time:'******',
          outputImage:
        }
      ] 
    }


数据库表
  1. user
     openId

  2. log
     openId
     history_Id
     time
     outputImage ：
     type: 'fusion'

  3. image 
     feature 
  

图片上传 返回图片地址
图片下载 通过图片在服务器地址返回图片