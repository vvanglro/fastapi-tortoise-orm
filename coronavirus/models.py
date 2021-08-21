# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:49
# @Author  : wanghao
# @File    : models.py
# @Software: PyCharm
from tortoise.models import Model
from tortoise import fields


class BaseModel(Model):
    id = fields.IntField(pk=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, description='更新时间')

    class Meta:
        abstract = True


class City(BaseModel):
    province = fields.CharField(max_length=100, unique=True, nullable=False, description='省/直辖市')
    country = fields.CharField(max_length=100, nullable=False, description='国家')
    country_code = fields.CharField(max_length=100, nullable=False, description='国家代码')
    country_population = fields.BigIntField(nullable=False, description='国家人口')

    class Meta:
        table = "city"
        ordering = ["country_code"]


class Data(BaseModel):
    date = fields.DateField(nullable=False, description='数据日期')
    confirmed = fields.BigIntField(default=0, nullable=False, description='确诊数量')
    deaths = fields.BigIntField(default=0, nullable=False, description='死亡数量')
    recovered = fields.BigIntField(default=0, nullable=False, description='痊愈数量')
    city = fields.ForeignKeyField('models.City', related_name='data')

    class Meta:
        table = "data"
        ordering = ["-date"]
