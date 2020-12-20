import uvicorn
from fastapi import FastAPI, Body, Query, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.api.func import user, init, db, video, utils, model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def userreg(username: str = Query(...),
                  authcode: str = Body(..., embed=True)
                  ):
    return user.reg(username, authcode)


@app.post("/user/login")
async def userlogin(username: str = Query(...),
                    authcode: str = Body(..., embed=True)
                    ):
    return user.login(username, authcode)


@app.post('/user/auth')
async def userauth(username: str = Query(...),
                   session: str = Header(...)
                   ):
    return user.auth(username, session)


@app.get('/video/getinfo')
async def videogetinfo(username: str = Query(...),
                       session: str = Header(...)
                       ):
    if utils.auth(username, session) == 4:
        return video.getinfo()
    else:
        raise HTTPException(status_code=403, detail="Fobidden")


@app.post('/video/setinfo')
async def videogetinfo(username: str = Query(...),
                       session: str = Header(...),
                       info: model.setInfo = Body(...),
                       tagstatus: bool = Body(False, embed=True)
                       ):
    if utils.auth(username, session):
        return video.setinfo(info,tagstatus)
    else:
        raise HTTPException(status_code=403, detail="Fobidden")


if __name__ == '__main__':
    uvicorn.run('app:app', port=23333, debug=True)
