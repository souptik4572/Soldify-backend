from flask import Blueprint, request
from backend.models import Session
from backend.models.user import User
from backend.models.product import Product
from backend.models.interested_buyers import InterestedBuyer
from flask_marshmallow import Marshmallow
from backend.middleware import get_logged_user_id

session = Session()

sold = Blueprint('sold', __name__)

@sold.route('', methods=['GET'])
def get_all_sold_items():
    return 'All items come here'
    