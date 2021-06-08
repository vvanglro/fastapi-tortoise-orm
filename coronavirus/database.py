# -*- coding: utf-8 -*-
# @Time    : 2021/5/13 10:49
# @Author  : wanghao
# @File    : database.py
# @Software: PyCharm

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./coronavirus.sqlite3'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://username:password@host:port/database_name'  # mysql或者postgresql的连接方法

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://hulk:hulk@db:3306/coronavirus'  # mysql或者postgresql的连接方法

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf-8',
    # 由于sqlalchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可使用。这个参数只在用sqlite数据库时设置
    # connect_args={"check_same_thread":False}

    # pool_size: 连接池大小
    pool_size=10,
    # 连接回收时间，这个值必须要比数据库自身配置的interactive_timeout值小
    # 在MySQL中执行指令查看：
    # show variables like "interactive_timeout";
    pool_recycle=1600,
    # 预检测池中连接是否有效，并替换无效连接
    pool_pre_ping=True,
    # 使用后进先出的方式获取连接，允许多余连接保持空闲
    pool_use_lifo=True,
    # 会打印输出连接池的异常信息，帮助排查问题
    echo_pool=True,
    # 最大允许溢出连接池大小的连接数量
    max_overflow=5,
    # 将连接这个数据库引擎的所有执行语句打印出来
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    echo=True
)


'''
https://zhuanlan.zhihu.com/p/48994990 sqlalchemy的autoflush 和 autocommit
简单说，flush之后你才能在这个Session中看到效果，而commit之后你才能从其它Session中看到效果
简单说：
flush预提交，等于提交到数据库内存，还未写入数据库文件；
commit就是把内存里面的东西直接写入，可以提供查询了；
'''
# 在sqlalchemy中, CRUD都是通过会话(session)进行的, 所以我们必须要先创建会话, 每一个SessionLocal实例就是一个数据库session
# autoflush是指发送数据库语句到数据库, 但数据库不一定执行写入磁盘
# autocommit是指提交事务, 将变更保存到数据库文件
'''
expire_on_commit=True时, commit 之后所有实例都会过期.  (之后再访问这些过期实例的属性时，SQLAlchemy 会重新去数据库加载实例对应的数据记录)
上边括号里的话有问题  expire_on_commit=True时自己实验时commit后 在用同一个session访问属性时 sqlalchemy会报错
而expire_on_commit=False时在commit后 在访问这个session的属性时 不会报错 也不会去重新加载数据
expire_on_commit=True时的坑https://blog.csdn.net/qq_41359051/article/details/109124617
'''
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

# 创建基本的映射类
Base = declarative_base(bind=engine, name='Base')
