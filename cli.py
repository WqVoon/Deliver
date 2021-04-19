from flask.cli import with_appcontext, AppGroup
from click import command

custom_cli = AppGroup("cli")


def cli(*args, **kwargs):
	"""
		自定义装饰器，用来简化下面命令的包装
		使得下面的命令都归属于 custom_cli 的 AppGroup
	"""
	def decorator(f):
		return custom_cli.command(
			*args, **kwargs)(with_appcontext(f))
	return decorator


@cli("test")
def test_cli():
	""" 用来测试外部文件的 CLI """
	print("OK!")