# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:chapter08.py
@time:2021/04/24
"""
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends

app08 = APIRouter()

"""【见run.py】Middleware 中间件"""

# 注：带yield的依赖的退出部分的代码 和 后台任务 会在中间件之后运行

"""【见run.py】CORS (Cross-Origin Resource Sharing) 跨源资源共享"""

# 域的概念：协议+域名+端口


'''Background Tasks 后台任务'''

def bg_task(framework: str):
    with open('bg_task.md', mode='a', encoding='utf8') as f:
        f.write(f'## {framework} 后台任务写入测试')

@app08.post('/background_tasks')
async def run_bg_task(framework: str, background_task: BackgroundTasks):
    '''
    :param framework: 被调用的后台任务函数的参数
    :param background_task:  FastAPI.BackgroundTasks
    :return:
    '''
    # 调用后台任务函数bg_task  framework为bg_task函数接收的参数
    background_task.add_task(bg_task, framework)
    return {"message":"任务已在后台运行"}


def continue_write_readme(background_tasks: BackgroundTasks, q: Optional[str] = None):
    # q有值则执行后台任务函数
    if q:
        background_tasks.add_task(bg_task, '\n> dependency 依赖后台任务写入测试\n')
    # q没有值则返回默认None
    return q

@app08.post('/dependency/background_tasks')
async def dependency_run_bg_task(q: str = Depends(continue_write_readme)):
    # 如果传入了查询参数q 则会执行依赖函数里的后台任务
    if q:
        return {"message":"任务已在后台运行"}