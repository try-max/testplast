from flask import Blueprint

from flask_restful import Api


from .resources.case import case_bp
from .resources.login import Login
from .resources.logout import Logout
from .resources.menu import UserMenu, UserButtons
from .resources.register import Register
from .resources.user import UserService


from ..testcase.receive import TestCase

api_blueprint = Blueprint('api', __name__, url_prefix="/api")

api = Api(api_blueprint)
api.add_resource(Register, '/register')
api.add_resource(Login, '/login', '/refreshToken')

api.add_resource(Logout, '/logout',)

api.add_resource(UserService, '/getUserList')

api.add_resource(UserMenu, '/menu/list')


api.add_resource(UserButtons, '/auth/buttons')


api.add_resource(TestCase, '/interfaces/execute')







# api.add_resource(api_blueprint, '')


