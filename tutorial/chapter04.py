# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:chapter04.py
@time:2021/04/24
"""
from typing import Optional, List, Union
from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr, Field

app04 = APIRouter()

'''Response Model 响应模型'''


class UserMix(BaseModel):
    username: str
    email: EmailStr   # 用EmailStr 需要 pip install  pydantic[email]
    mobile: str = Field(default='18812340987', title='手机号', regex="^1[3456789]\d{9}$")
    address: str = None
    full_name: Optional[str] = None


# 共有的字段可以写类继承
class UserIn(UserMix):
    password: str


# 共有的字段可以写类继承
class UserOut(UserMix):
    pass


users = {
    "user01": {"username": "user01", "password": "123456", "email": "user01@example.com"},
    "user02": {"username": "user02", "password": "123456", "email": "user02@example.com", "mobile": "15612340987"},
}


@app04.post('/response_model', response_model=UserOut, response_model_exclude_unset=True)
async def response_model_r(user: UserIn):
    """
    response_model_exclude_unset=True表示默认值不包含在响应中，仅包含实际给的值，如果实际给的值与默认值相同也会包含在响应中
    """
    print(user.password)  # password不会被返回
    return users['user02']


@app04.post(
    '/response_model/attributes',
    response_model=UserOut,
    # response_model=Union[UserIn, UserOut],
    # response_model=List[UserOut],
    response_model_include=['username', 'email', 'mobile'],
    # response_model_exclude= ['mobile']
)
async def r_model_attributes(user: UserIn):
    '''
    response_model_include列出需要在返回结果中包含的字段；
    response_model_exclude列出需要在返回结果中排除的字段；
    response_model=Union[UserIn, UserOut] 取UserIn和UserOut并集后的字段返回
    response_model=List[UserOut] 返回的结果是list中嵌套UserOut模型
    '''

    # del user.password  # Union[UserIn, UserOut]后， 删除password属性也能返回成功
    # return [user, user]  # response_model=List[UserOut]返回必须是list
    return user


'''Response Status Code 响应状态码'''


@app04.post('/status_code', status_code=200)
async def status_code():
    return {"status_code": 200}


@app04.post('/status_attribute', status_code=status.HTTP_200_OK)
async def status_attribute():
    print(type(status.HTTP_200_OK))
    return {"status_code": status.HTTP_200_OK}



'''Form Data 表单数据处理'''

@app04.post('/login')
async def login(
        username: str = Form(...),
        password: str = Form(...)
):
    '''
    用Form类需要pip install python-multipart
    Form类的元数据和校验方法类似Body/Query/Path/Cookie
    '''
    return {"username": username}


'''Request Files 单文件 多文件上传及参数详解'''

@app04.post('/file')
async def file_1(file: bytes = File(...)):  # 如果要上传多个文件 files: List[bytes] = File(...)
    '''使用File类 文件内容会以bytes的形式读入内存 适合用于上传小文件'''
    return {'file_size': len(file)}

@app04.post('/upload_files')
async def upload_files(files: List[UploadFile] = File(...)):  # 如果要上传单个文件 files: UploadFile = File(...)
    '''
        使用Uploadfile类的优势：
            1. 文件存储在内存中，使用的内容达到阈值后，将被保存在磁盘中
            2. 适用于图片、视频大文件
            3. 可以获取上传文件的元数据，如文件名，创建时间等
            4. 有文件对象的异步接口
            5. 上传的文件是python文件对象，可以使用write()，read()，seek()，close()操作
    :param files:
    :return:
    '''
    for file in files:
        contents = await file.read()
        print(contents)
    return {"filename": files[0].filename, "content_type": files[0].content_type}


'''【见run.py】FastAPI项目的静态文件配置'''



'''Path Operation Configuration 路径操作配置'''

@app04.post(
    '/path_operation_configuration',
    response_model=UserOut,
    # tags=['Path','Operation','Configurarion'],
    summary= "This is summary",   #api文档里的描述
    description='This is description',  #api文档里的描述
    response_description='This is response description',  #api文档里的描述
    # description=True,
    status_code=status.HTTP_200_OK
)
async def path_operation_configuration(user: UserIn):
    '''
    Path Operarion configuration 路径操作配置
    :param user: 用户信息
    :return:
    '''
    return user.dict()


'''Handing Errors 错误处理'''

@app04.get('/http_exception')
async def http_exception(city: str):
    if city != 'CD':
        raise HTTPException(status_code=404, detail='city not found', headers={"X-Error":'error'})
    return {"city":city}


