import tkinter as tk
from tkinter import ttk
import mysql.connector

class ViewOrdersApp:
    def __init__(self, master):
        self.master = master
        self.master.title("View Orders")
        self.master.geometry("800x600")

        # Connect to MySQL
        self.connection = mysql.connector.connect(
            host='localhost',
            user='python_app',
            password='python_app',
            database='python_app'
        )
        self.cursor = self.connection.cursor()

        # Set the style to 'clam' for a more modern look
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Create a treeview for displaying orders with vertical scrollbar
        self.orders_treeview = ttk.Treeview(master, style="Treeview")
        self.orders_treeview["columns"] = ("ID", "Item", "Price","Order Number", "Paid", "Order Time")
        self.orders_treeview.column("#0", width=0, stretch=tk.NO)  # Dummy column
        self.orders_treeview.column("ID", anchor=tk.W, width=50)
        self.orders_treeview.column("Item", anchor=tk.W, width=200)
        self.orders_treeview.column("Price", anchor=tk.W, width=100)
        self.orders_treeview.column("Order Number", anchor=tk.W, width=100)
        self.orders_treeview.column("Paid", anchor=tk.W, width=100)
        self.orders_treeview.column("Order Time", anchor=tk.W, width=200)

        self.orders_treeview.heading("#0", text="", anchor=tk.W)
        self.orders_treeview.heading("ID", text="ID", anchor=tk.W)
        self.orders_treeview.heading("Item", text="Item", anchor=tk.W)
        self.orders_treeview.heading("Price", text="Price", anchor=tk.W)
        self.orders_treeview.heading("Order Number", text="Order Number", anchor=tk.W)
        self.orders_treeview.heading("Paid", text="Paid", anchor=tk.W)
        self.orders_treeview.heading("Order Time", text="Order Time", anchor=tk.W)

        # Add a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.orders_treeview.yview)
        self.orders_treeview.configure(yscrollcommand=self.scrollbar.set)

        self.orders_treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load orders from the database
        self.load_orders()

    def load_orders(self):
        # Retrieve orders from the database
        self.cursor.execute("SELECT id, item, price, order_number, is_paid, order_time FROM orders")
        orders = self.cursor.fetchall()

        # Populate the treeview with orders
        for order in orders:
            self.orders_treeview.insert("", tk.END, values=order)

    def on_closing(self):
        # Close the database connection before closing the window
        self.connection.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ViewOrdersApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Close the database connection before closing the window
    root.mainloop()
