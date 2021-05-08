from flask import Blueprint, request, abort
from flask_login import current_user, login_required
from ..model import Active
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