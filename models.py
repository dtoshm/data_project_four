from sqlalchemy import (create_engine, Column,
                        Integer, String, Date)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory.db', echo=False)
Base = declarative_base()
Session = sessionmaker(engine)
session = Session()


# Brands
# brand_id | brand_name

# Products 
# product_id | product_name | product_quantity | product_price | date_updated | brand_id
