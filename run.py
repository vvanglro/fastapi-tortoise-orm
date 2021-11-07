"""
@author:wanghao
@file:run.py
@time:2021/04/24
"""
import time

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from coronavirus import application
from coronavirus.config import DEBUG
from coronavirus.database import DATABASE_URL
from coronavirus.schemas import MsgResponse
from tutorial import app03
from tutorial import app04
from tutorial import app05
from tutorial import app06
from tutorial import app07
from tutorial import app08

app_kwargs = {
    'title': 'FastAPI (Python)',
    'debug': DEBUG,
    'version': '1.0',
    'description': 'FastAPI Framework, high performance, <br>'
                   'easy to learn, fast to code, ready for production',
}
if not DEBUG:
    app_kwargs.update(
        {'redoc_url': None, 'docs_url': None, 'openapi_url': None},
    )
app = FastAPI(**app_kwargs)

# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
# .mount()不要在分路由APIRouter().mount()调用，模板会报错
app.mount(
    path='/coronavirus/static',
    app=StaticFiles(directory='./coronavirus/static'), name='static',
)


# 中间件
@app.middleware('http')
# call_next将接收request请求作为参数
async def add_process_time_header(request: Request, call_next):
    # 计算每个请求的响应时间
    start_time = time.time()
    # 处理每个请求
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)  # 添加自定义的以"X-"开头的请求头
    return response


app.add_middleware(
    CORSMiddleware,
    #  允许跨域的列表
    allow_origins=[
        '*',
    ],
    # 允许使用证书
    allow_credentials=True,
    # 允许跨域的请求方法
    allow_methods=['*'],
    # 设置允许跨域的headers
    allow_headers=['*'],
)

if not DEBUG:
    app.include_router(
        application, prefix='/coronavirus',
        tags=['新冠病毒疫情跟踪器API'],
    )
else:
    app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
    app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
    app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
    app.include_router(app06, prefix='/chapter06', tags=['第六章 安全、认证和授权'])
    app.include_router(
        app07, prefix='/chapter07',
        tags=['第七章 FastAPI的数据库操作和多应用的目录结构设计'],
    )
    app.include_router(
        app08, prefix='/chapter08',
        tags=['第八章 中间件、CORS、后台任务、测试用例'],
    )
    app.include_router(
        application, prefix='/coronavirus',
        tags=['新冠病毒疫情跟踪器API'],
    )


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
            'code': 'your code',
            'message': 'your message',
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

@app.on_event('startup')
async def init_orm() -> None:  # pylint: disable=W0612
    await Tortoise.init(db_url=DATABASE_URL, modules={'models': ['coronavirus.models']}, timezone='Asia/Shanghai')


@app.on_event('shutdown')
async def close_orm() -> None:  # pylint: disable=W0612
    await Tortoise.close_connections()


# register_tortoise(
#     app,
#     config={
#         'connections': {
#             'default': DATABASE_URL
#         },
#         "apps": {
#             "models": {
#                 "models": ["coronavirus.models"],
#                 "default_connection": "default",
#             }
#         },
#         'use_tz': False,
#         'timezone': 'Asia/Shanghai'
#     },
#     generate_schemas=False,
#     add_exception_handlers=True,
# )

if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=9091, reload=True, debug=True, workers=1, log_config='log-config.json')
