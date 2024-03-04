import models
import datetime
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
            product_quantity = int(row[2])
            date_updated = make_date(row[3])
            brand_name = row[4]
            
            cleaned_product_price = float(product_price.replace('$', ''))
            price_in_cents = int(cleaned_product_price * 100)
            brand_query = models.session.query(models.Brand).filter(models.Brand.brand_name==brand_name).first().brand_id
            
            new_product = models.Product(product_name=product_name, product_price=price_in_cents, 
                                         product_quantity=product_quantity, product_updated=date_updated,
                                         brand_id = brand_query)
            
            models.session.add(new_product)
            models.session.commit()
      

def make_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return_date = datetime.date(year, month, day)
    return return_date      


def menu():
    print("Welcome")
    while True:
        user_input = input("V: View product details \nN:Add New Product \nA:View Analysis \nB:Backup Database \nE:Exit \n:").lower()
        if user_input == "v":
            print("View Details")
        elif user_input == "n":
            print("Add New Product")
        elif user_input == "a":
            print("View Anaylsis")
        elif user_input == "b":
            print("Backup Database")
        elif user_input == "e":
            print("Exit Program")
            break
        else:
            print("\nPlease enter a valid menu option\n")

    
if __name__ == '__main__':
    models.Base.metadata.create_all(models.engine)
    import_brands_csv()
    import_inventory_csv()
    menu()
