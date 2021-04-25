from flask import Blueprint, request, abort
from flask_login import current_user, login_required
from ..model import db, User, Address


me_bp = Blueprint("me", __name__, url_prefix="/me")


@me_bp.route("/tele/update", methods=["POST"])
@login_required
def update_tele():
	"""
	修改当前用户的电话号码
		- 参数
			tele 为新的号码字符串
		- 返回
			成功返回 OK
	"""
	new_tele = request.json.get("tele")
	if new_tele is None:
		return "Please provide 'tele' arg by json", 403

	User.query.get(current_user.id).tele = new_tele
	db.session.commit()
	return "OK"


@me_bp.route("/addr/add", methods=["POST"])
@login_required
def add_addr():
	"""
	为当前用户添加新的常用地址
		- 参数
			addrs 为想要添加的新地址的字符串列表
		- 返回
			{
				"addrs": [
					{"key": 数据库主键, "location": 地址文本},
					...
				]
			}

	"""
	addrs = request.json.get("addrs")
	if addrs is None:
		return "Please provide 'addrs' arg by json", 403

	me = User.query.get(current_user.id)
	new_addrs = []
	for location in addrs:
		addr = Address(location=location)
		me.addresses.append(addr)
		new_addrs.append(addr)

	db.session.commit()

	return {
		"new_addrs": [
			{"key": addr.id, "location": addr.location}
			for addr in new_addrs
		]
	}


@me_bp.route("/addr/delete", methods=["POST"])
@login_required
def delete_addr():
	"""
	为当前用户删除常用地址
		- 参数
			addrs 为想要删除的地址的主键列表
		- 返回
			如果删除成功，返回 200 的 OK
			否则返回 403
	"""
	addrs = request.json.get("addrs")
	if addrs is None:
		return "Please provide 'addrs' arg by json", 403

	for key in addrs:
		item = Address.query.get(key)
		if item is None or item.user_id != current_user.id:
			abort(403)
		else:
			db.session.delete(item)
	db.session.commit()
	return "OK"


@me_bp.route("/addr/update", methods=["POST"])
@login_required
def update_addr():
	"""
	更新用户的地址信息
		- 参数
			{
				"addrs": [
					{"key": 数据库主键, "location": 地址文本},
					...
				]
			}
		- 返回
			成功返回 OK
	"""
	addrs = request.json.get("addrs")
	if addrs is None:
		return "Please provide 'addrs' arg by json", 403

	for addr in addrs:
		try:
			key, value = addr["key"], addr["location"]
		except IndexError:
			return "Please provide {'key':xxx, 'value':xxx} pattern", 403

		addr = Address.query.get(key)
		if addr is None or addr.user_id != current_user.id:
			abort(403)

		addr.location = value
	db.session.commit()

	return "OK"