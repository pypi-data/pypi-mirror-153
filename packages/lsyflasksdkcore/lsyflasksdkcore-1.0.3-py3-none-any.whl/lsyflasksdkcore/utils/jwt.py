import datetime

import jwt
from flask import current_app

from lsyflasksdkcore.exceptions import JwtTokenError


def encode_auth_token(user_id, login_time):
    """
    生成认证Token
    :param user_id: int
    :param login_time: int(timestamp)
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
            'iat': datetime.datetime.utcnow(),
            'iss': 'ken',
            'data': {
                'id': str(user_id),
                'login_time': login_time
            }
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
    except Exception as e:
        raise JwtTokenError("生成Token失败")


def decode_auth_token(auth_token):
    """
    验证Token
    :param auth_token:
    :return: integer|string
    """
    try:
        # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
        # 取消过期时间验证
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'),
                             options={'verify_exp': False},
                             algorithms=["HS256"])
        if 'data' in payload and 'id' in payload['data']:
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        raise JwtTokenError("Token过期")
    except jwt.InvalidTokenError:
        raise JwtTokenError("无效Token")
