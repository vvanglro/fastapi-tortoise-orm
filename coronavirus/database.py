# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:49
# @Author  : wanghao
# @File    : database.py
# @Software: PyCharm

DATABASE_URL = 'mysql://root:hulk@localhost:3306/async_coronavirus?charset=utf8'

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