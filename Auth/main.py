from ninja import NinjaAPI, Router
from django.contrib.auth import login, authenticate
import jwt

import djangoProject.settings
from Auth.schema import LoginSchema

api = NinjaAPI()
router = Router()
SECRET_KEY = djangoProject.settings.SECRET_KEY


def token_required(f):
    """
    验证 JWT
    :param f:
    :return:
    """

    def decorated(request, *args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return {'message': 'Token is missing'}, 401
        token = auth.split(' ')[1]
        if not token:
            return {'message': 'Token is missing'}, 401

        try:
            user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return {'message': 'Token is invalid'}, 401

        return f(request, user, *args, **kwargs)

    return decorated


@router.post('/login/')
def login(request, payload: LoginSchema):
    """
    使用django自带登录验证账号登录  并生成jwt返回
    """
    user = authenticate(request, username=payload.username, password=payload.password)
    print(user)
    if user is not None:
        token = jwt.encode(
            {'user_id': user.id, 'user_name': user.username, 'role': user.is_superuser},
            SECRET_KEY)
        return {'token': token,
                'user_info': {'user_id': user.id, 'user_name': user.username, 'role': user.is_superuser}}
    else:
        return {'error': '用户名或密码错误！'}


@router.post('/logout/')
@token_required
def logout(request, user):
    """
    退出登录
    """
    return {'message': '退出登录成功！'}
