import mysql.connector
import tkinter as tk
from tkinter import messagebox
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
cursor.execute(query)
users_data = cursor.fetchall()
query_admin = "SELECT * FROM ADMINS"
cursor.execute(query_admin)
adminsdata = cursor.fetchall()
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
    email = email_entry.get()
    password = password_entry.get()
    
    for user_data in users_data:
        if email == user_data[2] and password == user_data[3]:
            login_window.destroy()
            open_product_selection_window(user_data)
            return
    messagebox.showerror("Error", "Invalid email Id or password")
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


def open_product_selection_window(user_data):
    product_window = tk.Tk()
    product_window.title("Product Selection")
    
    def add_to_cart():
        selected_item = products_listbox.get(tk.ACTIVE)
        cart_listbox.insert(tk.END, selected_item)
    
    products_label = tk.Label(product_window, text="Products:")
    products_label.grid(row=0, column=0, padx=5, pady=5)

    products = ["Apples", "Bananas", "Oranges", "Bread", "Milk", "Eggs", "Cheese"]
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
    login_window.title("Login")

    # Email label and entry
    tk.Label(login_window, text="Email:").grid(row=0, column=0, padx=5, pady=5)
    email_entry = tk.Entry(login_window)
    email_entry.grid(row=0, column=1, padx=5, pady=5)

    # Password label and entry
    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # User Login button
    tk.Button(login_window, text="User Login", command=login).grid(row=2, column=0, padx=5, pady=5)
    
    tk.Button(login_window, text="Register", command=register).grid(row=2, column=3, padx=5, pady=5)

    # Admin Login button
    tk.Button(login_window, text="Admin Login", command=admin_login).grid(row=2, column=1, padx=5, pady=5)

    login_window.mainloop()

run()