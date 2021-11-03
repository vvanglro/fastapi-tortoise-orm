
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse

app = FastAPI()

# 定义异常方法
class NormalException(Exception):
    def __init__(self, code: int, message: str):
        self.message = message
        self.code = code


@app.exception_handler(NormalException)
async def unicorn_exception_handler(request: Request, exc: NormalException):
    print(request)
    print(exc)
    return JSONResponse(
        status_code=200,
        content={
            "code": "your code",
            "message": "your message",
        },
    )

# 捕获状态码为404的请求
@app.exception_handler(404)
async def handler_not_found(request: Request, exc):
    html = f"""
        <h1 style="color:red">请求资源不存在,请联系管理员</h1>
        <hr>
        <h3>当前请求的地址：{request.url}</h3>
    """
    return HTMLResponse(html,status_code=200)


# 捕获状态码为500的请求
@app.exception_handler(500)
async def handler_server_error(request: Request, exc):
    print(exc)
    print(dir(exc))
    print(type(str(exc)))
    print(exc.args)
    print(exc.with_traceback)

    print(request.url)
    return JSONResponse(
        status_code=200,
        content={
            "message": "服务器异常",
            "error": str(exc)
        },
    )

@app.get('/a')
async def func():
    raise NormalException(code=300,message='error')

@app.get('/b')
async def func():
    '''测试捕获状态码为500请求的'''
    r = 1/0
    return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='异常捕获:app', host="0.0.0.0", port=8001, reload=True)