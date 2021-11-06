# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:49
# @Author  : wanghao
# @File    : database.py
# @Software: PyCharm
from coronavirus.config import DB_USER, DB_PASSWORD, DB_NAME

DATABASE_URL = f'mysql://{DB_USER}:{DB_PASSWORD}@db:3306/{DB_NAME}'

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["aerich.models", "coronavirus.models"],
          	# 须添加“aerich.models” 后者“model”是上述model.py文件的路径
            "default_connection": "default",
        },
    },
}