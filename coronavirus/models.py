# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:49
# @Author  : wanghao
# @File    : models.py
# @Software: PyCharm

from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base

class City(Base):
    __tablename__ = 'city'  # 表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Column(String(100), nullable=False, comment='国家')
    country_code = Column(String(100),  nullable=False, comment='国家代码')
    country_population = Column(BigInteger,  nullable=False, comment='国家人口')
    data = relationship('Data', back_populates='city')   # 'Data'是关联的类名; back_populates='city'来指定反向访问的属性名

    # server_default=func.now()设置默认值为当前时间
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    # onupdate=func.now()数据更新时更新时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(),comment='创建时间')

    __mapper_args__ = {"order_by":country_code}  # 默认是正序, 倒序加上country_code.desc()方法

    def __repr__(self):
        return f'{self.country}_{self.province}'

'''
default 和 server_default的 坑  默认值是sqlalchemy自动在内部添加进去表中的 所以生成表中的时候 表结构没有默认值
https://zhuanlan.zhihu.com/p/37892676
'''

class Data(Base):
    __tablename__ = 'data'  # 表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id', ondelete='CASCADE'), comment='所属省/直辖市') # ForeignKey里的字符串格式不是类名.属性名，而是表名.字段名
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
    deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
    recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
    city = relationship('City', back_populates='data')

    # server_default=func.now()设置默认值为当前时间
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    # onupdate=func.now()数据更新时更新时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(),comment='创建时间')

    __mapper_args__ = {"order_by":date.desc()}  # 默认是正序, 倒序加上date.desc()方法 按日期降序排列

    def __repr__(self):
        return f'{repr(self.date)}:确诊{self.confirmed}例'




""" 附上三个SQLAlchemy教程
SQLAlchemy的基本操作大全 
    http://www.taodudu.cc/news/show-175725.html
Python3+SQLAlchemy+Sqlite3实现ORM教程 
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html
SQLAlchemy基础知识 Autoflush和Autocommit
    https://zhuanlan.zhihu.com/p/48994990
"""
