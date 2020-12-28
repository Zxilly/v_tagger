import json
import uuid

from fastapi import HTTPException

from .db import *
from .utils import auth as auth2
from .utils import getSession, timenow


def login(username: str, auth_code: str):
    user_record = USER.get_or_none(USER.studentID == username)
    if user_record:
        if user_record.authCode == auth_code:
            user_record.session = getSession()
            user_record.sessioncreated = timenow()
            user_record.save()
            return [0, "登陆成功", user_record.session]
        else:
            return [2, "密码错误"]
    else:
        return [1, "用户未找到"]


def auth(username: str, session: str):
    return auth2(username, session)


def reg(username: str, authcode: str, regcode: str):
    session = getSession()
    with open('config.json', 'r') as f:
        if regcode != json.loads(f.read())['regcode']:
            raise HTTPException(status_code=403, detail="Wrong RegCode")
    if not USER.get_or_none(USER.studentID == username):
        USER.create(studentID=username,
                    ID=uuid.uuid4(),
                    tagCount=0,
                    role=0,
                    authCode=authcode,
                    info=json.dumps({}),
                    session=session,
                    sessioncreated=timenow())
        return [7, "注册成功", session]
    else:
        return [6, "用户已存在"]
