from requests import get
from hashlib import sha1
from .model import User, db
from werkzeug.exceptions import NotFound
from .config import PER_PAGE


def get_user(uid, name="Test"):
	"""
		如果 uid 对应的用户已经存在于数据库，则返回之
		否则根据 uid 新建一个用户对象，并加入到 user 表中
	"""
	try:
		user = User.query.get_or_404(uid)
		print("从数据库获取了用户")
	except NotFound:
		user = User(id=uid, name=name)
		db.session.add(user)
		db.session.commit()
		print("新建了用户")

	return user


def get_one_page_orders(query, page_id):
	"""根据查询器获取指定页的内容，找不到则返回 404，否则返回字典列表"""
	one_page = query.paginate(page_id, per_page=PER_PAGE).items
	items = []
	for data in one_page:
		items.append(dict(
			id = data.id,
			stuff_number    = data.stuff_number,
			stuff_weight    = data.stuff_weight,
			stuff_address   = data.stuff_address,
			receive_address = data.receive_address,
			amount          = data.amount,
			timestamp       = data.timestamp.strftime("%Y/%m/%d %H:%M:%S"),
			buyer_tele      = data.buyer_tele,
			receiver_tele   = data.receiver_tele,
			comments        = data.comments,
		))
	return items


def validate_user(raw_data, session_key, signature):
	"""用来根据用户提供的信息计算签名，并比对来严重用户的合法性"""
	code = (raw_data+session_key).encode('utf8')
	calc_sign = sha1(code).hexdigest()
	print("calc_sign:", calc_sign)
	return calc_sign == signature


def code_to_session(code, appid, secret):
	"""调用微信后台接口来获取用户唯一标识 open_id 和 session_key"""
	r = get(
		"https://api.weixin.qq.com/sns/jscode2session",
		params={
			"appid": appid,
			"secret": secret,
			"js_code": code,
			"grant_type": "authorization_code"
		}
	)
	print(r.json())
	return r.json()