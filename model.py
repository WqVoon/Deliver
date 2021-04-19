from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
	id = db.Column(db.String(32), primary_key=True)
	name = db.Column(db.String(16))
	tele = db.Column(db.String(11))

	def __repr__(self):
	 return f"<User name={self.name} tele={self.tele}>"


class Address(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.String(32), db.ForeignKey("user.id"), nullable=False)
	user = db.relationship("User", backref=db.backref("addresses", lazy=True))


class OrderInfo(db.Model):
	id = db.Column(db.String(32), primary_key=True)
	buyer_id = db.Column(db.String(32), db.ForeignKey("user.id"), nullable=False)
	buyer = db.relationship("User", backref=db.backref("picks", lazy=True))


def register_db_shell_context(app):
	""" 注册数据库相关的变量到 flask shell 上下文中 """
	app.shell_context_processor(lambda: {
		"db": db,
		"User": User,
		"Address": Address,
	})