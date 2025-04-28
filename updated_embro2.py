import sys
import json
import sqlite3
import bcrypt
import uuid
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QFrame, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QFormLayout
)
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QFont
from home import HomePage

# Save & Load Theme
THEME_FILE = "theme.json"

def load_theme():
    try:
        with open(THEME_FILE, "r") as file:
            return json.load(file).get("theme", "dark")
    except FileNotFoundError:
        return "dark"

def save_theme(theme):
    with open(THEME_FILE, "w") as file:
        json.dump({"theme": theme}, file)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('embroidery.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id TEXT PRIMARY KEY, name TEXT, contact TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (id TEXT PRIMARY KEY, name TEXT, contact TEXT, address TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (design_id TEXT PRIMARY KEY, description TEXT, embroidery_type TEXT, price REAL, stock INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id TEXT PRIMARY KEY, description TEXT, amount REAL, date TEXT)''')
    conn.commit()
    conn.close()

class RegisterPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch()

        title = QLabel("🧵 Yogi Fashion Register")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        layout.addLayout(form_layout)

        register_button = QPushButton("📝 Register")
        register_button.setFont(QFont("Arial", 14))
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        login_button = QPushButton("🔐 Go to Login")
        login_button.setFont(QFont("Arial", 14))
        login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)
        self.update_theme()

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            c.execute("SELECT username FROM users WHERE username = ?", (username,))
            if c.fetchone():
                QMessageBox.warning(self, "Error", "Username already exists")
                conn.close()
                return

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            c.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
                      (str(uuid.uuid4()), username, hashed))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Registration successful! Please login.")
            self.stacked_widget.setCurrentIndex(1)  # Go to Login Page
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to register: {str(e)}")

    def update_theme(self):
        theme = load_theme()
        if theme == "dark":
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364);
                color: white;
            """)
        else:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 #e0f7fa, stop:1 #ffffff);
                color: black;
            """)

class LoginPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch()

        title = QLabel("🧵 Yogi Fashion Login")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        layout.addLayout(form_layout)

        login_button = QPushButton("🔐 Login")
        login_button.setFont(QFont("Arial", 14))
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        register_button = QPushButton("📝 Go to Register")
        register_button.setFont(QFont("Arial", 14))
        register_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)
        self.update_theme()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        conn = sqlite3.connect('embroidery.db')
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()
        conn.close()
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1]):
            self.stacked_widget.setCurrentIndex(2)  # Go to Welcome Page
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def update_theme(self):
        theme = load_theme()
        if theme == "dark":
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364);
                color: white;
            """)
        else:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 #e0f7fa, stop:1 #ffffff);
                color: black;
            """)

class WelcomePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.welcome_label = QLabel("✨ Welcome to Yogi Fashion ✨")
        self.welcome_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)

        self.enter_button = QPushButton("🚀 Enter")
        self.enter_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.enter_button.clicked.connect(self.go_to_main)

        self.layout.addStretch()
        self.layout.addWidget(self.welcome_label)
        self.layout.addWidget(self.enter_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.update_theme()

    def go_to_main(self):
        self.stacked_widget.setCurrentIndex(3)  # Go to Main Page

    def update_theme(self):
        theme = load_theme()
        if theme == "dark":
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364);
                color: white;
            """)
            self.enter_button.setStyleSheet("""
                background-color: #00c9a7; color: #fff;
                padding: 12px; border-radius: 10px;
            """)
        else:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 #e0f7fa, stop:1 #ffffff);
                color: black;
            """)
            self.enter_button.setStyleSheet("""
                background-color: #0288d1; color: white;
                padding: 12px; border-radius: 10px;
            """)

