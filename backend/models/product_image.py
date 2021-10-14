from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from . import Base


class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    link = Column(String(200), nullable=False)
    # Creating foreign key to products table
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref=backref(
        'product_image', cascade="all, delete-orphan"))

    def __init__(self, link, product):
        self.link = link
        self.product = product
