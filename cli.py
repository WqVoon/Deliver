from flask.cli import with_appcontext, AppGroup
from click import command, option
from model import db, User, Address
from uuid import uuid1

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
		id="TEST-" + uuid1().hex[5:],
		name=input("Name: "),
		tele=input("Tele: ")
	)
	db.session.add(tmp_user)
	db.session.commit()
	print("Add User:", tmp_user)


@cli()
@option("--name")
def query_user(name):
	""" 根据用户名来查询 User 表中的记录 """
	if name is None:
		results = User.query.all()
	else:
		results = User.query.filter_by(name=name).all()

	for u in results:
		print(u)
	print("Done")


@cli()
@option("--name", required=True)
def update_user(name):
	""" 根据用户名来更新 User 表中的手机号 """
	User.query.filter_by(name=name).update({
		"tele": input("New Tele: ")
	})
	db.session.commit()
	print("Done")


@cli()
@option("--name", required=True)
def add_address(name):
	""" 向 Address 中加入一条与某 user 相关的记录 """
	u = User.query.filter_by(name=name).first()
	if u is None:
		print("No such user")
		return None

	u.addresses.append(Address(location=input("Location: ")))
	db.session.commit()
	print("Done")