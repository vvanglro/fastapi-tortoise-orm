"""
@author:wanghao
@file:chapter05.py
@time:2021/04/24
"""
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException

app05 = APIRouter()

'''Dependencies 创建 导入和声明依赖'''


async def common_parameters(q: Optional[str] = None, page: int = 1, limit: int = 10):
    return {'q': q, 'page': page, 'limit': limit}


@app05.get('/dependency01')
# 使用Depends将common_parameters方法用作依赖 代码的复用
async def dependency01(commons: dict = Depends(common_parameters)):
    return commons


@app05.get('/dependency02')
# 可以在async def中调用def依赖， 也可以在def中导入async def依赖
def dependency02(commons: dict = Depends(common_parameters)):
    return commons


'''Classes as Dependencies 类作为依赖性'''

fake_items_db = [
    {'item_name': 'Foo'}, {
        'item_name': 'Bar',
    }, {'item_name': 'Hulk'},
]


class CommonQueryParams:

    def __init__(self, q: Optional[str] = None, page: int = 1, limit: int = 10):
        self.q = q
        self.page = page
        self.limit = limit


@app05.get('/classes_as_dependencies')
# async def classes_as_dependencies(commons: CommonQueryParams = Depends(CommonQueryParams))  # 类做为依赖的写法一
# async def classes_as_dependencies(commons: CommonQueryParams = Depends()) # 类做为依赖的写法二
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):  # 类做为依赖的写法三
    response = {}
    if commons.q:
        response.update({'q': commons.q})
    items = fake_items_db[commons.page: commons.limit]
    response.update({'items': items})
    return response


'''Sub-dependencies 子依赖'''


def query(q: Optional[str] = None):
    return q


def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if not q:
        return last_query
    return q


@app05.get('/sub_dependency')
async def sub_dependency(final_query: str = Depends(sub_query, use_cache=True)):
    '''user_cache默认是True， 表示当多个依赖有一个共同的子依赖时， 每次request请求只会调用子依赖一次，多次调用将从缓存中获取'''
    return {'sub_dependency': final_query}


'''Dependencies in path operation decorators 路径操作装饰器中的多依赖'''


async def verify_token(x_token: str = Header(...)):
    '''没有返回值的子依赖'''
    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')
    # return x_token


async def verify_key(x_key: str = Header(...)):
    '''有返回值的子依赖，但是返回值不会被调用'''
    if x_key != 'fake-super-secret-key':
        raise HTTPException(status_code=400, detail='X-Key header invalid')
    return x_key


@app05.get(
    '/depandency_in_path_operation',
    dependencies=[Depends(verify_token), Depends(verify_key)],
)  # 这时候不是在函数参数中调用依赖，而是在路径操作中
async def depandency_in_path_operation():
    return [{'user': 'user01'}, {'user': 'user02'}]


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ''):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker('bar')


@app05.get('/query-checker/')
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {'fixed_content_in_query': fixed_content_included}


'''Global Dependencies 全局依赖'''

# 对于app05这个路由下的接口都进行依赖的验证  例如可以验证token 等
# app05 =APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])


'''Dependencies with yield 带yield的依赖'''
# 这个需要python3.7才支持， python3.6需要pip install async-exit-stack async-generator
# 以下是伪代码


async def get_db():
    db = 'db_connection'
    try:
        yield db
    finally:
        db.endswith('db_close')


async def dependency_a():
    dep_a = 'generate_dep_a()'
    try:
        yield dep_a
    finally:
        dep_a.endswith('db_close')


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = 'generate_dep_b'
    try:
        yield dep_b
    finally:
        dep_b.endswith(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = 'generate_dep_c'
    try:
        yield dep_c
    finally:
        dep_c.endswith(dep_b)
