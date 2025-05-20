import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .api.models.revoked_token import RevokedTokenModel
from .config import config
from .api.models import db
from .api import api_blueprint
from .manage import migrate
from .api.models.user import UserModel
from .api.models.cases import CasesModel


def create_app(config_name):
    # 初始化 Flask 项目
    app = Flask(__name__)
    # 加载配置项
    app.config.from_object(config[config_name])
    # 初始化数据库ORM
    db.init_app(app)
    # 初始化JWT
    jwt = JWTManager(app)
    # 注册 JWT 钩子
    registerJwtHooks(jwt)
    # 解决跨域
    CORS(app)
    # 初始化数据库ORM迁移插件
    migrate.init_app(app, db)
    # 注册蓝图
    app.register_blueprint(api_blueprint)

    return app


def registerJwtHooks(jwt):
    # 注册 JWT 钩子 用于检查 token 是否在黑名单中
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)


# 初始化项目
app = create_app(os.getenv('FLASK_ENV', 'development'))


