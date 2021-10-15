from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base
from datetime import date


class Category(Enum):
    books = 'books'
    electronics = 'electronics'
    sports = 'sports'
    clothing = 'clothing'
    furniture = 'furniture'
    cars = 'cars'
    other = 'other'


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    category = Column(Enum('books', 'electronics', 'sports', 'clothing',
                      'furniture', 'cars', 'other', name='Category'), nullable=False, default='other')
    title = Column(String(150), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False)
    created_on = Column(Date, default=date.today())

    # Creating foreign key to users table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref(
        'product', cascade='all, delete-orphan'))

    def __init__(self, category, title, price, description, user, created_on=date.today()):
        self.category = category
        self.title = title
        self.price = price
        self.description = description
        self.user = user
        self.created_on = created_on
