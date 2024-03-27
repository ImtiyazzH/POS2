import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector
import random
from datetime import datetime

# Replace with your database credentials
db_config = {
    'host': 'localhost',
    'user': 'python_app',
    'password': 'python_app',
    'database': 'python_app'
}

class PointOfSaleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Point of Sale")
        self.master.geometry("600x400")

        # Fonts
        title_font = ("Helvetica", 20, "bold")
        label_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        # Colors
        bg_color = "#f2f2f2"
        button_bg_color = "#4CAF50"
        button_fg_color = "white"

        # Menu data (you can load this from a file or database in a real application)
        self.menu_items = {
            "Drinks": {
                "Cola": 1.99,
                "Orange Juice": 2.49,
                "Iced Tea": 1.79,
                "Coffee": 2.99,
                "Milkshake": 3.49
            },
            "Chinese": {
                "Fried Rice": 7.99,
                "Kung Pao Chicken": 8.49,
                "Spring Rolls": 5.99,
                "Sweet and Sour Pork": 9.99,
                "Beef Chow Mein": 10.99
            },
            "Chickster": {
                "Chicken Burger": 5.99,
                "Chicken Wings": 6.49,
                "Chicken Tenders": 4.99,
                "Grilled Chicken Salad": 7.99,
                "Spicy Chicken Sandwich": 6.99
            }
        }


        self.order = {}  # To store the current order

        # Create GUI elements
        self.menu_label = tk.Label(master, text="Menu:", font=title_font, bg=bg_color)
        self.menu_label.pack()

        self.menu_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, font=label_font)
        for item in self.menu_items:
            self.menu_listbox.insert(tk.END, f"{item} - ${self.menu_items[item]:.2f}")
        self.menu_listbox.pack()

        self.add_to_order_button = tk.Button(master, text="Add to Order", command=self.add_to_order, font=button_font, bg=button_bg_color, fg=button_fg_color)
        self.add_to_order_button.pack(pady=5)

        self.order_label = tk.Label(master, text="Order:", font=title_font, bg=bg_color)
        self.order_label.pack()

        self.order_listbox = tk.Listbox(master, font=label_font)
        self.order_listbox.pack()

        self.total_label = tk.Label(master, text="Total: $0.00", font=label_font, bg=bg_color)
        self.total_label.pack()

        self.checkout_button = tk.Button(master, text="Checkout", command=self.checkout, font=button_font, bg=button_bg_color, fg=button_fg_color)
        self.checkout_button.pack(pady=5)

        # Add "Pay Now" button for automatic payment
        self.pay_now_button = tk.Button(master, text="Pay Now", command=self.pay_now, font=button_font, bg=button_bg_color, fg=button_fg_color)
        self.pay_now_button.pack(pady=5)

        # Payment method dropdown
        self.payment_method_label = tk.Label(master, text="Payment Method:", font=label_font, bg=bg_color)
        self.payment_method_label.pack()

        self.payment_methods = ["Credit Card", "Debit Card", "Cash"]
        self.selected_payment_method = tk.StringVar()
        self.payment_method_dropdown = ttk.Combobox(master, textvariable=self.selected_payment_method, values=self.payment_methods, font=label_font)
        self.payment_method_dropdown.pack()

    def add_to_order(self):
        selected_items = self.menu_listbox.curselection()
        for index in selected_items:
            menu_item = self.menu_listbox.get(index)
            item_name = menu_item.split(" - ")[0]
            item_price = self.menu_items[item_name]
            self.order[item_name] = item_price
            self.order_listbox.insert(tk.END, f"{item_name} - ${item_price:.2f}")
        self.update_total()

    def update_total(self):
        total = sum(self.order.values())
        self.total_label.config(text=f"Total: ${total:.2f}")

    def checkout(self):
        total = sum(self.order.values())
        if total > 0:
            checkout_message = f"Thank you for your order! Total: ${total:.2f}"

            # Provide a recommendation
            recommended_item = self.get_recommendation()

            if recommended_item:
                recommendation_response = tk.messagebox.askquestion("Recommendation", f"We recommend trying {recommended_item}. Would you like to add it to your order?")
                if recommendation_response == 'yes':
                    self.order[recommended_item] = self.menu_items[recommended_item]
                    self.order_listbox.insert(tk.END, f"{recommended_item} - ${self.menu_items[recommended_item]:.2f}")
                    self.update_total()  # Update the total after adding the recommended item
                    checkout_message += f"\nRecommended item '{recommended_item}' added to your order. Updated Total: ${sum(self.order.values()):.2f}"

            tk.messagebox.showinfo("Checkout", checkout_message)

            # Automatically trigger payment upon checkout
            self.pay_now()
        else:
            tk.messagebox.showinfo("Checkout", "Your order is empty. Please add items to your order first.")

    def pay_now(self):
        # Simulate payment process (replace this with actual payment integration)
        selected_payment_method = self.selected_payment_method.get()
        if selected_payment_method:
            payment_successful = tk.messagebox.askyesno("Payment", f"Pay ${sum(self.order.values()):.2f} using {selected_payment_method}. Do you want to proceed?")
            if payment_successful:
                tk.messagebox.showinfo("Payment Success", "Payment successful!")
                self.mark_order_as_paid()
            else:
                tk.messagebox.showwarning("Payment Failed", "Payment failed. Please try again.")
        else:
            tk.messagebox.showwarning("Payment Failed", "Payment method not selected. Please try again.")

    def mark_order_as_paid(self):
        # Update the database to mark the order as paid
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert order data into the database
        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order_values = [(item, price, self.get_last_order_number() + 1, True, order_time) for item, price in self.order.items()]
        cursor.executemany("INSERT INTO orders (item, price, order_number, is_paid, order_time) VALUES (%s, %s, %s, %s, %s)", order_values)

        connection.commit()
        cursor.close()
        connection.close()

    def get_recommendation(self):
        # In a real-world scenario, you might use more sophisticated recommendation logic.
        # For simplicity, we'll randomly select an item from the menu as a recommendation.
        menu_items = list(self.menu_items.keys())
        random.shuffle(menu_items)
        for item in menu_items:
            if item not in self.order:
                return item
        return None

    def get_last_order_number(self):
        # Retrieve the last order number from the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(order_number) FROM orders")
        last_order_number =  cursor.fetchone()[0] or 0  # If no orders exist, start from 0

        cursor.close()
        connection.close()

        return last_order_number

if __name__ == "__main__":
    root = tk.Tk()
    app = PointOfSaleApp(root)
    root.mainloop()
