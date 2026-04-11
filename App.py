import uvicorn
from apis.wx_apis import WX_Apis
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

apis = WX_Apis()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
    获取公众号的id
    :json query: 公众号名称
    :json token: token
    :json cookies_str: cookies
"""
@app.post("/get_fakeid")
def get_fakeid(data: dict):
    try:
        query = data["query"]
        token = data["token"]
        cookies_str = data["cookies_str"]
        success, msg, res_json = apis.get_fakeid(query, token, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": res_json}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

"""
    获取公众号的所有文章
    :json fakeid: 公众号id
    :json token: token
    :json cookies_str: cookies
    :json sleep_time: 睡眠时间
"""
@app.post("/get_shop_works")
def get_shop_works(data: dict):
    try:
        fakeid = data["fakeid"]
        token = data["token"]
        cookies_str = data["cookies_str"]
        sleep_time = data["sleep_time"]
        success, msg, res = apis.get_shop_all_works(fakeid, token, cookies_str, sleep_time)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

"""
    获取文章的内容
    :json url: 文章的url
"""
@app.post("/get_work_detail")
def get_work_detail(data: dict):
    try:
        url = data["url"]
        success, msg, res = apis.get_work_detail(url)
        if success:
            return {"code": 200, "message": msg, "data": res}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5004, forwarded_allow_ips='*')
