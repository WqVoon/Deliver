from flask import Blueprint, request
from flask_login import login_user, current_user, login_required
from uuid import uuid3, NAMESPACE_DNS
from ..model import User
from .auth import users
from ..utils import get_user

test_bp = Blueprint("test", __name__, url_prefix="/test")

@test_bp.route("/")
def test_bp_idx():
	return "Hello Test!"


@test_bp.route("/login", methods=["GET"])
def test_login():
	""" 测试用的登录 API """
	id = request.args.get("id")
	if id:
		uuid = uuid3(NAMESPACE_DNS, id).hex
		tmp_user = get_user(id)
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
		return "Login Err"


@test_bp.route("/logout", methods=["GET"])
@login_required
def test_logout():
	""" 测试用的登出 API """
	uuid = request.args.get("uuid")
	users.pop(uuid)
	return "Logout OK"


@test_bp.route("/loginTest")
@login_required
def test_users():
	""" 用来判断用户是否登录成功，成功返回字符串，否则返回 405 """
	return f"Hello, {current_user}", 200, {
		"Content-Type": "text/plain;charset=utf-8"}