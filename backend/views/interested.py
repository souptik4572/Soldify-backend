from flask import Blueprint, request
from ..models import Session
from ..models.user import User
from ..models.product import Product
from ..models.interested_buyers import InterestedBuyer
from flask_marshmallow import Marshmallow
from ..middleware import get_logged_user_id
from ..models.base import session

interested = Blueprint('interested', __name__)
ma = Marshmallow(interested)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone')


user_schema = UserSchema()


def get_buyers_list(interested_buyers):
    result = []
    for element in interested_buyers:
        result.append(user_schema.dump(element.buyer))
    return result


@interested.route('', methods=['GET'])
def get_all_interested_buyers(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    interested_buyers = session.query(InterestedBuyer).join(Product).join(User).filter(
        InterestedBuyer.product_id == product_id, Product.user_id == logged_in_id).all()
    return {'success': True, 'buyers': get_buyers_list(interested_buyers)}, 200


@interested.route('/add', methods=['PUT'])
def add_interested_buyer(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    product = session.query(Product).join(
        User).filter(Product.id == product_id).first()
    if not product:
        return {'success': False, 'error': 'Product with given id does not exist'}, 404
    if product.user_id == logged_in_id:
        return {'success': False, 'error': 'Seller cannot buy their own product'}, 404
    interested_buyer = session.query(InterestedBuyer).join(Product).filter(
        InterestedBuyer.product_id == product_id and InterestedBuyer.buyer_id == logged_in_id).first()
    if interested_buyer:
        return {'success': False, 'error': 'Logged in user is already an interested buyer of the product'}
    buyer = session.query(User).filter(User.id == logged_in_id).first()
    if not buyer:
        return {'success': False, 'error': 'Buyer with given id does not exist'}, 404
    try:
        new_interested_buyer = InterestedBuyer(product, buyer)
        session.add(new_interested_buyer)
        session.commit()
        return {'success': True}, 201
    except Exception as e:
        return {'success': False, 'error': str(e)}


@interested.route('/remove', methods=['DELETE'])
def remove_interested_buyer(product_id):
    logged_in_id, message = get_logged_user_id(
        request.headers.get('Authorization'))
    if not logged_in_id:
        return {'success': False, 'error': message}, 404
    interested_buyer = session.query(InterestedBuyer).filter(
        InterestedBuyer.buyer_id == logged_in_id).first()
    if not interested_buyer:
        return {'success': False, 'error': 'Logged in user is not a buyer for this product'}, 404
    try:
        session.delete(interested_buyer)
        session.commit()
        return {'success': True}, 201
    except Exception as e:
        return {'success': False, 'error': str(e)}
