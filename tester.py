"""
测试用的模块，内部封装了 GET 和 POST 方法用于避免手动登录
可运行 `python3 -i tester.py` 来获取 REPL 环境
"""

from requests import get, post

base = "http://127.0.0.1:5000/"

r = get(f"{base}test/login", params={"id": "1"})

if not r.ok:
	raise Exception("Login Error")

uuid = r.json()["uuid"]
print("uuid:", uuid)

def GET(url, params={}):
	params["uuid"] = uuid
	return get(url, params=params)

def POST(url, json={}):
	json["uuid"] = uuid
	return post(url, json=json)

