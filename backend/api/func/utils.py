import hashlib
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import ffmpeg
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

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


def update_database():
    if db.is_closed():
        init()
    records = VIDEO.select().where(True)
    for record in records:
        json_value = json.loads(record.info)
        if "items" in json_value.keys():
            continue
        clips = json_value.pop("clips")
        conjunctions = json_value.pop("conjunctions")
        full = json_value.pop("full") if "full" in json_value.keys() else ""

        if record.tagstatus == 0:
            json_value["items"] = []
        else:
            json_value["items"] = [{
                "clips": clips,
                "conjunctions": conjunctions,
                "full": full
            }]

        record.info = json.dumps(jsonable_encoder(json_value))
        record.markstatus = 0

        record.save()
    db.close()


def needAuth(username: str, session: str, func):
    if auth(username, session)[0] == 4:
        return func()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


def getMD5(encryptstr: str):
    return hashlib.md5(encryptstr.encode()).hexdigest()


def getBinaryMD5(encryptbyte: bytes):
    return hashlib.md5(encryptbyte).hexdigest()


def getSession():
    return getMD5(str(uuid.uuid4()))


def timenow():
    return datetime.now()


def getRegCode():
    with open('config.json', 'r') as f:
        return json.loads(f.read())['regcode']
