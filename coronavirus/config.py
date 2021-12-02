from typing import Optional

from starlette.config import Config
from starlette.datastructures import Secret

config = Config('.env')

DEBUG: bool = config('DEBUG', cast=bool, default=False)

# mysql
DB_NAME: str = config('MYSQL_DATABASE', cast=str, default='async_coronavirus')
DB_USER: Optional[str] = config('MYSQL_USER', cast=str, default='root')
DB_PASSWORD: Optional[Secret] = config('MYSQL_PASSWORD', cast=Secret, default=None)
DB_ROOT_PASSWORD: Optional[Secret] = config('MYSQL_ROOT_PASSWORD', cast=Secret, default=None)
REDIS_PASSWORD: Optional[Secret] = config('REDIS_PASSWORD', cast=Secret, default=None)
