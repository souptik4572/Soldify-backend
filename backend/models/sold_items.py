from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from models import Base
from datetime import date


class SoldItem(Base):
    __tablename__ = 'sold_items'
    id = Column(Integer, primary_key=True)
    sold_date = Column(Date, default=date.today())

    # Creating foreign key to users table
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller = relationship('User', backref=backref(
        'sold_item', cascade="all, delete-orphan"))

    # Creating foreign key to users table
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer = relationship('User', backref=backref(
        'sold_item', cascade="all, delete-orphan"))

    # Creating foreign key to products table
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref=backref('sold_item', cascade="all, delete-orphan"))

    def __init__(self, seller, buyer):
        self.seller = seller
        self.buyer = buyer
