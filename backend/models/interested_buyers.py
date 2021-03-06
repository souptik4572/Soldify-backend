from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base
from datetime import date

class InterestedBuyer(Base):
    __tablename__ = 'interested_buyers'
    id = Column(Integer, primary_key=True)
    contact_date = Column(Date, default=date.today())

    # Creating foreign key to products table
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref=backref('interested_buyer', cascade="all, delete-orphan"))

    # Creating foreign key to users table
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer = relationship('User', backref=backref('interested_buyer', cascade="all, delete-orphan"))

    def __init__(self, product, buyer):
        self.product = product
        self.buyer = buyer