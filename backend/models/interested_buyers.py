from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from datetime import date

class InterestedBuyer(Base):
    __tablename__ = 'interested_buyers'
    id = Column(Integer, primary_key=True)
    contact_date = Column(Date, default=date.today())

    # Creating foreign key to users table
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller = relationship('User', backref='interested_buyer')

    # Creating foreign key to users table
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer = relationship('User', backref='interested_buyer')

    def __init__(self, seller, buyer):
        self.seller = seller
        self.buyer = buyer