from flask import Flask
from config import app_config

def create_app():
	app = Flask(__name__)
	app.config.from_mapping(app_config)
	
	from test import test_bp
	app.register_blueprint(test_bp)

	return app