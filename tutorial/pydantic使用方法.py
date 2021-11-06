"""
@author:wanghao
@file:pydantic使用方法.py
@time:2021/04/23
"""
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import constr
from pydantic import ValidationError
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

"""
Data validation and settings management using python type annotations.
使用Python的类型注解来进行数据校验和settings管理

pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
Pydantic可以在代码运行时提供类型提示，数据校验失败时提供友好的错误提示

Define how data should be in pure, canonical python; validate it with pydantic.
定义数据应该如何在纯规范的Python代码中保存，并用Pydantic验证它
"""
# 插件好像搜索不到了
print('\033[31m1. --- Pydantic的基本用法。Pycharm可以安装Pydantic插件 ---\033[0m')


class User(BaseModel):
    id: int  # 类型为int的 必填字段
    name: str = 'hulk'  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None  # 使用Optional来设置为选填字段，不填则为None
    friends: List[int] = []  # 列表中的元素是int类型或者可以直接转换成int类型


external_date = {
    'id': '123',
    'signup_ts': '2021-04-23 21:58',
    'friends': [1, 2, '3'],  # '3'是可以int('3')的
}

user = User(**external_date)
print(user.id, user.friends)  # 实例化后调用属性
print(type(user.signup_ts))
print(type(repr(user.signup_ts)))
print(repr(user.signup_ts))   # repr函数将datetime类型的数据转换为str类型

print(user.dict())  # 将实例化后的对象转换为dict输出


print('\033[31m2. --- 校验失败处理 ---\033[0m')
try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, 'not number'])
except ValidationError as e:
    print(e.json())


print('\033[31m3. --- 模型类的属性和方法 ---\033[0m')
print(user.dict())
print(user.json())
print(user.copy())  # 这里是浅拷贝
# 下边是模型类自带的方法
print(User.parse_obj(obj=external_date))  # 解析一个对象数据
print(
    User.parse_raw(
        '{"id":"123","signup_ts":"2021-04-23 22:52","friends":[1,2,3]}',
    ),
)  # 解析原始数据

# 使用pathlib库写入文件
path = Path('data.json')
path.write_text(
    '{"id":"123","signup_ts":"2021-04-23 22:52","friends":[1,2,3]}',
)
print(User.parse_file(path))  # 解析一个文件数据

# 输出更详细的数据类型信息
print(user.schema())  # 字典类型
print(type(user.schema()))
print(user.schema_json())   # json类型
print(type(user.schema_json()))

user_data = {
    'id': 'qwer',
    'signup_ts': '2021-04-23 22:52', 'friends': [1, 2, 3],
}
# construct方法不校验数据 直接创建模型类  不建议在construct方法中传入未经验证的数据
print(User.construct(**user_data))

# 定义模型类的时候, 所有字段都注明类型，字段顺序就不会乱
print(User.__fields__.keys())  # 输出模型类中所有的字段


print('\033[31m4. --- 递归模型 ---\033[0m')


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]  # 不同的狗有不同的叫声。递归模型（Recursive Models）就是指一个嵌套一个


dogs = Dog(
    birthday=date.today(), weight=6.66, sound=[
        {'sound': 'wang wang ~'}, {'sound': 'ying ying ~'},
    ],
)
print(dogs.dict())

print('\033[31m5. --- ORM模型：从类实例创建符合ORM对象的模型  ---\033[0m')

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    id: int
    # pydantic的constr限制字段长度
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        # 表示将pydantic模型类与orm模型类关联起来
        orm_mode = True


co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    name='Testing',
    domains=['example.com', 'foobar.com'],
)

print(CompanyModel.from_orm(co_orm))

# 官方文档：https://pydantic-docs.helpmanual.io/usage/types/
print('\033[31m6. --- Pydantic支撑的字段类型  ---\033[0m')
