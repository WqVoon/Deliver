from flask import Blueprint, request, abort
from flask_login import current_user, login_required


active_bp = Blueprint("active", __name__, url_prefix="/active")


@active_bp.route("/")
def active_index():
	return "Hello, Active!"