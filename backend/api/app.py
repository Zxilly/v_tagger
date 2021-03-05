import time
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Body, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from func import user, init, db, video, utils, model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()

    if not db.db.is_connection_usable():
        db.db.connect()

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)



    return response


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


@app.get("/regcode")
async def regcode(
        username: str = Query(...),
        session: str = Header(...)
):
    return utils.needAuth(username, session, lambda: utils.getRegCode())


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
    # if utils.auth(username, session)[0] == 4:
    #     return video.add(videos)
    # else:
    #     raise HTTPException(status_code=403, detail="Fobidden")
    return utils.needAuth(username, session, lambda: video.add(videos))


@app.get('/video/gethash')
async def video_getinfo(
        username: str = Query(...),
        session: str = Header(...)
):
    # if utils.auth(username, session)[0] == 4:
    #     return video.gethash()
    # else:
    #     raise HTTPException(status_code=403, detail="Fobidden")
    return utils.needAuth(username, session, lambda: video.gethash())


@app.get('/video/getinfo')
async def video_getinfo(username: str = Query(...),
                        hashv: str = Query(...),
                        session: str = Header(...),
                        ):
    # if utils.auth(username, session)[0] == 4:
    #     return video.getinfo(hashv)
    # else:
    #     raise HTTPException(status_code=403, detail="Fobidden")
    return utils.needAuth(username, session, lambda: video.getinfo(hashv))


@app.post('/video/setinfo')
async def video_getinfo(username: str = Query(...),
                        session: str = Header(...),
                        info: model.setInfo = Body(...),
                        tagstatus: Optional[bool] = Body(False, embed=True),
                        markstatus: Optional[bool] = Body(False, embed=True)
                        ):
    # if utils.auth(username, session):
    #     return video.setinfo(info, tagstatus, markstatus)
    # else:
    #     raise HTTPException(status_code=403, detail="Fobidden")
    return utils.needAuth(username, session, lambda: video.setinfo(info, tagstatus, markstatus))


@app.get('/video/getsentencehash')
async def video_getsentencehash(
        username: str = Query(...),
        session: str = Header(...)
):
    # if utils.auth(username, session):
    #     return video.getsentencehash()
    # else:
    #     raise HTTPException(status_code=403, detail="Fobidden")
    return utils.needAuth(username, session, lambda: video.getsentencehash())


@app.get('/video/gettags')
async def video_gettags():
    return video.gettags()


if __name__ == '__main__':
    uvicorn.run('app:app', port=14562, debug=False)
