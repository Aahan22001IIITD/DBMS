import mysql.connector
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dbms_project"
)
cursor = cnx.cursor()
query = "SELECT * FROM CUSTOMERS"
query_wallet = "SELECT * FROM WALLET"
query_cart = "SELECT * FROM CART"
query_consists_of = "SELECT * FROM CONSISTS_OF"
query_discount_and_offers = "SELECT * FROM DISCOUNT_AND_OFFERS"
cursor.execute(query)
users_data = cursor.fetchall()
query_admin = "SELECT * FROM ADMINS"
cursor.execute(query_admin)
adminsdata = cursor.fetchall()
cursor.execute(query_consists_of)
consists_of_data = cursor.fetchall()
cursor.execute(query_discount_and_offers)
discount_offers_data = cursor.fetchall()
admindata=[]
for admin in adminsdata:
    admindata.append(admin[2])
# print(admindata)
cursor.execute(query_wallet)
wallet_data = cursor.fetchall()
cursor.execute(query_cart)
cart_data = cursor.fetchall()
# for wallet in wallet_data :
#     print(wallet)
# for cart in cart_data:
#     print(cart)
last_entry = users_data[-1]
def login():
    login_window.destroy()
    register_window = tk.Tk()
    register_window.title("Login")

    email_label = tk.Label(register_window, text="Email ID:")
    email_label.grid(row=1, column=0, padx=5, pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.grid(row=1, column=1, padx=5, pady=5)

    password_label = tk.Label(register_window, text="Password:")
    password_label.grid(row=2, column=0, padx=5, pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5)
    
    def func():
        email = email_entry.get()
        password = password_entry.get()
        # print(email)
        # print(password)
        for user_data in users_data:
            if email == user_data[2] and password == user_data[3]:
                messagebox.showinfo("Login successful!")
                register_window.destroy()
                userinterface(user_data)
                return
        messagebox.showerror("Error", "Invalid email Id or password")
        
    login_button = tk.Button(register_window , text ="login" , command=func)
    login_button.grid(row=5, columnspan=2, padx=5, pady=5)
def userinterface(user_data):
    user_window = tk.Tk()
    user_window.title("Login")
    products_button = tk.Button(user_window, text="See Products", command=lambda: open_product_selection_window(user_data))
    wallet_button = tk.Button(user_window, text="See Wallet", command=lambda: open_wallet_window(user_data, wallet_data))
    seeDiscountButton = tk.Button(user_window, text="See discounts", command=lambda: open_discount_window(discount_offers_data))
    seeCartButton = tk.Button(user_window, text="See Cart", command=lambda: open_cart_window(user_data, consists_of_data))
    place_order_button = tk.Button(user_window, text="Place Order", command=lambda: place_order(user_data, consists_of_data))
    products_button.grid(row=5, column=1, padx=5, pady=5)
    wallet_button.grid(row=5, column=2, padx=5, pady=5)
    seeDiscountButton.grid(row=5, column=3, padx=5, pady=5)
    seeCartButton.grid(row=5, column=4, padx=5, pady=5)
    place_order_button.grid(row=5, column=5, padx=5, pady=5)

def place_order(user_data, consists_of_data):
    product_counts = {} # {orderId : quantity}
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query)
    tot_products = cursor.fetchall()
    tot_amount = 0
    for data in consists_of_data:
        if data[2] == user_data[6]:
            product_counts[data[1]] = product_counts.get(data[1], 0) + 1
    cart_id = data[2]


    order_placed = True
    for key in product_counts.keys():
        c1 = product_counts.get(key, 0)
        for product in tot_products:
            tot_amount += product[3]
            if product[0] == key and c1 > int(product[6]):
                order_placed = False
                break
    
    if order_placed == False:
        error_window = tk.Tk()
        error_window.title("Error")
        error_label = tk.Label(error_window, text="Order cannot be processed due to unavailability of items.")
        error_label.pack()
        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack()
        error_window.mainloop()
    else:
        for key in product_counts.keys():
            c1 = product_counts.get(key, 0)
            for i, product in enumerate(tot_products):
                if product[0] == key:
                    cursor.execute("UPDATE products SET quantity = %s WHERE product_id = %s", (int(product[6])-c1, key))
                    if int(product[6])-c1 == 0:
                        cursor.execute("UPDATE products SET is_available = %s WHERE product_id = %s", (False, key))

                    

        query = "DELETE FROM consists_of WHERE cart_id = %s"
        cart_id = user_data[5]
        values = (cart_id,)
        cursor.execute(query, values)
        cnx.commit()

        # delete all the cart contents
        current_date = datetime.now().date().strftime('%Y-%m-%d')
        current_time = datetime.now().time().strftime('%H:%M:%S')

        query = "INSERT INTO transactions (payment_method, transaction_date, transaction_time, amount) VALUES ('Credit Card', %s, %s, 123.45)"
        values = (current_date, current_time)
        cursor.execute(query, values)
        cnx.commit()

        

        query = "INSERT INTO orders (order_date, order_time, order_statuss, total_amount, cart_id, discount_id, transactions_id, admin_id, agent_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (current_date, current_time, False, tot_amount, user_data[6], None, 510, 100, 7232)
        cursor.execute(query, values)
        cnx.commit()



        success_window = tk.Tk()
        success_window.title("Order Placed")
        success_label = tk.Label(success_window, text="Order Placed Successfully!\nTotal Amount: {}".format(tot_amount))
        success_label.pack()
        ok_button = tk.Button(success_window, text="OK", command=success_window.destroy)
        ok_button.pack()
        success_window.mainloop()