class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Form for adding employee
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.role_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Contact:", self.contact_input)
        form_layout.addRow("Role:", self.role_input)
        add_button = QPushButton("Add Employee")
        add_button.clicked.connect(self.add_employee)
        form_layout.addWidget(add_button)
        layout.addLayout(form_layout)

        # Table for displaying employees
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Role"])
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Buttons for update/delete
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update Selected")
        update_button.clicked.connect(self.update_employee)
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_employee)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_employees()

    def load_employees(self):
        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            c.execute("SELECT id, name, contact, role FROM employees")
            employees = c.fetchall()
            conn.close()
            self.table.setRowCount(len(employees))
            for row_idx, employee in enumerate(employees):
                for col_idx, data in enumerate(employee):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def add_employee(self):
        name = self.name_input.text()
        contact = self.contact_input.text()
        role = self.role_input.text()
        if name and contact and role:
            try:
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("INSERT INTO employees (id, name, contact, role) VALUES (?, ?, ?, ?)",
                          (str(uuid.uuid4()), name, contact, role))
                conn.commit()
                conn.close()
                self.load_employees()
                self.name_input.clear()
                self.contact_input.clear()
                self.role_input.clear()
                QMessageBox.information(self, "Success", "Employee added")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add employee: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "All fields are required")

    def update_employee(self):
        selected = self.table.currentRow()
        if selected >= 0:
            id = self.table.item(selected, 0).text()
            name = self.name_input.text()
            contact = self.contact_input.text()
            role = self.role_input.text()
            if name and contact and role:
                try:
                    conn = sqlite3.connect('embroidery.db')
                    c = conn.cursor()
                    c.execute("UPDATE employees SET name = ?, contact = ?, role = ? WHERE id = ?",
                              (name, contact, role, id))
                    conn.commit()
                    conn.close()
                    self.load_employees()
                    QMessageBox.information(self, "Success", "Employee updated")
                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Error", f"Failed to update employee: {str(e)}")
            else:
                QMessageBox.warning(self, "Error", "All fields are required")
        else:
            QMessageBox.warning(self, "Error", "Select an employee to update")

    def delete_employee(self):
        selected = self.table.currentRow()
        if selected >= 0:
            id = self.table.item(selected, 0).text()
            try:
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("DELETE FROM employees WHERE id = ?", (id,))
                conn.commit()
                conn.close()
                self.load_employees()
                QMessageBox.information(self, "Success", "Employee deleted")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to delete employee: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Select an employee to delete")

class PartyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Form for adding client
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.address_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Contact:", self.contact_input)
        form_layout.addRow("Address:", self.address_input)
        add_button = QPushButton("Add Client")
        add_button.clicked.connect(self.add_client)
        form_layout.addWidget(add_button)
        layout.addLayout(form_layout)

        # Table for displaying clients
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Address"])
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Buttons for update/delete
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update Selected")
        update_button.clicked.connect(self.update_client)
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_client)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_clients()

    def load_clients(self):
        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            c.execute("SELECT id, name, contact, address FROM clients")
            clients = c.fetchall()
            conn.close()
            self.table.setRowCount(len(clients))
            for row_idx, client in enumerate(clients):
                for col_idx, data in enumerate(client):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def add_client(self):
        name = self.name_input.text()
        contact = self.contact_input.text()
        address = self.address_input.text()
        if name and contact and address:
            try:
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("INSERT INTO clients (id, name, contact, address) VALUES (?, ?, ?, ?)",
                          (str(uuid.uuid4()), name, contact, address))
                conn.commit()
                conn.close()
                self.load_clients()
                self.name_input.clear()
                self.contact_input.clear()
                self.address_input.clear()
                QMessageBox.information(self, "Success", "Client added")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add client: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "All fields are required")

    def update_client(self):
        selected = self.table.currentRow()
        if selected >= 0:
            id = self.table.item(selected, 0).text()
            name = self.name_input.text()
            contact = self.contact_input.text()
            address = self.address_input.text()
            if name and contact and address:
                try:
                    conn = sqlite3.connect('embroidery.db')
                    c = conn.cursor()
                    c.execute("UPDATE clients SET name = ?, contact = ?, address = ? WHERE id = ?",
                              (name, contact, address, id))
                    conn.commit()
                    conn.close()
                    self.load_clients()
                    QMessageBox.information(self, "Success", "Client updated")
                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Error", f"Failed to update client: {str(e)}")
            else:
                QMessageBox.warning(self, "Error", "All fields are required")
        else:
            QMessageBox.warning(self, "Error", "Select a client to update")

    def delete_client(self):
        selected = self.table.currentRow()
        if selected >= 0:
            id = self.table.item(selected, 0).text()
            try:
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("DELETE FROM clients WHERE id = ?", (id,))
                conn.commit()
                conn.close()
                self.load_clients()
                QMessageBox.information(self, "Success", "Client deleted")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to delete client: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Select a client to delete")

class MaterialPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Form for adding product
        form_layout = QFormLayout()
        self.desc_input = QLineEdit()
        self.type_input = QLineEdit()
        self.price_input = QLineEdit()
        self.stock_input = QLineEdit()
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("Embroidery Type:", self.type_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Stock:", self.stock_input)
        add_button = QPushButton("Add Product")
        add_button.clicked.connect(self.add_product)
        form_layout.addWidget(add_button)
        layout.addLayout(form_layout)

        # Table for displaying products
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Design ID", "Description", "Type", "Price", "Stock"])
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Buttons for update/delete
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update Selected")
        update_button.clicked.connect(self.update_product)
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_product)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_products()

    def load_products(self):
        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            c.execute("SELECT design_id, description, embroidery_type, price, stock FROM products")
            products = c.fetchall()
            conn.close()
            self.table.setRowCount(len(products))
            for row_idx, product in enumerate(products):
                for col_idx, data in enumerate(product):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def add_product(self):
        description = self.desc_input.text()
        embroidery_type = self.type_input.text()
        price = self.price_input.text()
        stock = self.stock_input.text()
        if description and embroidery_type and price and stock:
            try:
                price = float(price)
                stock = int(stock)
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("INSERT INTO products (design_id, description, embroidery_type, price, stock) VALUES (?, ?, ?, ?, ?)",
                          (str(uuid.uuid4()), description, embroidery_type, price, stock))
                conn.commit()
                conn.close()
                self.load_products()
                self.desc_input.clear()
                self.type_input.clear()
                self.price_input.clear()
                self.stock_input.clear()
                QMessageBox.information(self, "Success", "Product added")
            except ValueError:
                QMessageBox.warning(self, "Error", "Price and Stock must be numbers")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add product: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "All fields are required")

    def update_product(self):
        selected = self.table.currentRow()
        if selected >= 0:
            design_id = self.table.item(selected, 0).text()
            description = self.desc_input.text()
            embroidery_type = self.type_input.text()
            price = self.price_input.text()
            stock = self.stock_input.text()
            if description and embroidery_type and price and stock:
                try:
                    price = float(price)
                    stock = int(stock)
                    conn = sqlite3.connect('embroidery.db')
                    c = conn.cursor()
                    c.execute("UPDATE products SET description = ?, embroidery_type = ?, price = ?, stock = ? WHERE design_id = ?",
                              (description, embroidery_type, price, stock, design_id))
                    conn.commit()
                    conn.close()
                    self.load_products()
                    QMessageBox.information(self, "Success", "Product updated")
                except ValueError:
                    QMessageBox.warning(self, "Error", "Price and Stock must be numbers")
                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Error", f"Failed to update product: {str(e)}")
            else:
                QMessageBox.warning(self, "Error", "All fields are required")
        else:
            QMessageBox.warning(self, "Error", "Select a product to update")

    def delete_product(self):
        selected = self.table.currentRow()
        if selected >= 0:
            design_id = self.table.item(selected, 0).text()
            try:
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("DELETE FROM products WHERE design_id = ?", (design_id,))
                conn.commit()
                conn.close()
                self.load_products()
                QMessageBox.information(self, "Success", "Product deleted")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to delete product: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Select a product to delete")

class ExpensePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Form for adding expense
        form_layout = QFormLayout()
        self.desc_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Date:", self.date_input)
        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)
        form_layout.addWidget(add_button)
        layout.addLayout(form_layout)

        # Table for displaying expenses
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Description", "Amount", "Date"])
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Buttons for update/delete
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update Selected")
        update_button.clicked.connect(self.update_expense)
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_expense)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_expenses()

    def load_expenses(self):
        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            c.execute("SELECT id, description, amount, date FROM expenses")
            expenses = c.fetchall()
            conn.close()
            self.table.setRowCount(len(expenses))
            for row_idx, expense in enumerate(expenses):
                for col_idx, data in enumerate(expense):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def add_expense(self):
        description = self.desc_input.text()
        amount = self.amount_input.text()
        date = self.date_input.text()
        if description and amount and date:
            try:
                amount = float(amount)
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("INSERT INTO expenses (id, description, amount, date) VALUES (?, ?, ?, ?)",
                          (str(uuid.uuid4()), description, amount, date))
                conn.commit()
                conn.close()
                self.load_expenses()
                self.desc_input.clear()
                self.amount_input.clear()
                self.date_input.clear()
                QMessageBox.information(self, "Success", "Expense added")
            except ValueError:
                QMessageBox.warning(self, "Error", "Amount must be a number")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to add expense: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "All fields are required")

    def update_expense(self):
        selected = self.table.currentRow()
        if selected >= 0:
            id = self.table.item(selected, 0).text()
            description = self.desc_input.text()
            amount = self.amount_input.text()
            date = self.date_input.text()
            if description and amount and date:
                try:
                    amount = float(amount)
                    conn = sqlite3.connect('embroidery.db')
                    c = conn.cursor()
                    c.execute("UPDATE expenses SET description = ?, amount = ?, date = ? WHERE id = ?",
                              (description, amount, date, id))
                    conn.commit()
                    conn.close()
                    self.load_expenses()
                    QMessageBox.information(self, "Success", "Expense updated")
                except ValueError:
                    QMessageBox.warning(self, "Error", "Amount must be a number")
                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Error", f"Failed to update expense: {str(e)}")
            else:
                QMessageBox.warning(self, "Error", "All fields are required")
        else:
            QMessageBox.warning(self, "Error", "Select an expense to update")

    def delete_expense(self):
        selected = self.table.currentRow()
        if selected >= 0:
            id = self.table.item(selected, 0).text()
            try:
                conn = sqlite3.connect('embroidery.db')
                c = conn.cursor()
                c.execute("DELETE FROM expenses WHERE id = ?", (id,))
                conn.commit()
                conn.close()
                self.load_expenses()
                QMessageBox.information(self, "Success", "Expense deleted")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Failed to delete expense: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Select an expense to delete")

class MainPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Header
        self.header = QHBoxLayout()
        self.logo = QLabel("🧵 Yogi Fashion")
        self.logo.setFont(QFont("Arial", 18, QFont.Bold))

        self.language_selector = QComboBox()
        self.language_selector.addItems(["English", "Hindi", "Gujarati"])

        self.theme_button = QPushButton("🌞 Light Mode")
        self.theme_button.setFont(QFont("Arial", 10))
        self.theme_button.clicked.connect(self.toggle_theme)

        self.date_time_label = QLabel()
        self.date_time_label.setFont(QFont("Arial", 10))
        self.update_datetime()
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)

        self.header.addWidget(self.logo)
        self.header.addStretch()
        self.header.addWidget(self.date_time_label)
        self.header.addWidget(self.language_selector)
        self.header.addWidget(self.theme_button)

        # Side Menu
        self.side_menu = QVBoxLayout()
        button_names = ["Home", "Party Details", "Material Details", "Employee Details", "Expense Details"]
        self.buttons = {}
        for name in button_names:
            btn = QPushButton(name)
            btn.setFont(QFont("Arial", 12))
            btn.clicked.connect(lambda checked, page=name: self.open_page(page))
            self.buttons[name] = btn
            self.side_menu.addWidget(btn)
        self.side_menu.addStretch()

        # Main Layout
        self.main_layout = QHBoxLayout()
        self.side_menu_frame = QFrame()
        self.side_menu_frame.setLayout(self.side_menu)

        self.content_frame = QFrame()
        self.content_layout = QVBoxLayout()

        # Back button
        self.back_button = QPushButton("🔙 Back")
        self.back_button.setFont(QFont("Arial", 10))
        self.back_button.clicked.connect(self.show_dashboard)
        self.back_button.setVisible(False)

        self.dashboard = QLabel("📌 Select an option from the menu")
        self.dashboard.setFont(QFont("Arial", 16, QFont.Bold))
        self.dashboard.setAlignment(Qt.AlignCenter)

        self.content_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.content_layout.addWidget(self.dashboard)
        self.content_frame.setLayout(self.content_layout)

        # Pages dictionary
        self.pages = {
            "Home": HomePage(),
            "Employee Details": EmployeePage(),
            "Party Details": PartyPage(),
            "Material Details": MaterialPage(),
            "Expense Details": ExpensePage()
        }

        self.main_layout.addWidget(self.side_menu_frame, 1)
        self.main_layout.addWidget(self.content_frame, 4)

        self.layout.addLayout(self.header)
        self.layout.addLayout(self.main_layout)
        self.setLayout(self.layout)

        self.update_theme()

    def update_datetime(self):
        current = QDateTime.currentDateTime().toString("dddd, dd MMM yyyy hh:mm:ss")
        self.date_time_label.setText(current)

    def open_page(self, page):
        if page in self.pages:
            for i in reversed(range(self.content_layout.count())):
                widget = self.content_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)
            self.content_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
            self.content_layout.addWidget(self.pages[page])
            self.back_button.setVisible(True)
        else:
            self.show_dashboard()
            self.dashboard.setText(f"📄 {page} Page Opened")

    def show_dashboard(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.content_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.content_layout.addWidget(self.dashboard)
        self.back_button.setVisible(False)

    def toggle_theme(self):
        current_theme = load_theme()
        new_theme = "light" if current_theme == "dark" else "dark"
        save_theme(new_theme)
        self.update_theme()
        self.stacked_widget.widget(2).update_theme()  # Update Welcome Page
        for page in self.pages.values():
            if hasattr(page, 'update_theme'):
                page.update_theme()

    def update_theme(self):
        theme = load_theme()
        if theme == "dark":
            self.setStyleSheet("""
                background-color: #121212; color: white;
            """)
            self.theme_button.setText("🌞 Light Mode")
            for btn in self.buttons.values():
                btn.setStyleSheet("""
                    background-color: #37474f; color: white; padding: 6px; border-radius: 8px;
                """)
            self.back_button.setStyleSheet("""
                background-color: #455a64; color: white; padding: 5px; border-radius: 5px;
            """)
        else:
            self.setStyleSheet("""
                background-color: #f5f5f5; color: black;
            """)
            self.theme_button.setText("🌙 Dark Mode")
            for btn in self.buttons.values():
                btn.setStyleSheet("""
                    background-color: #b3e5fc; color: black; padding: 6px; border-radius: 8px;
                """)
            self.back_button.setStyleSheet("""
                background-color: #81d4fa; color: black; padding: 5px; border-radius: 5px;
            """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_db()  # Initialize database
    stacked_widget = QStackedWidget()

    register_page = RegisterPage(stacked_widget)
    login_page = LoginPage(stacked_widget)
    welcome_page = WelcomePage(stacked_widget)
    main_page = MainPage(stacked_widget)

    stacked_widget.addWidget(register_page)
    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(welcome_page)
    stacked_widget.addWidget(main_page)

    stacked_widget.setCurrentIndex(0)
    stacked_widget.showMaximized()

    sys.exit(app.exec_())