from flask import Flask, request
from requests import get
from hashlib import sha1

app = Flask(__name__)

def validate_user(raw_data, session_key, signature):
	"""用来根据用户提供的信息计算签名，并比对来严重用户的合法性"""
	code = (raw_data+session_key).encode('utf8')
	calc_sign = sha1(code).hexdigest()
	print("calc_sign:", calc_sign)
	return calc_sign == signature

def code_to_session(code, appid, secret):
	"""调用微信后台接口来获取用户唯一标识 open_id 和 session_key"""
	r = get(
		"https://api.weixin.qq.com/sns/jscode2session",
		params={
			"appid": appid,
			"secret": secret,
			"js_code": code,
			"grant_type": "authorization_code"
		}
	)
	print(r.json())
	return r.json()

@app.route("/login", methods=("GET", "POST"))
def index():
	code, appid, secret, raw_data, signature = (
		request.json["code"],
		request.json["appid"],
		request.json["secret"],
		request.json["raw_data"],
		request.json["signature"]
	)
	print(
		f"code: {code}",
		f"appid: {appid}",
		f"secret: {secret}",
		f"raw_data: {raw_data}",
		f"signature: {signature}",
		sep="\n"
	)
	
	ret = code_to_session(code, appid, secret)
	session_key = ret['session_key']
	open_id = ret['openid']
	if validate_user(raw_data, session_key, signature):
		return "OK"
	else:
		return "Err"

app.run(port=8080)