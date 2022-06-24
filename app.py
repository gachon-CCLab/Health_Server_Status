from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
import requests, asyncio, logging



#버킷과 파일 이름은 여기서 결정된다. 다른 곳에서는 이 값을 받아와 사용
#
class ServerStatus(BaseModel):

    S3_bucket: str = 'fl-flower-model'
    S3_key: str = '' # 모델 가중치 파일 이름
    play_datetime: str = ''
    FLSeReady: bool = False
    GL_Model_V: int = 0 #모델버전 


app = FastAPI()

FLSe = ServerStatus()

@app.get("/FLSe/info")
def read_status():
    global FLSe
    print('Server_status: ')
    print(FLSe)
    print()
    return {"Server_Status": FLSe}


@app.put("/FLSe/FLSeUpdate")
def update_status(Se: ServerStatus):
    global FLSe
    FLSe = Se
    return {"Server_Status": FLSe}

@app.put("/FLSe/FLRoundFin")
def update_ready(FLSeReady: bool):
    global FLSe
    FLSe.FLSeReady = FLSeReady
    if FLSeReady==False:
        FLSe.GL_Model_V += 1
    return {"Server_Status": FLSe}

# @app.on_event("startup")
# def startup():
#     loop = asyncio.get_event_loop()
#     loop.set_debug(True)

#     loop.create_task(fl_server_check())

# def async_dec(awaitable_func):
#     async def keeping_state():
#         while True:
#             try:
#                 logging.debug(str(awaitable_func.__name__) + '함수 시작')
#                 # print(awaitable_func.__name__, '함수 시작')
#                 await awaitable_func()
#                 logging.debug(str(awaitable_func.__name__) + '_함수 종료')
#             except Exception as e:
#                 # logging.info('[E]' , awaitable_func.__name__, e)
#                 logging.error('[E]' + str(awaitable_func.__name__) + str(e))
#             await asyncio.sleep(1)
#     return keeping_state

# @async_dec
# async def fl_server_check():
#     res = requests.get('http://10.152.183.249:8080/FL_ST')
#     if res.status_code != 200:
#         FLSe.FLSeReady=False
#     else:
#         FLSe.FLSeReady=True
#     return FLSe



if __name__ == "__main__":    

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
