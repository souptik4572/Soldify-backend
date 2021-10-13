from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class ProductImage(Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True)
    
    # Creating foreign key to products table
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref='product_image')

    def __init__(self, product):
        self.product = product