import uvicorn
from fastapi import FastAPI, Body, Query
from fastapi.middleware.cors import CORSMiddleware

from func import user, init, db

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
                   session: str = Body(..., embed=True)
                   ):
    return user.auth(username, session)


if __name__ == '__main__':
    uvicorn.run('app:app', port=23333, debug=True)
