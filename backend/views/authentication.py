from flask import Blueprint, request
from ..models.user import User
from decouple import config
import jwt
import bcrypt
from flask_marshmallow import Marshmallow
from datetime import datetime, timedelta
from ..middleware import get_logged_user_id
from ..utils.check_args import are_all_args_present
from ..models.base import session

SECRET_KEY = config('ACCESS_SECRET_TOKEN')
BCRYPT_SALT = int(config('BCRYPT_SALT'))

authentication = Blueprint('authentication', __name__)
ma = Marshmallow(authentication)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'phone', 'password')


user_schema = UserSchema()

@authentication.route('/edit', methods=['PATCH'])
def edit_user_date():
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    phone = request.json.get('phone', None)
    try:
        user = session.query(User).filter(User.id == logged_in_id).first()
        if not user:
            return {'success': False, 'error': 'User with given id does not exist'}, 404
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        session.commit()
        return {'success': True, 'user': user_schema.dump(user)}, 201
    except Exception as e:
        session.rollback()
        return {'success': False, 'error': str(e)}, 404

@authentication.route('/delete', methods=['DELETE'])
def delete_existing_user():
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    user = session.query(User).filter(User.id == logged_in_id).first()
    if not user:
        return {'success': False, 'error': 'User with given id does not exist'}, 404
    try:
        session.delete(user)
        session.commit()
        return {'success': True, 'user': user_schema.dump(user)}, 201
    except Exception as e:
        return {'success': False, 'error': str(e)}, 404
    

@authentication.route('/login', methods=['POST'])
def login_user():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not are_all_args_present(email, password):
        return {'success': False, 'error': 'Please provide all the arguments'}, 404

    user = session.query(User).filter(User.email == email).first()
    if not user:
        return {'success': False, 'error': 'User with email id does not exist'}, 404
    is_password_matching = bcrypt.checkpw(
        password.encode('utf-8'), user.password.encode('utf-8'))
    if is_password_matching:
        expiry_limit = datetime.now() + timedelta(days=1)
        encoded_token = jwt.encode(
            {"id": user.id, 'exp': expiry_limit}, SECRET_KEY, algorithm='HS256')
        return {'success': True, 'name': user.name, 'token': encoded_token}, 200
    return {'success': False, 'error': 'Passwords does not match'}, 404


@authentication.route('/register', methods=['PUT'])
def create_new_user():
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    phone = request.json.get('phone', None)
    password = request.json.get('password', None)

    if not are_all_args_present(name, email, phone, password):
        return {'success': False, 'error': 'Please provide all the arguments'}, 404

    is_user_present = session.query(User).filter(User.email == email).first()
    if is_user_present:
        return {'success': False, 'error': 'Email already in use'}, 404
    hashed_password = str(bcrypt.hashpw(password.encode(
        'utf-8'), bcrypt.gensalt(BCRYPT_SALT))).replace("b'", "").replace("'", "")
    new_user = User(name, email, phone, hashed_password)
    try:
        session.add(new_user)
        session.commit()
        return {'success': True, 'user': user_schema.dump(new_user)}, 201
    except Exception as e:
        return {'success': False, 'error': str(e)}, 404
