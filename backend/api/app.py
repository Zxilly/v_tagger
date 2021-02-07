from typing import List

import uvicorn
from fastapi import FastAPI, Body, Query, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from func import user, init, db, video, utils, model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.mount("/video/data", StaticFiles(directory="../data/"), name="static")


# Just for test, uvicorn not support range request. Will use nginx to serve the files in the release.

@app.on_event("startup")
def startup():
    init.init()


@app.on_event("shutdown")
def shutdown():
    if not db.db.is_closed():
        db.db.close()


@app.get("/")
async def root():
    return "There is nothing here."


@app.post('/user/reg')
async def user_reg(username: str = Query(...),
                   authcode: str = Body(..., embed=True),
                   regcode: str = Body(..., embed=True)
                   ):
    return user.reg(username, authcode, regcode)


@app.post("/user/login")
async def user_login(username: str = Query(...),
                     authcode: str = Body(..., embed=True)
                     ):
    return user.login(username, authcode)


@app.post('/user/auth')
async def user_auth(username: str = Query(...),
                    session: str = Header(...)
                    ):
    return user.auth(username, session)


@app.post('/video/add')
async def video_add(
        username: str = Query(...),
        session: str = Header(...),
        videos: List[model.video] = Body(..., embed=True)
):
    if utils.auth(username, session)[0] == 4:
        return video.add(videos)
    else:
        raise HTTPException(status_code=403, detail="Fobidden")


@app.get('/video/gethash')
async def video_getinfo(
        username: str = Query(...),
        session: str = Header(...)
):
    if utils.auth(username, session)[0] == 4:
        return video.gethash()
    else:
        raise HTTPException(status_code=403, detail="Fobidden")


@app.get('/video/getinfo')
async def video_getinfo(username: str = Query(...),
                        hashv: str = Query(...),
                        session: str = Header(...),
                        ):
    if utils.auth(username, session)[0] == 4:
        return video.getinfo(hashv)
    else:
        raise HTTPException(status_code=403, detail="Fobidden")


@app.post('/video/setinfo')
async def video_getinfo(username: str = Query(...),
                        session: str = Header(...),
                        info: model.setInfo = Body(...),
                        tagstatus: bool = Body(False, embed=True)
                        ):
    if utils.auth(username, session):
        return video.setinfo(info, tagstatus)
    else:
        raise HTTPException(status_code=403, detail="Fobidden")


@app.get('/video/gettags')
async def video_gettags():
    return video.gettags()


if __name__ == '__main__':
    uvicorn.run('app:app', port=23333, debug=True)
