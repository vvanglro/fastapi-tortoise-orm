# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:run.py
@time:2021/04/24
"""
import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

from tutorial import app03,app04,app05,app06,app07,app08

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="FastAPI (Python)",
    description="FastAPI Framework, high performance, <br>"
                "easy to learn, fast to code, ready for production",
    version="1.0",
    openapi_url="/openapi.json",
)


# 注册捕获异常
# register_exception(app)
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])



#定义异常方法
class NormalException(Exception):
    def __init__(self, code: int, message: str):
            self.message = message
            self.code = code

@app.exception_handler(NormalException)
async def unicorn_exception_handler(request: Request, exc: NormalException):
  return JSONResponse(
     status_code=200,
     content={
        "code": "your code",
        "message": "your message",
        },
  )



# @app.exception_handler(Exception)
# async def validation_exception_handler(request, exc):
#     print(dir(request))
#     print(request.url.path)
#     print(exc.body)
#     print(exc.args)
#     print(dir(exc))
#     print(exc.errors()[0]['msg'])
#     # print(f"OMG! The client sent invalid data!: {exc}")
#     return await request_validation_exception_handler(request, exc)

if __name__ == '__main__':

    uvicorn.run('run:app', host='0.0.0.0', port=9090, reload=True, debug=True,workers=1)