from sqlalchemy import (create_engine, Column, Integer, 
                        String, Date, ForeignKey, desc, asc, func)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


# Database Configuration
engine = create_engine('sqlite:///inventory.db', echo=False)
Base = declarative_base()
Session = sessionmaker(engine)
session = Session()

    
class Brand(Base):
    __tablename__ = "Brands"
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)
    products = relationship("Product", back_populates="brand", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"brand_id: {self.brand_id}, brand_name:{self.brand_name}"


class Product(Base):
    __tablename__ = "Products"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    product_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey('Brands.brand_id'))
    brand = relationship("Brand", back_populates="products")
    
    def __repr__(self):
        return f'''product_id: {self.product_id},
                   \rproduct_name: {self.product_name},
                   \rproduct_quantity: {self.product_quantity},
                   \rproduct_price: {self.product_price},
                   \rproduct_updated: {self.product_updated},
                   \rbrand_id: {self.brand_id},
                   \rbrand: {self.brand}'''
