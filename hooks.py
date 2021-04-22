from flask import request, abort
from cachetools import TTLCache
from .config import LIMIT_TTL, LIMIT_COUNT, USER_MAX_SIZE

def register_hooks(app):
	""" 注册所有的钩子函数 """
	app.before_request(before_request)


ip_counter = TTLCache(maxsize=USER_MAX_SIZE, ttl=LIMIT_TTL)
def before_request():
	""" 请求进入业务逻辑前的钩子，主要用来限流 """
	key = request.remote_addr
	value = ip_counter.get(key, 0)
	if value >= LIMIT_COUNT:
		abort(403)
	ip_counter[key] = value + 1