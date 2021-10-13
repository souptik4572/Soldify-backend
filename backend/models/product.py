from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from datetime import date

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    category = Column(String(20), nullable=False)
    title = Column(String(150), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False)
    created_on = Column(Date, default=date.today())

    # Creating foreign key to users table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='product')

    def __init__(self, category, title, price, description, user):
        self.category = category
        self.title = title
        self.price = price
        self.description = description
        self.user = user
