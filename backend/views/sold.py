from flask import Blueprint, request
from ..models import Session
from ..models.user import User
from ..models.product import Product
from ..models.interested_buyers import InterestedBuyer
from ..models.sold_items import SoldItem
from flask_marshmallow import Marshmallow
from ..middleware import get_logged_user_id
from ..utils.check_args import are_all_args_present

session = Session()

sold = Blueprint('sold', __name__)
ma = Marshmallow(sold)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'category', 'title', 'price',
                  'description', 'created_on')
product_schema = ProductSchema()

def populate_products(values):
    result = []
    for value in values:
        ans = product_schema.dump(value.product)
        ans['sold_date'] = value.sold_date
        ans['is_sold'] = value.is_sold
        result.append(ans)
    return result

@sold.route('', methods=['GET'])
def get_all_sold_items(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    sold_products = session.query(SoldItem).join(Product).filter(
        SoldItem.product_id == product_id and Product.user_id == logged_in_id).all()
    print(sold_products)
    return { 'success': True, 'sold_products': populate_products(sold_products) }       
    

@sold.route('/final', methods=['PATCH'])
def final_sold_product(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    sold_item = session.query(SoldItem).filter(
        SoldItem.product_id == product_id).first()
    if not sold_item:
        return {'success': False, 'error': 'Product with given id has not been assigned to anyone for selling'}, 404
    if sold_item.is_sold:
        return {'success': False, 'error': 'Product with given id, has already been sold'}, 404
    try:
        sold_item.is_sold = True
        session.commit()
        return {'success': True}, 201
    except Exception as e:
        session.rollback()
        return {'success': False, 'error': str(e)}


@sold.route('/add', methods=['PUT'])
def add_sold_item(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    sold_item = session.query(SoldItem).filter(
        SoldItem.product_id == product_id).first()
    if sold_item:
        return {'success': False, 'error': 'Product has already been assigned to a buyer, cannot assign to any other buyer'}, 404
    buyer_id = request.json.get('buyer_id', None)
    if not are_all_args_present(buyer_id):
        return {'success': False, 'error': 'Please provide all the arguments'}, 404
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {'success': False, 'error': 'Product with given id does not exist'}
    interested_buyer = session.query(InterestedBuyer).join(
        User).filter(InterestedBuyer.id == buyer_id).first()
    if not interested_buyer:
        return {'success': False, 'error': 'Interested buyer with given id does not exist'}
    new_sold_product = SoldItem(product, interested_buyer.buyer)
    try:
        session.add(new_sold_product)
        session.commit()
        return {'success': True}, 201
    except Exception as e:
        print(e)
        return {'success': False, 'error': str(e)}


@sold.route('/remove', methods=['DELETE'])
def remove_sold_item(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    sold_item = session.query(SoldItem).filter(
        SoldItem.product_id == product_id).first()
    if not sold_item:
        return {'success': False, 'error': 'Product with given id has not been assigned to anyone for selling'}, 404
    if sold_item.is_sold:
        return {'success': False, 'error': 'Product with given id, has already been sold'}, 404
    try:
        session.delete(sold_item)
        session.commit()
        return {'success': True}, 201
    except Exception as e:
        return {'success': False, 'error': str(e)}
