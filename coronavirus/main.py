# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:51
# @Author  : wanghao
# @File    : schemas.py
# @Software: PyCharm
import httpx
from typing import List

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import HttpUrl
from starlette import status

from fastapi.templating import Jinja2Templates
from coronavirus import crud, schemas
from coronavirus.models import City, Data

# 路由
application = APIRouter()

templates = Jinja2Templates(directory='./coronavirus/templates')


@application.post(
    '/create_city',
    summary="创建城市",  # api文档里的描述
    description='创建城市接口',  # api文档里的描述
    response_model=schemas.ReadCity)
async def create_city(city: schemas.CreateCity):
    # 去数据库中查询城市是否存在 不存在则创建
    db_city = await crud.get_city_by_name(name=city.province)
    if db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='城市已存在')
    return await crud.create_city(city=city)


@application.put(
    '/update_city/{city}',
    summary="更新城市信息",  # api文档里的描述
    description='更新城市信息接口',  # api文档里的描述
)
async def update_city(city: str, city_data: schemas.CreateCity):
    # city为路径参数 去查询是否存在这个城市 存在则返回信息
    db_city = await crud.get_city_by_name(name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='城市未找到')
    # 更新数据是返回的更新的行数 这里是更加城市名去更新 由于城市名是unique所以只返回1或0
    num = await crud.update_city(city_name=city, city=city_data)
    if not num:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail='数据更新失败')
    return {"status_code": status.HTTP_200_OK, "msg": "success"}


@application.get(
    '/get_city/{city}',
    summary="获取单个城市信息",  # api文档里的描述
    description='获取单个城市信息接口',  # api文档里的描述
    response_model=schemas.ReadCity)
async def get_city(city: str):
    # city为路径参数 去查询是否存在这个城市 存在则返回信息
    db_city = await crud.get_city_by_name(name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='城市未找到')
    return db_city


@application.get(
    '/get_cities',
    summary="获取城市列表信息",  # api文档里的描述
    description='获取城市列表信息接口',  # api文档里的描述
    response_model=List[schemas.ReadCity])
async def get_cities(skip: int = 0, limit: int = 10):
    # 分页查询城市信息
    cities = await crud.get_cities(skip=skip, limit=limit)
    return cities


@application.post(
    '/create_data',
    summary="创建城市数据",  # api文档里的描述
    description='创建城市数据接口',  # api文档里的描述
    response_model=schemas.ReadData)
async def create_data_for_city(city: str, data: schemas.CreateData):
    # 创建与城市关联的数据
    db_city = await crud.get_city_by_name(name=city)
    data = await crud.create_city_data(data=data, city_id=db_city.id)
    return data


@application.get(
    '/get_data',
    summary="获取城市数据",  # api文档里的描述
    description='获取城市数据接口',  # api文档里的描述
)
async def get_data(city: str = None, skip: int = 0, limit: int = 10):
    # 分页获取数据
    data = await crud.get_data(city=city, skip=skip, limit=limit)
    return data


@application.get("/")
async def coronavirus(request: Request, city: str = None, skip: int = 0, limit: int = 34):
    # limit 34 默认获取最新的34个省/直辖市
    data = await crud.get_data(city=city, skip=skip, limit=limit)
    if not data:
        data = {}
    return templates.TemplateResponse("home.html", {
        "request": request,
        "data": data,
        "sync_data_url": "/coronavirus/sync_coronavirus_data/jhu"
    })


async def bg_task(url: HttpUrl):
    '''这里注意一个坑，不要在后台任务函数的参数中db：Session = Depends(get_db)这样导入依赖'''
    client = httpx.AsyncClient()
    city_data = await client.get(url=f"{url}?source=jhu&country_code=CN&timelines=false")
    if city_data.status_code == 200:
        await City.all().delete() # 同步数据前先清空原有数据
        city_locations = city_data.json()['locations']
        for location in city_locations:
            city = {
                "province": location['province'],
                "country": location['country'],
                "country_code": "CN",
                "country_population": location['country_population']
            }
            await crud.create_city(city=schemas.CreateCity(**city))

    coronavirus_data = await client.get(url=f"{url}?source=jhu&country_code=CN&timelines=true")
    if coronavirus_data.status_code == 200:
        await Data.all().delete()  # 同步数据前先清空原有数据
        data_locations = coronavirus_data.json()['locations']
        for data in data_locations:
            db_city = await crud.get_city_by_name(name=data['province'])
            for date, confirmed in data['timelines']['confirmed']['timeline'].items():
                db_data = {
                    "date": date.split('T')[0],  # 把'2020-12-31T00:00:00Z' 变成 ‘2020-12-31’
                    "confirmed": confirmed,
                    "deaths": data['timelines']['deaths']['timeline'][date],
                    "recovered": 0
                }
                # 这个city_id是city表中的主键ID，不是coronavirus_data数据里的ID
                await crud.create_city_data(data=schemas.CreateData(**db_data), city_id=db_city.id)

    await client.aclose()


@application.get('/sync_coronavirus_data/jhu')
async def async_coronavirus_data(background_tasks: BackgroundTasks):
    '''从Johns Hopkins University同步COVID-19数据'''
    background_tasks.add_task(bg_task, 'https://coronavirus-tracker-api.herokuapp.com/v2/locations')
    return {"message": "正在后台同步数据..."}
