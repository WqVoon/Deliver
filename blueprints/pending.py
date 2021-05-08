from flask import Blueprint, request, abort
from flask_login import current_user, login_required


pending_bp = Blueprint("pending", __name__, url_prefix="/pending")


@pending_bp.route("/")
def pending_index():
	return "Hello, Pending!"