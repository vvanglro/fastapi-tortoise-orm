# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:51
# @Author  : wanghao
# @File    : schemas.py
# @Software: PyCharm

from datetime import datetime
from datetime import date as date_
from pydantic import BaseModel


class CreateData(BaseModel):
    date:date_
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0


class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_population: int


class ReadData(CreateData):
    id: int
    city_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReadCity(CreateCity):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True