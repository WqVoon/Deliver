from flask import Flask

def create_app():
	app = Flask(__name__)

	# 注册配置信息
	from config import app_config
	app.config.from_mapping(app_config)
	
	# 注册错误码处理函数
	from code_handlers import (
		handle_401, handle_404, handle_500
	)
	app.register_error_handler(401, handle_401)
	app.register_error_handler(404, handle_404)
	app.register_error_handler(500, handle_500)

	# 注册测试蓝图，url前缀 /test
	from test import test_bp
	app.register_blueprint(test_bp)

	return app