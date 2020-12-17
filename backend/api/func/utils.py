import hashlib
import uuid
from datetime import datetime, timezone,timedelta

from .db import USER


def auth(username: str, session: str):
    auth_record = USER.get_or_none(USER.studentID == username)
    if session == auth_record.session:
        if timenow() - auth_record.sessioncreated < timedelta(days=15):  # 15天
            return [4, "session 有效"]
        else:
            return [5, "session 失效"]
    else:
        return [3, "session 错误"]


def getMD5(encryptstr: str):
    return hashlib.md5(encryptstr.encode()).hexdigest()

def getSession():
    return getMD5(str(uuid.uuid4()))

def timenow():
    return datetime.now()
