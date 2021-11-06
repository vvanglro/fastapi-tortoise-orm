# @Time    : 2021/5/13 10:49
# @Author  : wanghao
# @File    : database.py
# @Software: PyCharm
from coronavirus.config import DB_NAME
from coronavirus.config import DB_PASSWORD
from coronavirus.config import DB_ROOT_PASSWORD
from coronavirus.config import DB_USER

if DB_USER == 'root':
    db_user = DB_USER
    db_password = DB_ROOT_PASSWORD
else:
    db_user = DB_USER  # type: ignore
    db_password = DB_PASSWORD


DATABASE_URL = f'mysql://{db_user}:{db_password}@db:3306/{DB_NAME}'

TORTOISE_ORM = {
    'connections': {'default': DATABASE_URL},
    'apps': {
        'models': {
            'models': ['aerich.models', 'coronavirus.models'],
            # 须添加“aerich.models” 后者“model”是上述model.py文件的路径
            'default_connection': 'default',
        },
    },
}
