from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from theme import load_theme

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        self.title = QLabel("\U0001F4CA Dashboard")
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Cards Grid Layout (2 rows)
        card_layout = QGridLayout()
        card_layout.setSpacing(15)

        self.total_balance = self.create_card("\U0001F4B0 Total Balance", "\u20B90", "#b3e5fc")   # Light Blue
        self.total_expense = self.create_card("\U0001F4B8 Total Expenses", "\u20B90", "#c8e6c9")  # Light Green
        self.total_employees = self.create_card("\U0001F464 Total Employees", "0", "#fff9c4")    # Light Yellow
        self.total_machines = self.create_card("\U0001F9F5 Total Machines", "0", "#e1bee7")      # Light Purple
        self.total_udhar = self.create_card("\U0001F4B3 Total Udhar", "\u20B90", "#ffe0b2")       # Light Orange

        cards = [
            self.total_balance,
            self.total_expense,
            self.total_employees,
            self.total_machines,
            self.total_udhar
        ]

        # Add cards to grid layout (2 per row)
        for i, card in enumerate(cards):
            row = i // 2
            col = i % 2
            card_layout.addWidget(card, row, col)

        layout.addLayout(card_layout)

        # Notifications Section
        self.notification_label = QLabel("\U0001F514 Recent Notifications")
        self.notification_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.notification_label)

        self.notification_box = QLabel("No new notifications")
        self.notification_box.setFrameShape(QFrame.Box)
        self.notification_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.notification_box.setWordWrap(True)
        layout.addWidget(self.notification_box)

        self.setLayout(layout)
        self.update_theme()

    def create_card(self, title, value, bg_color):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setProperty("bg_color", bg_color)
        card_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 16, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card.setLayout(card_layout)

        return card

    def update_data(self, balance, expenses, employees, machines, udhar, notifications):
        self.total_balance.findChildren(QLabel)[1].setText(f"\u20B9{balance}")
        self.total_expense.findChildren(QLabel)[1].setText(f"\u20B9{expenses}")
        self.total_employees.findChildren(QLabel)[1].setText(f"{employees}")
        self.total_machines.findChildren(QLabel)[1].setText(f"{machines}")
        self.total_udhar.findChildren(QLabel)[1].setText(f"\u20B9{udhar}")
        self.notification_box.setText(notifications)

    def update_theme(self):
        theme = load_theme()
        if theme == "dark":
            self.setStyleSheet("background-color: #1e1e2f; color: white;")
            box_style = "background-color: #2a2a40; border: 1px solid #444; padding: 8px;"
        else:
            self.setStyleSheet("background-color: #f0f4f7; color: black;")
            box_style = "background-color: #ffffff; border: 1px solid #ccc; padding: 8px;"

        card_colors = (
            ["#b3e5fc", "#c8e6c9", "#fff9c4", "#e1bee7", "#ffe0b2"]
            if theme == "light"
            else ["#394b59", "#3d5a4d", "#6f6743", "#5a4b5c", "#5e4c3c"]
        )

        for idx, card in enumerate([
            self.total_balance,
            self.total_expense,
            self.total_employees,
            self.total_machines,
            self.total_udhar,
        ]):
            card.setStyleSheet(
                f"background-color: {card_colors[idx]}; color: {'white' if theme == 'dark' else 'black'}; padding: 10px; border-radius: 10px;"
            )

        self.notification_box.setStyleSheet(box_style)
        self.title.setStyleSheet("margin-top: 10px;")
        self.notification_label.setStyleSheet("margin-top: 20px;")