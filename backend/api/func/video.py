import json
from functools import lru_cache

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from peewee import fn

from .db import VIDEO
from .model import setInfo


def add(videos):
    all = len(videos)
    success = 0
    failed = 0
    for one in videos:
        record = VIDEO.select().where(VIDEO.hash == one.hash)
        if not VIDEO.get_or_none(VIDEO.hash == one.hash):
            info = {
                "length": one.length,
                "clips": [],
                "conjunctions": []
            }
            VIDEO.create(hash=one.hash, info=json.dumps(info), tagstatus=False)
            success += 1
        else:
            failed += 1
            continue
    if success + failed != all:
        raise HTTPException(status_code=503, detail="WTF happened.")
    return [11, f"上传成功{success}个，忽略{failed}个"]


def getinfo(hashv):
    record = VIDEO.select().where(VIDEO.hash == hashv)
    if record.count() == 0:
        raise HTTPException(status_code=404, detail="Can not find the corresponding video.")
    return_value = {
        'hash': record[0].hash,
        'info': json.loads(record[0].info)
    }
    return [8, "获取成功", return_value]


def gethash():
    if VIDEO.select().where(VIDEO.tagstatus == 0).count() == 0:
        raise HTTPException(status_code=503, detail="No more video to tag.")
    rand_record = VIDEO.select().where(VIDEO.tagstatus == 0).order_by(fn.Rand()).limit(1)[0]
    return [10, "获取成功", rand_record.hash]


def setinfo(info: setInfo, tagstatus: bool):
    record = VIDEO.get_or_none(VIDEO.hash == info.hash)
    if not record:
        raise HTTPException(status_code=404, detail="Can not find the corresponding video to tag.")
    else:
        reqinfo = {
            "length": info.length,
            "clips": info.clips,
            "conjunctions": info.conjunctions
        }
        # print(info.clips)
        record.info = json.dumps(jsonable_encoder(reqinfo))
        record.tagstatus = tagstatus
        record.save()
        return [9, "保存成功"]


@lru_cache()
def gettags():
    with open('tag.json', 'r', encoding='UTF-8') as f:
        tags = json.loads(f.read())
    # all_tags = []
    # for btype in tags.keys():
    #     # print(btype)
    #     for stype in tags[btype].keys():
    #         if not tags[btype][stype]:
    #             all_tags.append(btype + '-' + stype)
    #         else:
    #             for ttag in tags[btype][stype]:
    #                 all_tags.append(btype + '-' + stype + '-' + ttag)

    return tags
