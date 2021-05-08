# 用来初始化 app 实例的配置
app_config = {
	"SECRET_KEY": "IloveLym",
	"SQLALCHEMY_TRACK_MODIFICATIONS": False,
	"SQLALCHEMY_DATABASE_URI": "sqlite:///database.db"
}

# 最大在线用户数量
USER_MAX_SIZE = 100

# 用户会话的维持时间，当前为两天
USER_SESSION_TTL = 2 * 24 * 60 * 60

# 下面两个配置用来限制单个 ip 在 LIMIT_TTL 时间内最多允许访问 LIMIT_COUNT 次服务
LIMIT_COUNT = LIMIT_TTL = 5

# 分页返回内容时，每一页有多少条记录
PER_PAGE = 10