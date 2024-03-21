from models import (Base, session, Brand, 
                    Product, engine, desc, asc, func)
import datetime
import csv


def check_for_database():
    """
    Checks if the database is empty by counting the number of records in the Brand and Product tables.
    If both tables are empty, it triggers functions to import data from CSV files (import_brands_csv, import_inventory_csv).

    :return: None
    """
    if session.query(Brand).count() == 0 and session.query(Product).count() == 0:
        import_brands_csv()
        import_inventory_csv()


def import_brands_csv():
    """
    Reads data from a CSV file named 'brands.csv' and imports brand names into the Brands table in the database.
    Assumes that the CSV file has a header row.
    
    :return: None
    """
    with open('brands.csv') as csvfile:
        data=csv.reader(csvfile)
        next(data)
        for row in data:
            brand_name = row[0]
            new_brand = Brand(brand_name=brand_name)
            session.add(new_brand)
            session.commit()
    
    
def import_inventory_csv():
    """
    Reads data from a CSV file named 'inventory.csv' and imports inventory information into the Products table in the database.
    Converts product price to cents, parses date strings, and associates products with existing brands in the database.
    Assumes that the CSV file has a header row containing columns for product name, price, quantity, date updated, and brand name.

    :return: None
    """
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
            
            # Query the database to get the brand_id
            brand_query = session.query(Brand).filter(Brand.brand_name==brand_name).first().brand_id
            if brand_query:
                new_product = Product(product_name=product_name, 
                                      product_price=price_in_cents,
                                      product_quantity=product_quantity, 
                                      product_updated=date_updated,
                                      brand_id = brand_query) 
                add_product(new_product)
            else:
                print(f"Brand {brand_query} has not been found in the database.")


def backup_products_to_csv():
    """
    Backs up product data from the database to a CSV file named 'inventory_backup.csv'.
    Exports product name, price, quantity, date updated, and brand name.

    :return: None
    """
    products = session.query(Product).all()
    if not products:
        print("No products to export.")
        return
    
    csv_file_path = 'inventory_backup.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['product_name', 'product_price', 'product_quantity', 'date_updated', 'brand_name'])
        for product in products:
            
            date_str = str(product.product_updated).split('-')
            formatted_date = f'{date_str[1]}/{date_str[2]}/{date_str[0]}'
            
            csv_writer.writerow([product.product_name, 
                                 str(f'${product.product_price / 100}'), 
                                 str(product.product_quantity), 
                                 formatted_date,
                                 product.brand.brand_name
                                ])
    print(f"Data Exported To: {csv_file_path}")


def clean_price(price_str):
    """
    Cleans and converts a price string into an integer representing cents.

    :param price_str: String representing a price with or without a dollar sign (e.g., "$5.99" or "5.99").
    :return: Integer representing the price in cents, or None if price cleaning fails.
    """
    try:
        cleaned_price = float(price_str.replace('$', ''))
    except ValueError:
        print('****** PRICE ERROR ******')
        print('Please enter a price (ex 5.99)')
    else:
        return int(cleaned_price * 100)


def clean_quantity(quantity_str):
    """
    Cleans and converts a quantity string into an integer.

    :param quantity_str: String representing a quantity (e.g., "5").
    :return: Integer representing the quantity, or None if cleaning fails.
    """
    try:
        cleaned_quantity = int(quantity_str)
    except ValueError:
        print('****** QUANTITY ERROR ******')
        print('Please enter a quantity (ex 5)')
    else:
        return int(cleaned_quantity)


def clean_date(date_str):
    """
    Cleans and converts a date string in 'MM/DD/YYYY' format to a datetime.date object.

    :param date_str: String representing a date in 'MM/DD/YYYY' format (e.g., "04/08/2021").
    :return: datetime.date object representing the cleaned date, or None if cleaning fails.
    """
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except (ValueError, IndexError):
        print('****** DATE ERROR ******')
        print('Please enter a date (ex 04/08/2021)')
    else: 
        return return_date


def user_entered_product():
    """
    Guides the user to input product details and creates a new Product object.

    :return: New Product object based on user input.
    """
    product_name = input("Product Name: ")
    
    # Validate and clean price input
    price_error = True
    while price_error:
        price = input("Product Price: ")
        price = clean_price(price)
        if type(price) == int:
            price_error = False
     
    # Validate and clean quantity input
    quantity_error = True
    while quantity_error:
        quantity = input("Product Quantity: ")
        quantity = clean_quantity(quantity)
        if type(quantity) == int:
            quantity_error = False
    
    # Validate and clean date input
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


