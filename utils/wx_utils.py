import requests

def get_common_headers():
    return {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=0&token=587855976&lang=zh_CN&timestamp=1712484486851",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

def get_fakeid_params(query, token):
    return {
        "action": "search_biz",
        "begin": "0",
        "count": "5",
        "query": query,
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }

def get_shop_works_params(begin, fakeid, token):
    return {
        "sub": "list",
        "search_field": "null",
        "begin": begin,
        "count": "5",
        "query": "",
        "fakeid": fakeid,
        "type": "101_1",
        "free_publish_type": "1",
        "sub_action": "list_ex",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }

def text_contains(tag, substr, tag_name=None):
    if tag_name is not None and tag.name != tag_name:
        return False
    return substr in tag.text


def class_starts_with(tag, prefix, tag_name=None):
    if tag_name is not None and tag.name != tag_name:
        return False
    if not tag.has_attr('class'):
        return False
    return tag["class"][0].startswith(prefix)

def class_contains(tag, substr, tag_name=None):
    if tag_name is not None and tag.name != tag_name:
        return False
    if not tag.has_attr('class'):
        return False
    return substr in tag["class"]
def trans_cookies(cookies):
    return {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
