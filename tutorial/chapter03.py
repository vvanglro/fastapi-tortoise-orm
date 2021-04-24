# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:chapter03.py
@time:2021/04/24
"""
from enum import Enum

from fastapi import APIRouter, Path

app03 = APIRouter()

'''Path Parameters and Number Validations 路径参数和数字验证'''


@app03.get('/path/parameters')
def path_params01():
    return {"message": 'This is a message'}


# 函数的顺序就是路由的顺序  这里{parameters} 表示是路径参数 注意：如果路径参数值传入parameters 则路由会匹配到path_params01这个函数上
@app03.get('/path/{parameters}')
def path_params02(parameters: str):
    return {"message": parameters}


# 枚举类
class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get('/enum/{city}')
async def latest(city: CityName):  # 枚举类型参数
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 1432, "death": 1}
    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 567, "death": 1}
    return {"city_name": city, "latest": 'unknown'}


# {file_path:path} 指定file_path 为文件路径参数 可正常识别带/的参数
@app03.get('/files/{file_path:path}')  # 通过path 传递文件路径
async def filepath(file_path: str):
    return f'The file path is {file_path}'


# 使用Path方法对参数做限制  ...表示必填， ge le 大于等于 小于等于
@app03.get('/path_/{num}')
async def path_params_validate(
        num: int = Path(..., title='Your number', description='不可描述', ge=1, le=10)
):
    return num