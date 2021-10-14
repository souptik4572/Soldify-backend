from flask import Blueprint, request
from sqlalchemy.sql.schema import Column
from backend.models import Session
from backend.models.user import User
from backend.models.product import Product
from backend.models.product_image import ProductImage
from flask_marshmallow import Marshmallow
from backend.middleware import get_logged_user_id

session = Session()

product = Blueprint('product', __name__)
ma = Marshmallow(product)


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('category', 'title', 'price', 'description', 'created_on')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


def populate_images(value):
    result = { 'success': True }
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


@product.route('/<int:product_id>', methods=['PATCH'])
def edit_particular_product(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    try:
        particular_product = session.query(Product).join(
            ProductImage).filter(Product.id == product_id).first()
        if not particular_product:
            return {'success': False, 'error': 'Product does not exist'}, 404
        if logged_in_id != particular_product.user_id:
            return {'success': False, 'error': 'You are not authorized to edit this product'}, 404
        category = request.json.get('category')
        title = request.json.get('title')
        price = request.json.get('price')
        description = request.json.get('description')
        created_on = request.json.get('created_on')
        print(category, title, price, description)
        if category:
            particular_product.category = category
        if title:
            particular_product.title = title
        if price:
            particular_product.price = price
        if description:
            particular_product.description = description
        if created_on:
            particular_product.created_on = created_on
        session.commit()
        return populate_images(particular_product), 201
    except Exception as e:
        return {'success': False, 'error': 'Encountered error while editing particular product'}, 404


@product.route('/<int:product_id>', methods=['DELETE'])
def delete_particular_product(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    try:
        particular_product = session.query(Product).join(
            ProductImage).filter(Product.id == product_id).first()
        if not particular_product:
            return {'success': False, 'error': 'Product does not exist'}, 404
        if logged_in_id != particular_product.user_id:
            return {'success': False, 'error': 'You are not authorized to delete this product'}, 404
        session.delete(particular_product)
        session.commit()
        return { 'success': True }, 201
    except Exception as e:
        return {'success': False, 'error': 'Encountered error while deleting particular product'}, 404


@product.route('/<int:product_id>', methods=['GET'])
def get_particular_product(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    try:
        particular_product = session.query(Product).join(
            ProductImage).filter(Product.id == product_id).first()
        if not particular_product:
            return {'success': False, 'error': 'Product does not exist'}, 404
        return populate_images(particular_product), 200
    except Exception as e:
        return {'success': False, 'error': 'Encountered error while fetching particular product'}, 404


@product.route('', methods=['GET'])
def get_all_products():
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    try:
        products = session.query(Product).filter(
            Product.user_id == logged_in_id).all()
        if not products:
            return {'success': False, 'error': 'Products does not exist'}, 404
        result = populate_images(products)
        return result, 200
    except Exception as e:
        return {'success': False, 'error': 'Encountered error while creating new product'}, 404


@product.route('', methods=['PUT'])
def create_new_product():
    category = request.json.get('category')
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    images = request.json.get('images')
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    try:
        user = session.query(User).filter(User.id == logged_in_id).first()
        if not user:
            return {'success': False, 'error': 'User does not exist'}, 404
        new_product = Product(category, title, price, description, user)
        session.add(new_product)
        for image_link in images:
            new_product_image = ProductImage(image_link, new_product)
            session.add(new_product_image)
        session.commit()
    except Exception as e:
        return {'success': False, 'error': 'Encountered error while creating new product'}, 404
    return {'success': True}, 201
