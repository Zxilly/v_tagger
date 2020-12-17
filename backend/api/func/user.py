from .db import *


def auth(username: str, authcode: str):
    user_record = USER.get(USER.studentID == username)
    if user_record:
        if user_record.authCode == authcode:
            return [0, "登陆成功"]
        else:
            return [2, "密码错误"]
    else:
        return [1, "用户未找到"]
