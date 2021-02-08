import hashlib
import json
import uuid

from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

import ffmpeg
from fastapi import HTTPException

from .db import USER, VIDEO, db
from .init import init


def auth(username: str, session: str):
    auth_record = USER.get_or_none(USER.studentID == username)
    if auth_record and session == auth_record.session:
        if timenow() - auth_record.sessioncreated < timedelta(days=15):  # 15天
            return [4, "session 有效"]
        else:
            return [5, "session 失效"]
    else:
        return [3, "session 错误"]


def searchpath(path: str):
    if db.is_closed():
        init()
    handle_count = 0
    ignore_count = 0
    basepath = Path(path)
    if not basepath.is_dir():
        raise Exception("Argument is not a dir.")
    files_in_basepath = (entry for entry in basepath.iterdir() if entry.is_file())
    for item in files_in_basepath:
        if item.name.split(".")[-1] in ['mp4']:
            print(item.name)
            with item.open(mode="rb") as f:
                fileMD5 = getBinaryMD5(f.read(1024 * 200))
            if VIDEO.get_or_none(VIDEO.hash == fileMD5):
                ignore_count += 1
                continue
            probe = ffmpeg.probe(filename=item.absolute())
            video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            try:
                video_length = video_info['duration']
            except KeyError:
                ignore_count += 1
                continue
            info = {
                "length": round(float(video_length), 1),
                "clips": [],
                "conjunctions": []
            }
            item.resolve()
            item.rename(str(item.parents[0]) + '/' + fileMD5 + '.mp4')
            # shutil.copyfile(item.absolute(), '../data/' + fileMD5 + '.mp4')
            VIDEO.create(hash=fileMD5, info=json.dumps(info), tagstatus=False, markstatus=False)
            handle_count += 1
    print("Handle %d files and ignore %d files" % (handle_count, ignore_count))


def needAuth(username: str, session: str, func):
    if auth(username, session)[0] == 4:
        return func()
    else:
        raise HTTPException(status_code=403, detail="Fobidden")


def getMD5(encryptstr: str):
    return hashlib.md5(encryptstr.encode()).hexdigest()


def getBinaryMD5(encryptbyte: bytes):
    return hashlib.md5(encryptbyte).hexdigest()


def getSession():
    return getMD5(str(uuid.uuid4()))


def timenow():
    return datetime.now()
