from models import (Base, session, Brand, 
                    Product, engine, desc, asc, func)
import datetime
import csv


def import_brands_csv():
    with open('brands.csv') as csvfile:
        data=csv.reader(csvfile)
        next(data)
        for row in data:
            brand_name = row[0]
            new_brand = Brand(brand_name=brand_name)
            session.add(new_brand)
            session.commit()
    
    
def import_inventory_csv():
    with open('inventory.csv') as csvfile:
        data=csv.reader(csvfile)
        next(data)
        for row in data:
            product_name = row[0]
            product_price = row[1]
            product_quantity = int(row[2])
            date_updated = clean_date(row[3])
            brand_name = row[4]
            
            cleaned_product_price = float(product_price.replace('$', ''))
            price_in_cents = int(cleaned_product_price * 100)
            brand_query = session.query(Brand).filter(Brand.brand_name==brand_name).first().brand_id
            
            new_product = Product(product_name=product_name, product_price=price_in_cents, 
                                         product_quantity=product_quantity, product_updated=date_updated,
                                         brand_id = brand_query)
            
            session.add(new_product)
            session.commit()
      

def clean_price(price_str):
    try:
        cleaned_price = float(price_str.replace('$', ''))
    except ValueError:
        print('\n****** PRICE ERROR ******')
        print('Please enter a price (ex 5.99)')
    else:
        return int(cleaned_price * 100)


def clean_quantity(quantity_str):
    try:
        cleaned_quantity = int(quantity_str)
    except ValueError:
        print('\n****** QUANTITY ERROR ******')
        print('Please enter a quantity (ex 5)')
    else:
        return int(cleaned_quantity)


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except (ValueError, IndexError):
        print('\n****** DATE ERROR ******')
        print('Please enter a date (ex 04/08/2021)')
    else: 
        return return_date


def add_product(new_product):
    existing_product = session.query(Product).filter(Product.product_name==new_product.product_name).first()
    if existing_product:
        if existing_product.product_updated < new_product.product_updated:
            existing_product.product_name = new_product.product_name
            existing_product.product_price = new_product.product_price
            existing_product.product_quantity = new_product.product_quantity
            existing_product.product_updated = new_product.product_updated
            session.commit()
            print("\nProduct Updated\n")
    else:
        session.add(new_product)
        session.commit()
        print("\nProduct Added\n")


def get_product_by_id():
    while True:
        user_selected_product = input("\nEnter a Product ID \n:")
        product = session.query(Product).filter(Product.product_id==user_selected_product).first()
        if product == None:
            print("The product id you have entered has no matching id in the database. Please try again. \n:")
        else:
            print(f'''\nProduct ID: {product.product_id}
                  \rProduct Name: {product.product_name}
                  \rProduct Quantity: {product.product_quantity}
                  \rProduct Price: {product.product_price}
                  \rProduct Updated: {product.product_updated}
                  \rBrand ID: {product.brand_id}\n''')
            break


def user_entered_product():
    product_name = input("\nProduct Name: ")
    price_error = True
    while price_error:
        price = input("Product Price: ")
        price = clean_price(price)
        if type(price) == int:
            price_error = False
    quantity_error = True
    while quantity_error:
        quantity = input("Product Quantity: ")
        quantity = clean_quantity(quantity)
        if type(quantity) == int:
            quantity_error = False
    date_error = True
    while date_error:
        date = input("Product Date Updated (ex 04/08/2021): ")
        date = clean_date(date)
        if type(date) == datetime.date:
            date_error = False
    brand_id = input("Brand ID:")
    new_product = Product(product_name=product_name,
                        product_price=price,
                        product_quantity=quantity,
                        product_updated=date,
                        brand_id=brand_id)
    return new_product


def analysis():
    print("Analysis")
    most_expensive_product = session.query(Product).order_by(desc(Product.product_price)).first()
    least_expensive_product = session.query(Product).order_by(asc(Product.product_price)).first()
    print(f"The most expensive product is: {most_expensive_product.product_name} - ${most_expensive_product.product_price/100}")
    print(f"The least expensive product is: {least_expensive_product.product_name} - ${least_expensive_product.product_price/100}")


def menu():
    print("Welcome\n")
    while True:
        user_input = input("V: View product details \nN:Add New Product \nA:View Analysis \nB:Backup Database \nE:Exit \n:").lower()
        if user_input == "v":
            get_product_by_id()
        elif user_input == "n":
            new_product = user_entered_product()
            add_product(new_product) 
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
    Base.metadata.create_all(engine)
    import_brands_csv()
    import_inventory_csv()
    # menu()
    analysis()
