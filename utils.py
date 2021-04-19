from requests import get
from hashlib import sha1


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