from flask_login import (
	LoginManager, UserMixin, login_required,
	login_user, current_user
)
from flask import Blueprint, request, abort, current_app
from flask.sessions import SecureCookieSessionInterface
from json import loads
from uuid import uuid3, NAMESPACE_DNS
from ..model import User
from ..utils import validate_user, code_to_session, get_user
from cachetools import TTLCache
from ..config import USER_MAX_SIZE, USER_SESSION_TTL

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
login_manager = LoginManager()
users = TTLCache(maxsize=USER_MAX_SIZE, ttl=USER_SESSION_TTL)


class CustomSessionInterface(SecureCookieSessionInterface):
	""" 避免生成 cookie，用来配合 request.loader 实现自定义登录态 """
	def save_session(self, *args, **kwargs):
		return


@auth_bp.route("/")
def auth_bp_idx():
	return "Hello auth!"


@login_manager.request_loader
def load_user_from_request(r):
	""" 自定义的 user_loader，根据 uuid 字段来寻找用户 """
	if r.method == "GET":
		uuid = r.args.get("uuid")
	else:
		if r.json is None:
			return None
		uuid = r.json.get("uuid")
	return users.get(uuid)


@auth_bp.route("/login", methods=["POST"])
def index():
	""" 小程序使用的登录 API """
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
	session_key, open_id = ret['session_key'], ret['openid']

	if validate_user(raw_data, session_key, signature):
		uuid = uuid3(NAMESPACE_DNS, current_app.secret_key+open_id).hex
		info = loads(raw_data)
		tmp_user = get_user(open_id)
		users[uuid] = tmp_user
		login_user(tmp_user)
		return {
			"uuid": uuid,
			"tele": tmp_user.tele,
			"addr": [
				{"key": addr.id, "location": addr.location}
				for addr in tmp_user.addresses
			]
		}
	else:
		return "Err", 403


@auth_bp.route("/logout", methods=["POST"])
@login_required
def test_logout():
	""" 登出 API """
	uuid = request.json.get("uuid")
	users.pop(uuid)
	return "Logout OK"