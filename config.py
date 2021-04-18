# 用来初始化 app 实例的配置
app_config = {
	"SECRET_KEY": "IloveLym",
}

# 最大在线用户数量
USER_MAX_SIZE = 100

# 用户会话的维持时间，当前为两天
USER_SESSION_TTL = 2 * 24 * 60 * 60