from flask import Flask

def create_app():
	app = Flask(__name__)

	# 注册配置信息
	from config import app_config
	app.config.from_mapping(app_config)

	# 注册 Model 及其对应的 shell_context
	from model import db, register_db_shell_context
	db.init_app(app)
	register_db_shell_context(app)

	# 注册 CLI 命令
	from cli import custom_cli
	app.cli.add_command(custom_cli)
	
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

	# 注册登录蓝图，url前缀 /auth
	from auth import (
		auth_bp, CustomSessionInterface, login_manager
	)
	login_manager.init_app(app)
	app.session_interface = CustomSessionInterface()
	app.register_blueprint(auth_bp)

	return app