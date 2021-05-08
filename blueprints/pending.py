from flask import Blueprint, request, abort
from flask_login import current_user, login_required
from ..model import Pending, db
from ..utils import get_one_page_orders


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

	if current_user.tele is None:
		return "Please fill in the phone number first", 403

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


@pending_bp.route("/query/all/<int:page_id>")
# @login_required
def pending_query_all(page_id):
	"""查询所有待接取的订单
	在没有对应的页时返回 404
	否则返回如下内容的列表：
		{
			id: <订单主键>
			stuff_number: <物品数量>
			stuff_weight: <物品重量>
			stuff_address: <取件地址>
			receive_address: <收件地址>
			amount: <预付金额>
			timestamp: <下单时间>
			buyer_tele: <下单人电话>
			receiver_tele: <接单人电话>
			comments: <备注>
		}
	其中某一字段（如接单人电话）不存在时对应的值为 null
	"""
	items = get_one_page_orders(Pending.query, page_id)
	return { "items": items }


@pending_bp.route("/query/i-add/<int:page_id>")
# @login_required
def pending_query_i_add(page_id):
	"""查询我下过的所有订单，返回值同 /pending/query/all"""
	query = Pending.query.filter_by(buyer_id=current_user.id)
	items = get_one_page_orders(query, page_id)
	return { "items": items }