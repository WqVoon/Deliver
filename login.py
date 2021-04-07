from flask import Flask, request, abort
from flask.sessions import SecureCookieSessionInterface
from requests import get
from hashlib import sha1
from json import loads
from uuid import uuid3, NAMESPACE_DNS
from flask_login import (
	LoginManager, UserMixin, login_required,
	login_user, current_user
)

class CustomSessionInterface(SecureCookieSessionInterface):
	def save_session(self, *args, **kwargs):
		return

class User(UserMixin):
	def __init__(self, id, name):
		self.id = id
		self.name = name

app = Flask(__name__)
app.config["SECRET_KEY"] = "IloveLym"
app.session_interface = CustomSessionInterface()
login_manager = LoginManager(app)
users = {}


@login_manager.request_loader
def load_user_from_request(r):
	if r.method == "GET":
		uuid = r.args.get("uuid")
	else:
		uuid = r.json.get("uuid")
	return users.get(uuid)

@app.errorhandler(401)
def handle_401(e):
	return "Who are u?"

@app.errorhandler(404)
def handle_404(e):
	return "No such page"

@app.errorhandler(500)
def handle_500(e):
	return str(e)

@app.route("/login", methods=["GET"])
def test_login():
	id = request.args.get("id")
	if id:
		uuid = uuid3(NAMESPACE_DNS, id).hex
		u = User(id)
		users[uuid] = u
		login_user(u)
		return f"Login OK, uuid: {uuid}"
	else:
		return "Login Err"

@app.route("/logout", methods=["POST"])
@login_required
def test_logout():
	uuid = request.json.get("uuid")
	users.pop(uuid)
	return "Logout OK"


@app.route("/loginTest")
@login_required
def login_test():
	return f"Hello, {current_user.name}"

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

@app.route("/login", methods=["POST"])
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
		uuid = uuid3(NAMESPACE_DNS, app.secret_key+open_id).hex
		info = loads(raw_data)
		tmp_user = User(open_id, info["nickName"])
		users[uuid] = tmp_user
		login_user(tmp_user)
		return uuid
	else:
		return "Err"

app.run(host="0.0.0.0", port=1011)