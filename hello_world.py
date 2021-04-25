# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:hello_world.py
@time:2021/04/24
"""
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None  # 可选填布尔字段  默认值为None


# @app.get('/')
# def hello_world():
#     return {"hello": "world"}
#
#
# @app.get('/city/{city}')
# def result(city: str, query_string: Optional[str] = None):
#     return {"city": city, "query_string": query_string}
#
#
# @app.put('/city/{city}')
# def result(city: str, city_info: CityInfo):
#     return {"city": city, "province": city_info.province, "country": city_info.country,
#             "is_affected": city_info.is_affected}


# 异步方法 在函数里await即可
@app.get('/')
async def hello_world():
    return {"hello": "world"}


@app.get('/city/{city}')
async def result(city: str, query_string: Optional[str] = None):
    return {"city": city, "query_string": query_string}


@app.put('/city/{city}')
async def result(city: str, city_info: CityInfo):
    return {"city": city, "province": city_info.province, "country": city_info.country,
            "is_affected": city_info.is_affected}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
