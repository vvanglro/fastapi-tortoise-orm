"""
@author:wanghao
@file:__init__.py.py
@time:2021/04/24
"""
__author__ = 'hulk'
__version__ = '0.1.2'

from fastapi import APIRouter
from starlette.responses import RedirectResponse

from .main import application

router = APIRouter()
router.include_router(application, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])


@router.get('/')
async def redirect_url():
    url = router.url_path_for('coronavirus')
    return RedirectResponse(url=url)
