def handle_401(e):
	return "Who are u?", 401


def handle_404(e):
	return "No such page", 404


def handle_500(e):
	return str(e), 500