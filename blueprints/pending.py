from flask import Blueprint, request, abort
from flask_login import current_user, login_required
from ..model import Pending, db


pending_bp = Blueprint("pending", __name__, url_prefix="/pending")


@pending_bp.route("/")
def pending_index():
	return "Hello, Pending!"


@pending_bp.route("/add", methods=["POST"])
@login_required
def pending_add():
	"""用来添加新的订单
		- 参数
			{
				"amount": <价格>,
				"comments": <备注>,
				"stuff_number": <物品数量>
				"stuff_weight": <物品重量>
				"stuff_address": <取件地址>
				"receive_address": <收件地址>
			}
		- 返回
			成功返回 OK，参数不全时返回 403
	"""
	args = request.json
	try:
		tmp_order = Pending(
			buyer_id        = current_user.id,
			buyer_tele      = current_user.tele,
			amount          = args["amount"],
			comments        = args["comments"],
			stuff_number    = args["stuff_number"],
			stuff_weight    = args["stuff_weight"],
			stuff_address   = args["stuff_address"],
			receive_address = args["receive_address"],
		)
	except KeyError:
		return "Incomplete arg list", 403

	db.session.add(tmp_order)
	db.session.commit()
	return "OK!"