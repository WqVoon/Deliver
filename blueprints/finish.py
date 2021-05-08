from flask import Blueprint, request, abort
from flask_login import current_user, login_required


finish_bp = Blueprint("finish", __name__, url_prefix="/finish")


@finish_bp.route("/")
def finish_index():
	return "Hello, Finish!"