from sqlalchemy import (create_engine, Column,
                        Integer, String, Date)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///inventory.db', echo=False)
Base = declarative_base()
Session = sessionmaker(engine)
session = Session()


class Brand(Base):
    __tablename__ = "Brands"
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)

    def __repr__(self):
        return f"brand_name:{self.brand_name}"


class Product(Base):
    __tablename__ = "Products"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    product_updated = Column(Date)
    brand_id = relationship("Brand", back_populates="brand_id",
                                    cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return f'''product_name: {self.product_name},
                   \rproduct_quantity: {self.product_quantity},
                   \rproduct_price: {self.product_price},
                   \rproduct_updated: {self.product_updated},
                   \rbrand_id: {self.brand_id}'''
