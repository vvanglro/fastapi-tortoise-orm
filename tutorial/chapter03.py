"""
@author:wanghao
@file:chapter03.py
@time:2021/04/24
"""
from datetime import date
from enum import Enum
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Cookie
from fastapi import Header
from fastapi import Path
from fastapi import Query
from pydantic import BaseModel
from pydantic import Field

app03 = APIRouter()

'''Path Parameters and Number Validations 路径参数和数字验证'''


@app03.get('/path/parameters')
def path_params01():
    return {'message': 'This is a message'}


# 函数的顺序就是路由的顺序  这里{parameters} 表示是路径参数 注意：如果路径参数值传入parameters 则路由会匹配到path_params01这个函数上
@app03.get('/path/{parameters}')
def path_params02(parameters: str):
    return {'message': parameters}


# 枚举类
class CityName(str, Enum):
    Beijing = 'Beijing China'
    Shanghai = 'Shanghai China'


@app03.get('/enum/{city}')
async def latest(city: CityName):  # 枚举类型参数
    if city == CityName.Shanghai:
        return {'city_name': city, 'confirmed': 1432, 'death': 1}
    if city == CityName.Beijing:
        return {'city_name': city, 'confirmed': 567, 'death': 1}
    return {'city_name': city, 'latest': 'unknown'}


# {file_path:path} 指定file_path 为文件路径参数 可正常识别带/的参数
@app03.get('/files/{file_path:path}')  # 通过path 传递文件路径
async def filepath(file_path: str):
    return f'The file path is {file_path}'


# 使用Path方法对参数做限制  ...表示必填， ge le 大于等于 小于等于
@app03.get('/path_/{num}')
async def path_params_validate(
        num: int = Path(
            ..., title='Your number',
            description='不可描述', ge=1, le=10,
        ),
):
    return num


"""Query Parameters and String Validations 查询参数和字符串验证"""


@app03.get('/query')
# 给了默认值就是选填参数，没给默认值就是必填参数
def page_limit(page: int = 1, limit: Optional[int] = 10):
    if limit:
        return {'page': page, 'limit': limit}
    return {'page': page}


@app03.get('/query/bool/conversion')
def page_limit2(param: bool = False):  # bool类型转换： yes on 1 True true会转换成true

    return param


@app03.get('/query/validations')
def query_params_validate(
        value: str = Query(
            ..., min_length=8, max_length=16,
            regex='^a',
        ),  # regex 匹配以a开头的字符串 且最少长度为8
        values: List[str] = Query(default=['v1', 'v2'], alias='alias_name'),
):  # 多个查询参数的列表。参数别名
    return value, values


"""Request Body and Fields 请求体和字段"""


class CityInfo(BaseModel):
    name: str = Field(..., example='Chengdu')  # example是注解的作用，值不会被验证
    country: str
    country_code: str
    country_population: int = Field(
        default=800, title='人口数量', description='国家的人口数量', ge=800,
    )

    class Config:
        # 数据格式的例子
        schema_extra = {
            'example': {
                'name': 'Chengdu',
                'country': 'China',
                'country_code': 'CN',
                'country_population': 140000000,
            },
        }


@app03.post('/request_body/city')
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


'''Request Body + Path parameters + Query parameters 多参数混合'''


@app03.put('/request_body/city/{name}')
def mix_city_info(
        name: str,  # 路径参数
        city01: CityInfo,  # body参数
        city02: CityInfo,  # body参数
        confirmed: int = Query(ge=0, description='确诊数', default=0),   # 查询参数
        death: int = Query(ge=0, description='死亡数', default=0),    # 查询参数
):
    if name == 'Chengdu':
        return {'Chengdu': {'confirmed': confirmed, 'death': death}}
    return city01.dict(), city02.dict()


'''Request Body - Nested Models 数据格式嵌套的请求体'''


class Data(BaseModel):
    city: List[CityInfo]  # 这里就是定义数据格式嵌套的请求体
    date: date  # 额外的数据类型还有：uudi datetime bytes frozenset等， 参考官方文档https://fastapi.tiangolo.com/zh/tutorial/extra-data-types/
    confirmed: int = Field(ge=0, description='确诊数', default=0)
    deaths: int = Field(ge=0, description='死亡数', default=0)
    recovered: int = Field(ge=0, description='痊愈数', default=0)


@app03.put('/request_body/nested')
def nested_models(data: Data):
    return data


'''Cookie 和 Header 参数'''


@app03.get('/cookie')
def cookie(cookie_id: Optional[str] = Cookie(None)):  # 定义Cookie参数需要使用Cookie类
    # 在headers中Cookie键对应的value为cookie_id=qwer  这样才能取到值qwer
    return {'cookie_id': cookie_id}


@app03.get('/header')
def header(
    user_agent: Optional[str] = Header(None, convert_underscores=True),
    x_token: List[str] = Header(None),
):
    '''
    有些http代理和服务器是不允许在请求头中带有下划线的，所以Header提供convert_underscores属性来转换下划线
    :param user_agent:convert_underscores=True 会把 user_agent 变成 user-agent
    :param x_token: x_token是包含多个值的列表
    :return:
    '''

    return {'user_agent': user_agent, 'x_token': x_token}