def add_product(new_product):
    """
    Adds a new product to the database or updates an existing product if a newer version is provided.

    :param new_product: Product object representing the new or updated product to be added or updated.
    :return: None
    """
    existing_product = session.query(Product).filter(Product.product_name==new_product.product_name).first()
    
    if existing_product:
        if existing_product.product_updated < new_product.product_updated:
            # Update existing product with newer details
            existing_product.product_name = new_product.product_name
            existing_product.product_price = new_product.product_price
            existing_product.product_quantity = new_product.product_quantity
            existing_product.product_updated = new_product.product_updated
            session.commit()
    else:
        # Add new product to the database
        session.add(new_product)
        session.commit()


def delete_product(product_id):
    """
    Deletes a product from the database based on its product_id.

    :param product_id: Integer representing the unique identifier of the product to be deleted.
    :return: None
    """
    the_product = session.query(Product).filter(Product.product_id==product_id).first()
    if the_product:
        session.delete(the_product)
        session.commit()
    else:
        print(f"Product with ID {product_id} not found in the database.")


def get_product_by_id():
    """
    Retrieves and displays product details based on a user-provided Product ID.

    Continues to prompt the user until a valid Product ID is entered.
    
    :return: String representing the user-entered Product ID.
    """
    while True:
        user_product_id = input("Enter a Product ID:")
        product = session.query(Product).filter(Product.product_id==user_product_id).first()
        
        if product == None:
            print("The product id you entered has no matching id in the database. Please try again.")
        else:
            print(f'''Product ID: {product.product_id}
                  \rProduct Name: {product.product_name}
                  \rProduct Price: ${product.product_price/100}
                  \rProduct Quantity: {product.product_quantity}
                  \rProduct Updated: {product.product_updated}
                  \rBrand ID: {product.brand_id}
                  \rBrand: {product.brand.brand_name}''')
            break
    return user_product_id


def analysis():
    """
    Performs analysis on the products and brands in the database and prints relevant information.

    Prints:
    - The most expensive product and its price.
    - The least expensive product and its price.
    - The brand with the most products and the number of products.
    - The product with the most quantity in the inventory.

    :return: None
    """
    print("Analysis")
    
    # Find the most expensive product
    most_expensive_product = session.query(Product).order_by(desc(Product.product_price)).first()
    print(f"The most expensive product is: {most_expensive_product.product_name} - ${most_expensive_product.product_price/100}")
    
    # Find the least expensive product
    least_expensive_product = session.query(Product).order_by(asc(Product.product_price)).first()
    print(f"The least expensive product is: {least_expensive_product.product_name} - ${least_expensive_product.product_price/100}")
    
    # Find the brand with the most products
    brand_most_products = session.query(Brand.brand_name, func.count(Product.product_id)).join(Product).group_by(Brand.brand_id).order_by(func.count(Product.product_id).desc()).first()
    print(f"The brand with the most products is: {brand_most_products[0]} - {brand_most_products[1]} products")
    
    # Find the product with the most quantity in inventory
    most_quantity_product = session.query(Product).order_by(desc(Product.product_quantity)).first()
    print(f"The product with the most quantity in the inventory is: {most_quantity_product.product_name} - {most_quantity_product.product_quantity}")


def menu():
    """
    Displays a menu for interacting with the database and performs corresponding actions based on user input.

    Menu options:
    - V: View product details, with options to edit or delete a product
    - N: Add a new product
    - A: View analysis of products and brands
    - B: Backup database to CSV
    - X: Exit the program

    :return: None
    """
    check_for_database()
    print("\nWelcome\n")
    
    while True:
        user_input = input("V: View product details \nN:Add New Product \nA:View Analysis \nB:Backup Database \nX:Exit \n:").lower()    
        
        if user_input == "v":
            change_product = get_product_by_id()
            
            while True:
                user_decision = input("E: Edit Product \nD: Delete Product: \nX: Exit \n:").lower()
                
                if user_decision == "e":
                    new_product = user_entered_product()
                    add_product(new_product) 
                
                elif user_decision == "d":
                    delete_product(change_product)
                    print("Product Deleted")
                    break
                
                elif user_decision == "x":
                    break
                
                else:
                    print("Please enter y or n")       
        
        elif user_input == "n":
            new_product = user_entered_product()
            add_product(new_product) 
        
        elif user_input == "a":
            analysis()
        
        elif user_input == "b":
            backup_products_to_csv()
        
        elif user_input == "x":
            print("Exit Program")
            break
        
        else:
            print("Please enter a valid menu option")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    menu()
