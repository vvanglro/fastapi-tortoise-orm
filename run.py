# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:run.py
@time:2021/04/24
"""
import uvicorn
from fastapi import FastAPI
from tutorial import app03,app04,app05,app06,app07,app08

app = FastAPI()

app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])



if __name__ == '__main__':

    uvicorn.run('run:app', host='0.0.0.0', port=9090, reload=True, debug=True,workers=1)