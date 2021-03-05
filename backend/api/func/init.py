import json
import random
import string
from contextvars import ContextVar

import peewee

from .db import db, USER, VIDEO


def init(quiet=True):
    checkstatus = False
    try:
        with open("config.json", 'r+') as f:
            config = json.loads(f.read())
        sqladdress = config['sqladdress']
        sqlport = config['sqlport']
        sqluser = config['sqluser']
        sqlpassword = config['sqlpassword']
        sqldbname = config['sqldbname']
    except FileNotFoundError:
        sqladdress, sqlport, sqluser, sqlpassword, sqldbname = infocollect()

    while not checkstatus:
        try:
            check(sqldbname, sqluser, sqlpassword, sqladdress, sqlport)
            db.connect()
            if not quiet:
                print("连接成功")
            config = {
                'sqladdress': sqladdress,
                'sqlport': sqlport,
                'sqluser': sqluser,
                'sqlpassword': sqlpassword,
                'sqldbname': sqldbname,
                'regcode': ''.join(random.sample(string.ascii_letters + string.digits, 8))
            }
            with open("config.json", 'w+') as f:
                f.write(json.dumps(config))
            db.create_tables([USER, VIDEO])
            checkstatus = True
        except Exception as e:
            if not quiet:
                print("连接失败： " + str(e) + " ，重试")
            sqladdress, sqlport, sqluser, sqlpassword, sqldbname = infocollect()


db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


def check(sqldbname, sqluser, sqlpassword, sqladdress, sqlport):
    db.init(sqldbname, user=sqluser, password=sqlpassword, host=sqladdress, port=sqlport, charset='utf8mb4')

    db._state = PeeweeConnectionState()


def infocollect():
    sqladdress = input("SQL地址是：")
    sqlport = int(input("SQL端口是："))
    sqluser = input("SQL用户是：")
    sqlpassword = input("SQL用户密码是：")
    sqldbname = input("指定给此程序的数据库是:")
    return sqladdress, sqlport, sqluser, sqlpassword, sqldbname
