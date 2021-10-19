from flask import Blueprint, request
from ..models import Session
from ..models.user import User
from ..models.product import Product
from ..models.product_image import ProductImage
from ..models.sold_items import SoldItem
from flask_marshmallow import Marshmallow
from ..middleware import get_logged_user_id
from ..utils.check_args import are_all_args_present
from ..models.base import session

product = Blueprint('product', __name__)
ma = Marshmallow(product)


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'category', 'title', 'price',
                  'description', 'created_on')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


def populate_images_and_is_sold(value, exclude_sold=False):
    result = {'success': True}
    if isinstance(value, list):
        result['products'] = products_schema.dump(value)
        for i in range(len(result['products'])):
            result['products'][i]['images'] = []
            for image in value[i].product_image:
                result['products'][i]['images'].append(image.link)
            if value[i].sold_item:
                result['products'][i]['is_sold'] = value[i].sold_item.is_sold
            else:
                result['products'][i]['is_sold'] = False
        if exclude_sold:
            result['products'] = [a_product for a_product in result['products'] if a_product['is_sold']]
        return result
    result['product'] = product_schema.dump(value)
    result['product']['images'] = []
    if value.sold_item:
        result['product']['is_sold'] = value.sold_item.is_sold
    else:
        result['product']['is_sold'] = False
    for image in value.product_image:
        result['product']['images'].append(image.link)
    return result


def update_product_images(product_id, images, particular_product):
    particular_product_images = session.query(ProductImage).filter(
        ProductImage.product_id == product_id).all()
    existing_images = set(
        [image.link for image in particular_product_images if image.link in images])
    deleted_images = set(
        [image for image in particular_product_images if image.link not in images])
    new_images = set(images) - existing_images
    for new_image in new_images:
        new_product_image = ProductImage(new_image, particular_product)
        session.add(new_product_image)
    for delete_image in deleted_images:
        session.delete(delete_image)


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
        category = request.json.get('category', None)
        title = request.json.get('title', None)
        price = request.json.get('price', None)
        description = request.json.get('description', None)
        created_on = request.json.get('created_on', None)
        images = request.json.get('images', None)
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
        if images:
            update_product_images(product_id, images, particular_product)
        session.commit()
        return populate_images_and_is_sold(particular_product), 201
    except Exception as e:
        session.rollback()
        return {'success': False, 'error': str(e)}, 404


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
        return {'success': True}, 201
    except Exception as e:
        return {'success': False, 'error': str(e)}, 404


@product.route('/<int:product_id>', methods=['GET'])
def get_particular_product(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    try:
        particular_product = session.query(Product).join(
            ProductImage).outerjoin(SoldItem).filter(Product.id == product_id).first()
        if not particular_product:
            return {'success': False, 'error': 'Product does not exist'}, 404
        return populate_images_and_is_sold(particular_product), 200
    except Exception as e:
        return {'success': False, 'error': str(e)}, 404


@product.route('/own', methods=['GET'])
def get_own_products():
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    try:
        products = session.query(Product).outerjoin(SoldItem).filter(
            Product.user_id == logged_in_id).all()
        if not products:
            return {'success': False, 'error': 'Products does not exist'}, 404
        result = populate_images_and_is_sold(products)
        return result, 200
    except Exception as e:
        return {'success': False, 'error': str(e)}, 404


@product.route('/all', methods=['GET'])
def get_all_products():
    try:
        products = session.query(Product).outerjoin(SoldItem).all()
        if not products:
            return {'success': False, 'error': 'Products does not exist'}, 404
        result = populate_images_and_is_sold(products, True)
        return result, 200
    except Exception as e:
        return {'success': False, 'error': str(e)}, 404


@product.route('', methods=['PUT'])
def create_new_product():
    category = request.json.get('category', None)
    title = request.json.get('title', None)
    price = request.json.get('price', None)
    description = request.json.get('description', None)
    images = request.json.get('images', None)
    if not images:
        return {'success': False, 'error': 'Please provide all the arguments'}, 404
    images = set(images)
    if not are_all_args_present(category, title, price, description, images):
        return {'success': False, 'error': 'Please provide all the arguments'}, 404
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
        return {'success': False, 'error': str(e)}, 404
    return {'success': True}, 201
