# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:51
# @Author  : wanghao
# @File    : schemas.py
# @Software: PyCharm

from coronavirus import models, schemas


async def get_city(city_id: int):
    # 根据城市id查询第一条数据
    return await models.City.filter(id=city_id).first()


async def get_city_by_name(name: str):
    # 根据城市名字查询数据
    return await models.City.filter(province=name).first()


async def get_cities(skip: int = 0, limit: int = 10):
    # 查询默认0-10的数据
    return await models.City.all().offset(skip).limit(limit)


async def create_city(city: schemas.CreateCity):
    # 创建城市
    return await models.City.create(**city.dict())


async def update_city(city_name: str, city: schemas.CreateCity):
    # 更新城市信息
    return await models.City.filter(province=city_name).update(**city.dict())


async def get_data(city: str = None, skip: int = 0, limit: int = 10):
    # 获取数据
    if city:
        return await models.Data.filter(city__province=city).prefetch_related("city").limit(6)
    return await models.Data.all().prefetch_related("city").offset(skip).limit(limit)


async def create_city_data(data: schemas.CreateData, city_id: int):
    # 创建数据

    return await models.Data.create(**data.dict(), city_id=city_id)
