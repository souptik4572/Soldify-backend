from flask import Blueprint, request
from sqlalchemy.sql.schema import Column
from backend.models import Session
from backend.models.user import User
from backend.models.product import Product
from backend.models.product_image import ProductImage
from decouple import config
import jwt
from flask_marshmallow import Marshmallow

session = Session()

SECRET_KEY = config('ACCESS_SECRET_TOKEN')

product = Blueprint('product', __name__)
ma = Marshmallow(product)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('category', 'title', 'price', 'description', 'created_on')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

def populate_images(value):
    result = {}
    if isinstance(value, list):
        result['products'] = products_schema.dump(value)
        for i in range(len(value)):
            result['products'][i]['images'] = []
            for image in value[i].product_image:
                result['products'][i]['images'].append(image.link)
        return result
    result['product'] = product_schema.dump(value)
    result['product']['images'] = []
    for image in value.product_image:
        result['product']['images'].append(image.link)
    return result

def get_logged_user_id(token):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if not user['id']:
            return None, 'Token is invalid'
        return user['id'], 'Token is valid'
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired, please login again'
    except:
        return None, 'Token is invalid'


@product.route('', methods=['GET'])
def get_all_products():
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization').split(' ')[1])
    if not logged_in_id:
        return {'success': False, 'error': message}
    try:
        products = session.query(Product).filter(Product.user_id == logged_in_id).all()
        result = populate_images(products)
        result['success'] = True
        return result
    except Exception as e:
        print(e)
        return {'success': False, 'error': 'Encountered error while creating new product'}


@product.route('', methods=['PUT'])
def create_new_product():
    category = request.json.get('category')
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    images = request.json.get('images')
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization').split(' ')[1])
    if not logged_in_id:
        return {'success': False, 'error': message}
    try:
        user = session.query(User).filter(User.id == logged_in_id).first()
        new_product = Product(category, title, price, description, user)
        session.add(new_product)
        for image_link in images:
            new_product_image = ProductImage(image_link, new_product)
            session.add(new_product_image)
        session.commit()
    except Exception as e:
        print(e)
        return {'success': False, 'error': 'Encountered error while creating new product'}
    product = session.query(Product).join(
        ProductImage).filter(Product.id == new_product.id).first()
    result = populate_images(product)
    result['success'] = True
    return result
