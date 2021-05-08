from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
	id = db.Column(db.String(32), primary_key=True)
	name = db.Column(db.String(16))
	tele = db.Column(db.String(11))

	def __repr__(self):
		""" 用来以字符串形式显示用户信息 """
		return (
			f"<User name={self.name} tele={self.tele} "+
			f"addr={','.join(map(lambda a:a.location ,self.addresses)) or 'None'}>")


class Address(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	location = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.String(32), db.ForeignKey("user.id"), nullable=False)
	user = db.relationship("User", backref=db.backref("addresses", lazy=False))

	def __repr__(self):
		return f"<Address f{self.location}>"


class BaseOrderInfo:
	"""基本订单类，其他三个状态都继承自它"""
	id = db.Column(db.Integer, primary_key=True)
	# 表示有多少个物件
	stuff_number = db.Column(db.Integer, nullable=False)
	# 表示物件的重量
	stuff_weight = db.Column(db.String(12), nullable=False)
	# 表示取件地址
	stuff_address = db.Column(db.Text, nullable=False)
	# 表示收件地址
	receive_address = db.Column(db.Text, nullable=False)
	# 表示预付金额
	amount = db.Column(db.Float, nullable=False)
	# 表示下单时间
	timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
	# 表示下单人的电话
	buyer_tele = db.Column(db.String(11))
	# 表示接单人的电话
	receiver_tele = db.Column(db.String(11))
	# 表示备注信息
	comments = db.Column(db.Text)


class Pending(db.Model, BaseOrderInfo):
	# 表示谁下了这个单
	buyer_id = db.Column(db.String(32), db.ForeignKey("user.id"))
	# 表示谁接了这个单
	receiver_id = db.Column(db.String(32), db.ForeignKey("user.id"))


class Active(db.Model, BaseOrderInfo):
	# 表示谁下了这个单
	buyer_id = db.Column(db.String(32), db.ForeignKey("user.id"))
	# 表示谁接了这个单
	receiver_id = db.Column(db.String(32), db.ForeignKey("user.id"))


class Finish(db.Model, BaseOrderInfo):
	# 表示谁下了这个单
	buyer_id = db.Column(db.String(32), db.ForeignKey("user.id"))
	# 表示谁接了这个单
	receiver_id = db.Column(db.String(32), db.ForeignKey("user.id"))


def register_db_shell_context(app):
	""" 注册数据库相关的变量到 flask shell 上下文中 """
	app.shell_context_processor(lambda: {
		"db": db,
		"User": User,
		"Address": Address,
		"Pending": Pending,
		"Active": Active,
		"Finish": Finish,
	})