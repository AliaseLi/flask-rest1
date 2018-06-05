import os

# 配置根目录
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

class Config:
    DEBUG = True
    ENV = 'development'

    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 设置session相关参数
    SECRET_KEY = 'RESTFULLSEC'

