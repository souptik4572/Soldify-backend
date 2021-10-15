from werkzeug.wrappers import Request, Response, ResponseStream
import jwt
from decouple import config
SECRET_KEY = config('ACCESS_SECRET_TOKEN')
class AuthProtection():
    def __call__(self, environment, start_response):
        request = Request(environment)
        token = request.authorization

def get_logged_user_id(token):
    try:
        user = jwt.decode(token.split(
            ' ')[1], SECRET_KEY, algorithms=['HS256'])
        if not user['id']:
            return None, 'Token is invalid'
        return user['id'], 'Token is valid'
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired, please login again'
    except:
        return None, 'Token is invalid'
