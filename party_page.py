import sqlite3
import uuid
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PartyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("પાર્ટી વિગતો")  # "Party Details" in Gujarati
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("નામ અથવા સંપર્ક દ્વારા શોધો")  # "Search by Name or Contact" in Gujarati
        self.search_input.textChanged.connect(self.search_clients)
        search_button = QPushButton("🔍 શોધો")  # "Search" in Gujarati
        search_button.clicked.connect(self.search_clients)
        search_layout.addStretch()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Main content: Form on left, Table on right
        main_layout = QHBoxLayout()

        # Left: Form for adding/updating client
        left_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.address_input = QLineEdit()
        form_layout.addRow("નામ:", self.name_input)  # "Name" in Gujarati
        form_layout.addRow("સંપર્ક:", self.contact_input)  # "Contact" in Gujarati
        form_layout.addRow("સરનામું:", self.address_input)  # "Address" in Gujarati
        left_layout.addLayout(form_layout)

        # Action buttons below form
        action_layout = QHBoxLayout()
        add_button = QPushButton("ક્લાયન્ટ ઉમેરો")  # "Add Client" in Gujarati
        add_button.clicked.connect(self.add_client)
        update_button = QPushButton("ક્લાયન્ટ અપડેટ કરો")  # "Update Client" in Gujarati
        update_button.clicked.connect(self.update_client)
        action_layout.addWidget(add_button)
        action_layout.addWidget(update_button)
        left_layout.addLayout(action_layout)
        main_layout.addLayout(left_layout, 1)

        # Right: Table for displaying clients
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["નામ", "સંપર્ક", "સરનામું"])  # "Name", "Contact", "Address" in Gujarati
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.fill_form)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table, 2)

        layout.addLayout(main_layout)
        self.setLayout(layout)
        self.load_clients()

    def load_clients(self):
        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            c.execute("SELECT name, contact, address FROM clients")
            clients = c.fetchall()
            conn.close()
            self.table.setRowCount(len(clients))
            for row_idx, client in enumerate(clients):
                for col_idx, data in enumerate(client):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data or '')))
            self.table.resizeColumnsToContents()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")

    def search_clients(self):
        search_text = self.search_input.text().lower()
        conn = sqlite3.connect('embroidery.db')
        c = conn.cursor()
        c.execute("SELECT name, contact, address FROM clients WHERE name LIKE ? OR contact LIKE ?",
                  (f'%{search_text}%', f'%{search_text}%'))
        clients = c.fetchall()
        conn.close()
        self.table.setRowCount(len(clients))
        for row_idx, client in enumerate(clients):
            for col_idx, data in enumerate(client):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data or '')))
        self.table.resizeColumnsToContents()

    def add_client(self):
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        address = self.address_input.text().strip()

        if not (name and contact and address):
            QMessageBox.warning(self, "Error", "નામ, સંપર્ક, અને સરનામું આવશ્યક છે")  # "Name, Contact, and Address are required" in Gujarati
            return

        # Validate contact (e.g., phone number)
        if not re.match(r'^\+?\d{10,15}$', contact):
            QMessageBox.warning(self, "Error", "અમાન્ય સંપર્ક નંબર")  # "Invalid contact number" in Gujarati
            return

        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            c.execute("SELECT contact FROM clients WHERE contact = ?", (contact,))
            if c.fetchone():
                QMessageBox.warning(self, "Error", "સંપર્ક નંબર પહેલેથી અસ્તિત્વમાં છે")  # "Contact number already exists" in Gujarati
                conn.close()
                return

            c.execute("INSERT INTO clients (id, name, contact, address) VALUES (?, ?, ?, ?)",
                      (str(uuid.uuid4()), name, contact, address))
            conn.commit()
            conn.close()
            self.load_clients()
            self.clear_inputs()
            QMessageBox.information(self, "Success", "ક્લાયન્ટ ઉમેરાયું")  # "Client added" in Gujarati
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to add client: {str(e)}")

    def update_client(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "અપડેટ કરવા માટે ક્લાયન્ટ પસંદ કરો")  # "Select a client to update" in Gujarati
            return

        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        address = self.address_input.text().strip()

        if not (name and contact and address):
            QMessageBox.warning(self, "Error", "નામ, સંપર્ક, અને સરનામું આવશ્યક છે")  # "Name, Contact, and Address are required" in Gujarati
            return

        if not re.match(r'^\+?\d{10,15}$', contact):
            QMessageBox.warning(self, "Error", "અમાન્ય સંપર્ક નંબર")  # "Invalid contact number" in Gujarati
            return

        try:
            conn = sqlite3.connect('embroidery.db')
            c = conn.cursor()
            # Since we're not displaying ID in the table, we need to fetch it based on the current row
            c.execute("SELECT id FROM clients WHERE name = ? AND contact = ? AND address = ?",
                      (self.table.item(selected, 0).text(), self.table.item(selected, 1).text(), self.table.item(selected, 2).text()))
            client_id = c.fetchone()[0]
            
            c.execute("SELECT contact FROM clients WHERE contact = ? AND id != ?", (contact, client_id))
            if c.fetchone():
                QMessageBox.warning(self, "Error", "સંપર્ક નંબર પહેલેથી અસ્તિત્વમાં છે")  # "Contact number already exists" in Gujarati
                conn.close()
                return

            c.execute("UPDATE clients SET name = ?, contact = ?, address = ? WHERE id = ?",
                      (name, contact, address, client_id))
            conn.commit()
            conn.close()
            self.load_clients()
            self.clear_inputs()
            QMessageBox.information(self, "Success", "ક્લાયન્ટ અપડેટ થયું")  # "Client updated" in Gujarati
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to update client: {str(e)}")

    def fill_form(self):
        selected = self.table.currentRow()
        if selected < 0:
            return
        self.name_input.setText(self.table.item(selected, 0).text())
        self.contact_input.setText(self.table.item(selected, 1).text())
        self.address_input.setText(self.table.item(selected, 2).text())

    def clear_inputs(self):
        self.name_input.clear()
        self.contact_input.clear()
        self.address_input.clear()

    def update_theme(self):
        theme = load_theme()  # Assumes load_theme from main.py
        if theme == "dark":
            self.setStyleSheet("""
                background-color: #121212; color: white;
                QTableWidget { background-color: #1e1e1e; color: white; }
                QLineEdit { background-color: #2e2e2e; color: white; }
                QPushButton { background-color: #37474f; color: white; }
            """)
        else:
            self.setStyleSheet("""
                background-color: #f5f5f5; color: black;
                QTableWidget { background-color: #ffffff; color: black; }
                QLineEdit { background-color: #ffffff; color: black; }
                QPushButton { background-color: #b3e5fc; color: black; }
            """)