import models
import csv


def import_brands_csv():
    with open('brands.csv') as csvfile:
        data=csv.reader(csvfile)
        next(data)
        for row in data:
            brand_name = row[0]
            new_brand = models.Brand(brand_name=brand_name)
            models.session.add(new_brand)
            models.session.commit()
    
    
def import_inventory_csv():
    with open('inventory.csv') as csvfile:
        data=csv.reader(csvfile)
        next(data)
        for row in data:
            product_name = row[0]
            product_price = row[1]
            product_quantity = row[2]
            date_updated = row[3]
            brand_name = row[4]
            
    
if __name__ == '__main__':
    models.Base.metadata.create_all(models.engine)
