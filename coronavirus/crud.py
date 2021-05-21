# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:51
# @Author  : wanghao
# @File    : schemas.py
# @Software: PyCharm

from sqlalchemy.orm import Session
from coronavirus import models, schemas


def get_city(db: Session, city_id: int):
    # 根据城市id查询第一条数据
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, name: str):
    # 根据城市名字查询数据
    return db.query(models.City).filter(models.City.province == name).first()


def get_cities(db: Session, skip: int=0, limit: int =10):
    # 查询默认0-10的数据
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CreateCity):
    # 创建城市
    db_city =  models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_name: str,city: schemas.CreateCity):
    # 更新城市信息
    db_city = db.query(models.City).filter(models.City.province == city_name).update(city.dict())
    db.commit()
    return db_city


def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    # 获取数据
    if city:
        # 外键关联查询
        # models.Data.city.has(province=city)  从Data模型里relationship关联的City模型
        # 使用has筛选关联的City模型中的条件 https://www.osgeo.cn/sqlalchemy/orm/internals.html?highlight=has#sqlalchemy.orm.RelationshipProperty.Comparator.has
        return db.query(models.Data).filter(models.Data.city.has(province=city)).limit(5)
    return db.query(models.Data).offset(skip).limit(limit).all()


def create_city_data(db: Session, data: schemas.CreateData, city_id:int):
    # 创建数据
    db_data = models.Data(**data.dict(), city_id=city_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
