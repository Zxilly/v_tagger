import json

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from peewee import fn

from .db import VIDEO
from .model import setInfo


def getinfo():
    if VIDEO.select().where(VIDEO.tagstatus is False).count() == 0:
        raise HTTPException(status_code=503, detail="No more video to tag.")
    rand_record = VIDEO.select().where(VIDEO.tagstatus is False).order_by(fn.Rand()).limit(1)[0]
    return_value = {
        'hash': rand_record.hash,
        'info': json.loads(rand_record.info)
    }
    return [8, "获取成功", return_value]


def setinfo(info: setInfo, tagstatus: bool):
    record = VIDEO.get_or_none(VIDEO.hash == info.hash)
    if not record:
        raise HTTPException(status_code=500, detail="Can not find the video to tag.")
    else:
        repinfo = {
            "length": info.length,
            "clip": info.clip
        }
        record.info = jsonable_encoder(repinfo)
        record.tagstatus = tagstatus
        record.save()
        return [9, "保存成功"]
