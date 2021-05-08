from flask import Blueprint, request, abort
from flask_login import current_user, login_required
from ..model import Finish
from ..utils import get_one_page_orders

finish_bp = Blueprint("finish", __name__, url_prefix="/finish")


@finish_bp.route("/")
def finish_index():
	return "Hello, Finish!"


@finish_bp.route("/query/i-add/<int:page_id>")
@login_required
def finish_query_i_add(page_id):
	"""查询我下过的所有订单，返回值同 /pending/query/all"""
	query = Finish.query.filter_by(buyer_id=current_user.id)
	items = get_one_page_orders(query, page_id)
	return { "items": items }


@finish_bp.route("/query/i-fetch/<int:page_id>")
@login_required
def finish_query_i_fetch(page_id):
	"""查询我接过的所有订单，返回值同 /pending/query/all"""
	query = Finish.query.filter_by(receiver_id=current_user.id)
	items = get_one_page_orders(query, page_id)
	return { "items": items }