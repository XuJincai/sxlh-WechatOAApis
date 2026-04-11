import json
import os
import re

import requests

from apis.wx_apis import WX_Apis

def norm_str(str):
    new_str = re.sub(r"|[\\/:*?\"<>| ]+", "", str).replace('\n', '').replace('\r', '')
    return new_str

def check_and_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True

if __name__ == '__main__':
    wx_apis = WX_Apis()
    cookie_str = r'RK=CeFoJwNWeW; pgv_pvid=9728068514; ua_id=gQGYaF4GyOG8c5IFAAAAAAaN3_BaF0X1JltAsHr_zBc=; wxuin=16102799067869; mm_lang=zh_CN; fqm_pvqid=e100573a-8643-4fdb-9564-da661f4d65eb; ptcz=8a4dd43f86a310302a5155ce5f848eac4d8d89e13a21b99ba78a2c4a8b5d2f85; euin=NKEANe-A7w4i; tmeLoginType=2; psrf_qqunionid=9894D98ACAED683ECBBC1DDC4B87EA23; psrf_qqopenid=5416FCBE33A1C87492C0B54B869FD3AF; psrf_access_token_expiresAt=1724317213; psrf_qqrefresh_token=59755DFF12338A8C0E0B782A7FE57AEC; psrf_qqaccess_token=01F256459C01248AA7DB824B691511A6; eas_sid=n117r1u6x7J9d7D7W2Y8p8E8G2; _clck=3910640650|1|fn5|0; uuid=d6c5d2afa0ced42c882eb4df280efb4c; rand_info=CAESIBdYzFreQaxEZIRswdnzkE2FkOCcjZ4VfzhbcwGVNg+u; slave_bizuin=3910640650; data_bizuin=3910640650; bizuin=3910640650; data_ticket=ttQyR6SkxPn6wNDCvok5LiAM/y9gYzEP6bQaos4tFnB/25xcKpkpVZ+JEKfO/3wb; slave_sid=Y3JYXzV6R2tqeFVwd2hmSENvR01ZZ0pDYUYyak9oMkZyQWlOSktKc190OUJoRFFaN3BneWI2REdZODBLQkZKMENQSVpSSExWTFQ5c3ZqTXU4WFJwaVR1bkZucU5ZbkFoZFJ4WEJQekR6Ym9UZk96QUhEeVlTTGtOdlA2WTlpVjZpMmRHVkdXTzI0TEFmd2RB; slave_user=gh_6268a70afda0; xid=a02aac5ee81c11b89ec9638a58ae16c7'
    token = r'723131708'
    querys = [
        # "笛量AI",
        # "帆软",
        "ConvertlaC"
    ]
    for query in querys:
        success, msg, res = wx_apis.get_fakeid(query, token, cookie_str)
        shop_id = res['list'][0]['fakeid']
        print(f'开始爬取{query}的所有文章')
        success, msg, res = wx_apis.get_shop_all_works(shop_id, token, cookie_str, sleep_time=20)
        print(f'获取到{query}的{len(res)}篇文章')
        for index, work in enumerate(res):
            print(f'开始爬取{query}的第{index + 1}篇文章')
            work_info = json.loads(work['publish_info'])
            link = work_info['appmsgex'][0]['link']
            mid = re.findall(r"mid=(\d+)", link)[0]
            success, msg, work_res = wx_apis.get_work_detail(link)
            if success:
                title = norm_str(work_res['title'])
                if title.strip() == '':
                    title = f'无标题'
                path = f'./{query}/{title}_{mid}/'
                isExist = check_and_create_path(path)


                # 打开这个注释，相当于只获取最新的文章，注释掉这个，相当于获取所有文章
                # if isExist:
                #     break


                with open(f'{path}/content.html', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(work_res, ensure_ascii=False, separators=(',', ':')))
                for i, image in enumerate(work_res['images']):
                    with open(f'{path}/{i}.jpg', 'wb') as f:
                        img_res = requests.get(image)
                        f.write(img_res.content)
                print(f'{query}的第{index + 1}篇文章完成')
            else:
                print(f'爬取{query}的第{index + 1}篇文章失败')
            print('=====================================')
        print(f'爬取{query}的所有文章完成')

