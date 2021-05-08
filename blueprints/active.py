from flask import Blueprint, request, abort
from flask_login import current_user, login_required
from ..model import Active, Finish, db
from ..utils import get_one_page_orders


active_bp = Blueprint("active", __name__, url_prefix="/active")


@active_bp.route("/")
def active_index():
	return "Hello, Active!"


@active_bp.route("/query/i-add/<int:page_id>")
@login_required
def active_query_i_add(page_id):
	"""查询我下过的所有订单，返回值同 /pending/query/all"""
	query = Active.query.filter_by(buyer_id=current_user.id)
	items = get_one_page_orders(query, page_id)
	return { "items": items }


@active_bp.route("/query/i-fetch/<int:page_id>")
@login_required
def active_query_i_fetch(page_id):
	"""查询我接过的所有订单，返回值同 /pending/query/all"""
	query = Active.query.filter_by(receiver_id=current_user.id)
	items = get_one_page_orders(query, page_id)
	return { "items": items }


@active_bp.route("/finish", methods=["POST"])
@login_required
def active_finish():
	"""完成指定的订单，该动作只能由下单人发起"""
	try:
		key = request.json["key"]
	except KeyError:
		return "Incomplete arg list", 403

	item = Active.query.get_or_404(key)
	if item.buyer_id != current_user.id:
		return "Can not finish this order", 403

	new_item = Finish(
		receiver_id     = item.receiver_id,
		receiver_tele   = item.receiver_tele,
		buyer_id        = item.buyer_id,
		buyer_tele      = item.buyer_tele,
		amount          = item.amount,
		comments        = item.comments,
		stuff_number    = item.stuff_number,
		stuff_weight    = item.stuff_weight,
		stuff_address   = item.stuff_address,
		receive_address = item.receive_address,
		timestamp       = item.timestamp,
	)

	db.session.delete(item)
	db.session.add(new_item)
	db.session.commit()
	return "OK"