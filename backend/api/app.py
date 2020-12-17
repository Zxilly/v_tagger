import json

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from func import login,init

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return "There is nothing here."


@app.post("/login/auth")
async def loginauth(username: str, authcode: str):
    return login.auth(username, authcode)


if __name__ == '__main__':
    init.init()
    uvicorn.run('app:app',port=23333,debug=True)