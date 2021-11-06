from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()
# https://www.bilibili.com/video/BV1Fi4y1w7iv?p=17

# 捕获请求验证错误 并重写返回


@app.exception_handler(RequestValidationError)
async def handler_server_error(request: Request, exc):
    # print(exc.errors()) # [{'loc': ('query', 'q'), 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}, {'loc': ('query', 'f'), 'msg': 'field required', 'type': 'value_error.missing'}]
    # print(exc.body)
    # print(exc.args)
    errors = {
        'value_error.missing': '该字段为必填',
        'type_error.integer': '该字段为整数',
    }

    resp_error_msg = {
        '.'.join(item['loc']): errors[item['type']]
        for item in exc.errors()
    }
    return JSONResponse(
        status_code=400,
        content={'resp_error_msg': resp_error_msg, 'success': False},
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='字段验证错误消息处理:app', host='0.0.0.0', port=8001, reload=True)