def open_cart_window(user_data, consists_of_data):
    product_counts = {}
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query)
    tot_products = cursor.fetchall()
    
    for data in consists_of_data:
        if data[2] == user_data[6]:
            product_counts[data[1]] = product_counts.get(data[1], 0) + 1

    product_window = tk.Tk()
    product_window.title("Product Counts")
    heading_label = tk.Label(product_window, text="Product Counts")
    heading_label.pack()
    product_listbox = tk.Listbox(product_window)
    for product_id, count in product_counts.items():
        for product in tot_products:
            if product[0] == product_id:
                product_listbox.insert(tk.END, f"{product[1]}: {count}")

    product_listbox.pack()
    product_window.mainloop()

def open_wallet_window(user_data, wallet_data):
    wallet_window = tk.Toplevel()
    wallet_window.title("Wallet Details")

    user_wallet = None
    for wallet in wallet_data:
        if wallet[0] == user_data[7]:
            user_wallet = wallet
            break

    if user_wallet is None:
        label = tk.Label(wallet_window, text="Wallet not found.")
        label.pack()
    else:
        label_id = tk.Label(wallet_window, text=f"Wallet ID: {user_wallet[0]}")
        label_id.pack()
        label_balance = tk.Label(wallet_window, text=f"Wallet Balance: {user_wallet[1]}")
        label_balance.pack()

    wallet_window.mainloop()


def open_discount_window(discount_offers_data):
    discount_window = tk.Tk()
    discount_window.title("Discount Offers")

    tk.Label(discount_window, text="Discount ID").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(discount_window, text="Description").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(discount_window, text="Discount Percentage").grid(row=0, column=2, padx=5, pady=5)

    for idx, discount_offer in enumerate(discount_offers_data, start=1):
        tk.Label(discount_window, text=discount_offer[0]).grid(row=idx, column=0, padx=5, pady=5)
        tk.Label(discount_window, text=discount_offer[1]).grid(row=idx, column=1, padx=5, pady=5)
        tk.Label(discount_window, text=discount_offer[2]).grid(row=idx, column=2, padx=5, pady=5)

    discount_window.mainloop()


