import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="dbms_project"
)
cursor = cnx.cursor()
query = "SELECT * FROM CUSTOMERS"
cursor.execute(query)
import tkinter as tk
from tkinter import messagebox

users_data = cursor.fetchall()
last_entry = users_data[-1]
def login():
    email = email_entry.get()
    password = password_entry.get()
    
    # Check if email and password match with any user's credentials
    for user_data in users_data:
        if email == user_data[2] and password == user_data[3]:
            # Destroy login window
            login_window.destroy()
            # Open product selection window
            open_product_selection_window(user_data)
            return
    # If no match found, show error message
    messagebox.showerror("Error", "Invalid email Id or password")

def open_product_selection_window(user_data):
    # Create new window for product selection
    product_window = tk.Tk()
    product_window.title("Product Selection")
    
    def add_to_cart():
        selected_item = products_listbox.get(tk.ACTIVE)
        cart_listbox.insert(tk.END, selected_item)
    
    # Products listbox
    products_label = tk.Label(product_window, text="Products:")
    products_label.grid(row=0, column=0, padx=5, pady=5)

    products = ["Apples", "Bananas", "Oranges", "Bread", "Milk", "Eggs", "Cheese"]
    products_listbox = tk.Listbox(product_window, height=10, selectmode=tk.SINGLE)
    for product in products:
        products_listbox.insert(tk.END, product)
    products_listbox.grid(row=1, column=0, padx=5, pady=5)

    # Add to Cart button
    add_button = tk.Button(product_window, text="Add to Cart", command=add_to_cart)
    add_button.grid(row=2, column=0, padx=5, pady=5)

    # Cart listbox
    cart_label = tk.Label(product_window, text="Cart:")
    cart_label.grid(row=0, column=1, padx=5, pady=5)

    cart_listbox = tk.Listbox(product_window, height=10, selectmode=tk.SINGLE)
    cart_listbox.grid(row=1, column=1, padx=5, pady=5)

    product_window.mainloop()
def register():
    # Create a registration window
    register_window = tk.Tk()
    register_window.title("Register")

    # Registration fields
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

    # Register button'
    def register_user():

        # Retrieve data from the entry fields
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        address = address_entry.get()
        phone_number = phone_entry.get()

        # Insert user data into the CUSTOMERS table
        insert_query = "INSERT INTO customers (customer_id,name, email, password, address, phone_number,cart_id, wallet_id) VALUES (%s, %s, %s, %s, %s)"
        user_data = (last_entry[0]+1,name, email, password, address, phone_number,last_entry[6]+1,last_entry[7]+1)
        cursor.execute(insert_query, user_data)
        cnx.commit()

        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()

    register_button = tk.Button(register_window, text="Register", command=register_user)
    register_button.grid(row=5, columnspan=2, padx=5, pady=5)

    # Back button
    def go_back():
        register_window.destroy()

    back_button = tk.Button(register_window, text="Back", command=go_back)
    back_button.grid(row=6, columnspan=2, padx=5, pady=5)

    register_window.mainloop()
def run():
# Create login window
    login_window = tk.Tk()
    login_window.title("Login")

    # email label and entry
    tk.Label(login_window, text="Email ID:").grid(row=0, column=0, padx=5, pady=5)
    email_entry = tk.Entry(login_window)
    email_entry.grid(row=0, column=1, padx=5, pady=5)

    # Password label and entry
    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Login button
    tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, padx=5, pady=5)

    # Register button
    tk.Button(login_window, text="Register", command=register).grid(row=3, columnspan=2, padx=5, pady=5)

    login_window.mainloop()
run()