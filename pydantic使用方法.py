# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:pydantic使用方法.py
@time:2021/04/23
"""
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, ValidationError

"""
Data validation and settings management using python type annotations.
使用Python的类型注解来进行数据校验和settings管理

pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
Pydantic可以在代码运行时提供类型提示，数据校验失败时提供友好的错误提示

Define how data should be in pure, canonical python; validate it with pydantic.
定义数据应该如何在纯规范的Python代码中保存，并用Pydantic验证它
"""
# 插件好像搜索不到了
print("\033[31m1. --- Pydantic的基本用法。Pycharm可以安装Pydantic插件 ---\033[0m")

class User(BaseModel):
    id: int  # 类型为int的 必填字段
    name: str = 'hulk'  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None  # 使用Optional来设置为选填字段，不填则为None
    friends: List[int] = []  # 列表中的元素是int类型或者可以直接转换成int类型


external_date = {
    "id": "123",
    "signup_ts": "2021-04-23 21:58",
    "friends": [1, 2, '3']  # '3'是可以int('3')的
}

user = User(**external_date)
print(user.id, user.friends)  # 实例化后调用属性
print(type(user.signup_ts))
print(type(repr(user.signup_ts)))
print(repr(user.signup_ts))   # repr函数将datetime类型的数据转换为str类型

print(user.dict())  # 将实例化后的对象转换为dict输出


print("\033[31m2. --- 校验失败处理 ---\033[0m")
try:
    User(id=1, signup_ts=datetime.today(), friends=[1,2, 'not number'])
except ValidationError as e:
    print(e.json())


print("\033[31m3. --- 模型类的属性和方法 ---\033[0m")
print(user.dict())
print(user.json())
print(user.copy())  # 这里是浅拷贝
# 下边是模型类自带的方法
print(User.parse_obj(obj=external_date)) #解析一个对象数据
print(User.parse_raw('{"id":"123","signup_ts":"2021-04-23 22:52","friends":[1,2,3]}'))  # 解析原始数据

# 使用pathlib库写入文件
path = Path('data.json')
path.write_text('{"id":"123","signup_ts":"2021-04-23 22:52","friends":[1,2,3]}')
print(User.parse_file(path)) # 解析一个文件数据

# 输出更详细的数据类型信息
print(user.schema())  #字典类型
print(type(user.schema()))
print(user.schema_json())   # json类型
print(type(user.schema_json()))

user_data =  {"id":"qwer","signup_ts":"2021-04-23 22:52","friends":[1,2,3]}
# construct方法不校验数据 直接创建模型类  不建议在construct方法中传入未经验证的数据
print(User.construct(**user_data))

# 定义模型类的时候, 所有字段都注明类型，字段顺序就不会乱
print(User.__fields__.keys())  # 输出模型类中所有的字段