def admin_login():
    login_window.destroy()
    admin_login_window = tk.Tk()
    admin_login_window.title("Admin - Login")

    email_label = tk.Label(admin_login_window, text="Email ID:")
    email_label.grid(row=0, column=0, padx=5, pady=5)
    email_entry = tk.Entry(admin_login_window)
    email_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = tk.Label(admin_login_window, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(admin_login_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    adminEmailIfValid = ""
    def validate_admin_login():
        email = email_entry.get()
        password = password_entry.get()
        
        admin_query = "SELECT * FROM admins WHERE email = %s AND password = %s"
        cursor.execute(admin_query, (email, password))
        admin_data = cursor.fetchone()
        if admin_data:
            admin_login_window.destroy()

            open_admin_dashboard(admin_data)
            open_admin_dashboard(admin_data)
        else:
            messagebox.showerror("Error", "Invalid admin credentials")

    login_button = tk.Button(admin_login_window, text="Login", command=validate_admin_login)
    login_button.grid(row=2, columnspan=2, padx=5, pady=5)

    admin_login_window.mainloop()
def view_products():

    query = "SELECT * FROM products"
    cursor.execute(query)
    products = cursor.fetchall()
    

    product_window = tk.Toplevel()
    product_window.title("Products")
    

    listbox = tk.Listbox(product_window, width=50, height=20)
    listbox.pack(padx=10, pady=10)
    

    for product in products:
        listbox.insert(tk.END, f"{product[0]} - {product[1]} ({product[2]}) - Price: {product[3]} - Available: {product[4]} - Admin ID: {product[5]} - Quantity: {product[6]} - Measuring Type: {product[7]}")

def add_product():
    add_window = tk.Toplevel()
    add_window.title("Add Product")
    tk.Label(add_window, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(add_window, text="Category:").grid(row=1, column=0, padx=5, pady=5)
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Price:").grid(row=2, column=0, padx=5, pady=5)
    price_entry = tk.Entry(add_window)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Is Available (1 for True, 0 for False):").grid(row=3, column=0, padx=5, pady=5)
    available_entry = tk.Entry(add_window)
    available_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Admin ID:").grid(row=4, column=0, padx=5, pady=5)
    admin_id_entry = tk.Entry(add_window)
    admin_id_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Quantity:").grid(row=5, column=0, padx=5, pady=5)
    quantity_entry = tk.Entry(add_window)
    quantity_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Measuring Type:").grid(row=6, column=0, padx=5, pady=5)
    measuring_entry = tk.Entry(add_window)
    measuring_entry.grid(row=6, column=1, padx=5, pady=5)

    def add_product_to_db():
        name = name_entry.get()
        category = category_entry.get()
        price = float(price_entry.get())
        is_available = bool(int(available_entry.get()))
        admin_id = int(admin_id_entry.get())
        quantity = int(quantity_entry.get())
        measuring_type = measuring_entry.get()

        query = "INSERT INTO products (product_name, category, price, is_available, admin_id, quantity, measuring_type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (name, category, price, is_available, admin_id, quantity, measuring_type)
        cursor.execute(query, data)
        cnx.commit()

        messagebox.showinfo("Success", "Product added successfully!")
        add_window.destroy()

    tk.Button(add_window, text="Add Product", command=add_product_to_db).grid(row=7, columnspan=2, padx=5, pady=5)

def remove_product():
    remove_window = tk.Toplevel()
    remove_window.title("Remove Product")
    tk.Label(remove_window, text="Product ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(remove_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    def remove_product_from_db():
        product_id = id_entry.get()
        query = "DELETE FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        cnx.commit()

        messagebox.showinfo("Success", "Product removed successfully!")
        remove_window.destroy()

    tk.Button(remove_window, text="Remove Product", command=remove_product_from_db).grid(row=1, columnspan=2, padx=5, pady=5)

def open_admin_dashboard(admin_data):
    admin_dashboard = tk.Tk()
    admin_dashboard.title("Admin Dashboard")
    tk.Button(admin_dashboard, text="View Products", command=view_products).pack(pady=5)
    tk.Button(admin_dashboard, text="Add Product", command=add_product).pack(pady=5)
    tk.Button(admin_dashboard, text="Remove Product", command=remove_product).pack(pady=5)
    admin_dashboard.mainloop()

def getProducts():
    products=[]
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query)
    tot_products = cursor.fetchall()
    for product in tot_products:
        if(product[4]):#if that product is available
            products.append(product[1])
    return products
def AddToCart(user_data, selected_item, consists_of_data):
    query = "SELECT * FROM PRODUCTS"
    cursor.execute(query)
    tot_products = cursor.fetchall()
    # print(user_data)
    # print(selected_item)
    # print(consists_of_data)
    # print(tot_products)

    cart_id = user_data[6]
    product_id = None
    order_id = consists_of_data[len(consists_of_data)-1][0]+1

    for product in tot_products:
        if product[1] == selected_item:
            product_id = product[0]
            break

    consists_of_data.append((order_id, product_id, cart_id))
    query = "INSERT INTO consists_of (order_id, product_id, cart_id) VALUES (%s, %s, %s)"
    values = (order_id, product_id, cart_id)
    cursor.execute(query, values)
    cnx.commit()
    
def open_product_selection_window(user_data):
    product_window = tk.Tk()
    product_window.title("Product Selection")
    
    def add_to_cart():
        selected_item = products_listbox.get(tk.ACTIVE)
        cart_listbox.insert(tk.END, selected_item)
        AddToCart(user_data, selected_item, consists_of_data)
    
    products_label = tk.Label(product_window, text="Products:")
    products_label.grid(row=0, column=0, padx=5, pady=5)
    products = getProducts()
    products_listbox = tk.Listbox(product_window, height=10, selectmode=tk.SINGLE)
    for product in products:
        products_listbox.insert(tk.END, product)
    products_listbox.grid(row=1, column=0, padx=5, pady=5)

    add_button = tk.Button(product_window, text="Add to Cart", command=add_to_cart)
    add_button.grid(row=2, column=0, padx=5, pady=5)

    cart_label = tk.Label(product_window, text="Cart:")
    cart_label.grid(row=0, column=1, padx=5, pady=5)

    cart_listbox = tk.Listbox(product_window, height=10, selectmode=tk.SINGLE)
    cart_listbox.grid(row=1, column=1, padx=5, pady=5)

    product_window.mainloop()
def register():
    login_window.destroy()
    register_window = tk.Tk()
    register_window.title("Register")

    name_label = tk.Label(register_window, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(register_window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    email_label = tk.Label(register_window, text="Email ID:")
    email_label.grid(row=1, column=0, padx=5, pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.grid(row=1, column=1, padx=5, pady=5)

    password_label = tk.Label(register_window, text="Password:")
    password_label.grid(row=2, column=0, padx=5, pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    address_label = tk.Label(register_window, text="Address:")
    address_label.grid(row=3, column=0, padx=5, pady=5)
    address_entry = tk.Entry(register_window)
    address_entry.grid(row=3, column=1, padx=5, pady=5)

    phone_label = tk.Label(register_window, text="Phone Number:")
    phone_label.grid(row=4, column=0, padx=5, pady=5)
    phone_entry = tk.Entry(register_window)
    phone_entry.grid(row=4, column=1, padx=5, pady=5)

    def register_user():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        address = address_entry.get()
        phone_number = phone_entry.get()
        insert_query = "INSERT INTO customers (name, email, password, address, phone_number) VALUES (%s, %s, %s, %s, %s)"
        user_data = (name, email, password, address, phone_number)
        cursor.execute(insert_query, user_data)
        cnx.commit()
        customer_id = cursor.lastrowid
        insert_query_wallet = "INSERT INTO WALLET (balance) VALUES (0)"
        cursor.execute(insert_query_wallet)
        cnx.commit()
        wallet_id = cursor.lastrowid
        #for now 13 th product id is set as null product , which will be assigned to a newly registered user.
        insert_query_cart = "INSERT INTO cart (product_id, product_quantity, cost) VALUES (13, 0, 0)"
        cursor.execute(insert_query_cart)
        cnx.commit()
        cart_id = cursor.lastrowid
        update_query = "UPDATE customers SET cart_id = %s, wallet_id = %s WHERE customer_id = %s"
        cursor.execute(update_query, (cart_id, wallet_id, customer_id))
        cnx.commit()

        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()


    register_button = tk.Button(register_window, text="Register", command=register_user)
    register_button.grid(row=5, columnspan=2, padx=5, pady=5)

    def go_back():
        register_window.destroy()

    back_button = tk.Button(register_window, text="Back", command=go_back)
    back_button.grid(row=6, columnspan=2, padx=5, pady=5)

    register_window.mainloop()


def run():
    # Create login window
    global login_window
    login_window = tk.Tk()
    login_window.title("Blinkit")


    # User Login button
    tk.Button(login_window, text="User Login", command=login).grid(row=2, column=0, padx=5, pady=5)
    
    tk.Button(login_window, text="Register", command=register).grid(row=2, column=3, padx=5, pady=5)

    # Admin Login button
    tk.Button(login_window, text="Admin Login", command=admin_login).grid(row=2, column=1, padx=5, pady=5)

    login_window.mainloop()

run()
