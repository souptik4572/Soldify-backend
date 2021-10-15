from flask import Blueprint, request
from ..models import Session
from ..models.user import User
from ..models.product import Product
from ..models.interested_buyers import InterestedBuyer
from flask_marshmallow import Marshmallow
from ..middleware import get_logged_user_id

session = Session()

sold = Blueprint('sold', __name__)

@sold.route('', methods=['GET'])
def get_all_sold_items():
    return 'All items come here'
    