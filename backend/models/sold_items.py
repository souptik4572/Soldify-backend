from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base
from datetime import date


class SoldItem(Base):
    __tablename__ = 'sold_items'
    id = Column(Integer, primary_key=True)
    sold_date = Column(Date, default=date.today())
    is_sold = Column(Boolean, default=False)

    # Creating foreign key to users table
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer = relationship('User', backref=backref(
        'sold_item', uselist=False, cascade="all, delete-orphan"))

    # Creating foreign key to products table
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref=backref(
        'sold_item', uselist=False, cascade="all, delete-orphan"))

    def __init__(self, product, buyer):
        self.product = product
        self.buyer = buyer
