from flask import Blueprint, request
from backend.models import Session
from backend.models.user import User
from decouple import config
import jwt
import bcrypt
from flask_marshmallow import Marshmallow
from datetime import datetime, timedelta

session = Session()

SECRET_KEY = config('ACCESS_SECRET_TOKEN')
BCRYPT_SALT = int(config('BCRYPT_SALT'))

authentication = Blueprint('authentication', __name__)
ma = Marshmallow(authentication)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'phone', 'password')


user_schema = UserSchema()


def are_all_args_present(*args):
    for a in args:
        if a is None:
            return False
    return True


@authentication.route('/login', methods=['POST'])
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')

    if not are_all_args_present(email, password):
        return {'success': False, 'error': 'Please provide all the arguments'}

    user = session.query(User).filter(User.email == email).first()
    if not user:
        return {'success': False, 'error': 'User with email id does not exist'}
    is_password_matching = bcrypt.checkpw(
        password.encode('utf-8'), user.password.encode('utf-8'))
    if is_password_matching:
        expiry_limit = datetime.now() + timedelta(hours=1)
        encoded_token = jwt.encode(
            {"id": user.id, 'exp': expiry_limit}, SECRET_KEY, algorithm='HS256')
        return {'success': True, 'name': user.name, 'token': encoded_token}
    return {'success': False, 'error': 'Passwords does not match'}


@authentication.route('/register', methods=['PUT'])
def create_new_user():
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    password = request.json.get('password')

    if not are_all_args_present(name, email, phone, password):
        return {'success': False, 'error': 'Please provide all the arguments'}

    is_user_present = session.query(User).filter(User.email == email).first()
    if is_user_present:
        return {'success': False, 'error': 'Email already in use'}
    hashed_password = str(bcrypt.hashpw(password.encode(
        'utf-8'), bcrypt.gensalt(BCRYPT_SALT))).replace("b'", "").replace("'", "")
    new_user = User(name, email, phone, hashed_password)
    try:
        session.add(new_user)
        session.commit()
        return {'success': True, 'user': user_schema.dump(new_user)}
    except:
        return {'success': False, 'error': "New user not created"}
