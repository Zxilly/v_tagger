import json
from functools import lru_cache

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from peewee import fn

from .db import VIDEO
from .model import setInfo


def add(videos):
    all_num = len(videos)
    success = 0
    failed = 0
    for one in videos:
        if not VIDEO.get_or_none(VIDEO.hash == one.hash):
            info = {
                "length": one.length,
                "items": []
            }
            VIDEO.create(hash=one.hash, info=json.dumps(info), tagstatus=0, markstatus=0)
            success += 1
        else:
            failed += 1
            continue
    if success + failed != all_num:
        raise HTTPException(status_code=503, detail="WTF happened.")
    return [11, f"上传成功{success}个，忽略{failed}个"]


def getinfo(hashv):
    record = VIDEO.select().where(VIDEO.hash == hashv)
    if record.count() == 0:
        raise HTTPException(status_code=404, detail="Can not find the corresponding video.")
    return_value = {
        'hash': record[0].hash,
        'info': json.loads(record[0].info),
        'tagstatus': record[0].tagstatus
    }
    return [8, "获取成功", return_value]


def gethash():
    if VIDEO.select().where(VIDEO.tagstatus < 5).count() == 0:
        raise HTTPException(status_code=503, detail="No more video to tag.")
    rand_record = VIDEO.select().where(VIDEO.tagstatus == 0).order_by(fn.Rand()).limit(1)[0]
    return [10, "获取成功", rand_record.hash]


def setinfo(info: setInfo, tagstatus: bool, markstatus: bool):
    record = VIDEO.get_or_none(VIDEO.hash == info.hash)
    if not record:
        raise HTTPException(status_code=404, detail="Can not find the corresponding video to tag.")
    else:
        reqinfo = {
            "clips": info.clips,
            "conjunctions": info.conjunctions,
            "full": info.full
        }
        # print(info.clips)
        current_info = json.loads(record.info)
        current_info["items"].append(reqinfo)
        record.info = json.dumps(jsonable_encoder(current_info))
        record.tagstatus = tagstatus
        record.markstatus = markstatus
        record.save()
        return [9, "保存成功"]


def getsentencehash():
    if VIDEO.select().where(VIDEO.markstatus < VIDEO.tagstatus).count() == 0:
        raise HTTPException(status_code=503, detail="No more sentence to mark.")
    rand_record = \
        VIDEO.select().where(VIDEO.markstatus < VIDEO.tagstatus).order_by(fn.Rand()).limit(1)[0]
    return [10, "获取成功", rand_record.hash]


@lru_cache()
def gettags():
    with open('tag.json', 'r', encoding='UTF-8') as f:
        tags = json.loads(f.read())

    return tags
