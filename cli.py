from flask.cli import with_appcontext, AppGroup
from click import command, option
from model import db, User, Address

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


@cli()
def init_db():
	""" 用来初始化数据库 """
	db.create_all()
	print("Init All")


@cli()
def drop_db():
	""" 用来清空所有数据库 """
	db.drop_all()
	print("Clear All")


@cli()
def add_user():
	""" 向 User 表中加入一条内容 """
	tmp_user = User(
		id=input("ID: "),
		name=input("Name: "),
		tele=input("Tele: ")
	)
	db.session.add(tmp_user)
	db.session.commit()
	print("Add User:", tmp_user)


@cli()
@option("--id")
@option("--name")
def query_user(id, name):
	""" 根据提供的参数来查询 User 表中的记录 """
	for u in query_user_by_args(id, name):
		print(u)
	print("Done")


@cli()
@option("--id")
@option("--name")
def update_user(id, name):
	""" 根据提供的参数来更新 User 表中的手机号 """
	query_user_by_args(id, name).update({
		"tele": input("New Tele: ")
	})
	db.session.commit()
	print("Done")


@cli()
@option("--id")
@option("--name")
def add_address(id, name):
	""" 向 Address 中加入一条与某 user 相关的记录 """
	if id is None and name is None:
		print("Must provide query arg")
		return None
	try:
		u = query_user_by_args(id, name)[0]
	except IndexError:
		print("No such user")
		return None

	u.addresses.append(Address(location=input("Location: ")))
	db.session.commit()
	print("Done")


def query_user_by_args(id, name):
	""" 辅助函数 """
	if id is not None:
		return User.query.filter_by(id=id).all()
	elif name is not None:
		return User.query.filter_by(name=name).all()
	else:
		return User.query.all()