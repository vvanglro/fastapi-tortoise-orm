# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:run.py
@time:2021/04/24
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from tutorial import app03, app04, app05, app06, app07, app08

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="FastAPI (Python)",
    description="FastAPI Framework, high performance, <br>"
                "easy to learn, fast to code, ready for production",
    version="1.0",
    openapi_url="/openapi.json",

    # 全局路由使用依赖验证
    # dependencies=[Depends(verify_token), Depends(verify_key)]
)

# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/coronavirus/static', app=StaticFiles(directory='./coronavirus/static'), name='static')

# @app.exception_handler(StarletteHTTPException)  # 重写HTTPException异常处理器
# async def http_exception_handler(request, exc):
#     '''
#     :param request: 这个参数不能省
#     :param exc:
#     :return:
#     '''
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
# @app.exception_handler(RequestValidationError)  # 重写请求验证异常处理器
# async def validation_exception_handler(request, exc):
#     '''
#     :param request:  这个参数不能省
#     :param exc:
#     :return:
#     '''
#     return PlainTextResponse(str(exc), status_code=400)


# 注册捕获异常
# register_exception(app)
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 安全、认证和授权'])
app.include_router(app07, prefix='/chapter07', tags=['第七章 FastAPI的数据库操作和多应用的目录结构设计'])


# 定义异常方法
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
    uvicorn.run('run:app', host='0.0.0.0', port=9090, reload=True, debug=True, workers=1)
