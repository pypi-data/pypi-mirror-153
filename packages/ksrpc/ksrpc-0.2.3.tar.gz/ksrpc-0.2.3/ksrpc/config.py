"""
服务端配置
"""
# 是否检查可调用的方法。
# !!! 生产环境中请不要随意关闭，否则权限过大
from IPy import IP

METHODS_CHECK = False

# 允许的方法
# 没有列出的module和method默认值为False表示不可调用
METHODS_ALLOW = {
    'pandas': {
        'read_csv': True,
        'util': {
            'testing': {
                'makeTimeDataFrame': True,
                'makeDataFrame': False,
            }
        }
    },
    'os': True,
    'ntpath': True,
    'numpy': True,
    'math': True,
    'sys': True,
    'jqdatasdk': True,
    'WindPy': True,
    'tushare': True,
    'rqdatac': True,
    'demo': True,
}

# 禁止的方法
# 没有列出的module和method默认值为True表示放行
METHODS_BLOCK = {
    'os': {
        'remove': False,
    },
    'jqdatasdk': {
        'is_auth': False,
        'auth': False,
        'logout': False,
    },
    'WindPy': {
        'w': {
            'start': False,
        }
    },
    'tushare': {
        'set_token': False,
        'pro_api': False,
    },
    'rqdatac': {
        'init': False,
    },
    'demo': True,
}

# 是否进行IP检查，屏蔽外网访问
IP_CHECK = True

IP_ALLOW = {
    IP('127.0.0.0/8'): True,  # 回环地址
    IP('192.168.0.0/16'): True,  # C类内网
    IP('172.16.0.0/12'): True,  # B类内网
    IP('10.0.0.0/8'): True,  # A类内网
}
IP_BLOCK = {
    IP('8.8.8.8/32'): False,
    IP('8.8.4.4/32'): False,
}

# 缓存类型。生产环境请配置redis服务
CACHE_TYPE = 'fakeredis'  # fakeredis, aioredis
# 缓存服务地址
REDIS_URL = "redis://:password@localhost:6379/0"

# 是否启用授权
AUTH_CHECK = False
# API授权
AUTH_TOKENS = {
    "secret-token-1": "john",
    "secret-token-2": "susan",
}

# 聚宽账号
JQ_USERNAME = '13912345678'
JQ_PASSWORD = '12345678'

# TuShare账号
TUSHARE_TOKEN = '12345678'

# 米筐账号
RQ_USERNAME = '13912345678'
RQ_PASSWORD = '12345678'

# 启用万得
WIND_ENABLE = False
