import hashlib
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import ffmpeg

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


def searchpath(path: str):
    basepath = Path(path)
    files_in_basepath = (entry for entry in basepath.iterdir() if entry.is_file())
    for item in files_in_basepath:
        if item.name.split(".")[-1] in ['mp4']:
            print(item.name)
            with item.open(mode="rb") as f:
                fileMD5 = getBinaryMD5(f.read(1024 * 200))
            tagger = []
            info = {
                "length": timedelta,

            }


def getMD5(encryptstr: str):
    return hashlib.md5(encryptstr.encode()).hexdigest()


def getBinaryMD5(encryptbyte: bytes):
    return hashlib.md5(encryptbyte).hexdigest()


def getSession():
    return getMD5(str(uuid.uuid4()))


def timenow():
    return datetime.now()
