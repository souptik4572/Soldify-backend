from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from datetime import date

class SoldItem(Base):
    __tablename__ = 'sold_items'
    id = Column(Integer, primary_key=True)
    sold_date = Column(Date, default=date.today())

    # Creating foreign key to users table
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller = relationship('User', backref='sold_item')

    # Creating foreign key to users table
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer = relationship('User', backref='sold_item')

    # Creating foreign key to products table
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref='sold_item')

    def __init__(self, seller, buyer):
        self.seller = seller
        self.buyer = buyer