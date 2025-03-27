import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QComboBox,QMainWindow
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QFont
from party_details import PartyDetailsPage
from material_details import MaterialDetailsPage
from employee_details import EmployeeDetailsPage
from expense_details import ExpenseDetailsPage

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
        self.stacked_widget.setCurrentIndex(1)  # Switch to Main UI

    def update_theme(self):
        theme = load_theme()
        if theme == "dark":
            self.setStyleSheet("background-color: #121212; color: white;")
            self.enter_button.setStyleSheet("background-color: #6200ea; color: white; padding: 10px; border-radius: 10px;")
        else:
            self.setStyleSheet("background-color: white; color: black;")
            self.enter_button.setStyleSheet("background-color: #0084ff; color: white; padding: 10px; border-radius: 10px;")

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

        self.header.addWidget(self.logo)
        self.header.addStretch()
        self.header.addWidget(self.language_selector)
        self.header.addWidget(self.theme_button)

        # Side Menu
        self.side_menu = QVBoxLayout()
        button_names = ["Home", "Party Details", "Material Details", "Employee Details", "Expense Details"]
        for name in button_names:
            btn = QPushButton(name)
            btn.setFont(QFont("Arial", 12))
            self.side_menu.addWidget(btn)
        self.side_menu.addStretch()
        
        # Dashboard
        self.dashboard = QVBoxLayout()
        self.title = QLabel("📌 Yogi Fashion - Embroidery Management System")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))

        self.stats_layout = QHBoxLayout()
        self.balance_label = QLabel("💰 Total Balance: ₹0")
        self.expense_label = QLabel("💳 Total Expense: ₹0")
        self.employee_label = QLabel("👨‍💼 Total Employees: 0")
        
        for lbl in [self.balance_label, self.expense_label, self.employee_label]:
            lbl.setFont(QFont("Arial", 14))
            self.stats_layout.addWidget(lbl)

        # Date & Time
        self.date_time_label = QLabel()
        self.date_time_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.update_time()
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        
        self.dashboard.addWidget(self.title, alignment=Qt.AlignCenter)
        self.dashboard.addLayout(self.stats_layout)
        self.dashboard.addStretch()
        self.dashboard.addWidget(self.date_time_label, alignment=Qt.AlignRight)

        # Main Layout
        self.main_layout = QHBoxLayout()
        self.side_menu_frame = QFrame()
        self.side_menu_frame.setLayout(self.side_menu)

        self.content_frame = QFrame()
        self.content_frame.setLayout(self.dashboard)

        self.main_layout.addWidget(self.side_menu_frame, 1)
        self.main_layout.addWidget(self.content_frame, 4)

        self.layout.addLayout(self.header)
        self.layout.addLayout(self.main_layout)
        self.setLayout(self.layout)

        self.update_theme()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss")
        self.date_time_label.setText(f"🕒 {current_time}")

    def toggle_theme(self):
        current_theme = load_theme()
        new_theme = "light" if current_theme == "dark" else "dark"
        save_theme(new_theme)
        self.update_theme()
        self.parent().widget(0).update_theme()  # Update Welcome Page Theme

    def update_theme(self):
        theme = load_theme()
        if theme == "dark":
            self.setStyleSheet("background-color: #121212; color: white;")
            self.logo.setStyleSheet("color: #ff9800;")
            self.theme_button.setText("🌞 Light Mode")
            self.theme_button.setStyleSheet("background-color: #333; color: white;")
            self.language_selector.setStyleSheet("background-color: #333; color: white; padding: 5px;")
            self.side_menu_frame.setStyleSheet("background-color: #222; padding: 10px;")
            self.content_frame.setStyleSheet("background-color: #121212;")  # Fixed Background Dark
            self.date_time_label.setStyleSheet("background-color: black; color: #00ff00; padding: 8px;")
            for lbl in [self.balance_label, self.expense_label, self.employee_label]:
                lbl.setStyleSheet("background-color: #333; padding: 10px; border-radius: 10px;")
        else:
            self.setStyleSheet("background-color: white; color: black;")
            self.logo.setStyleSheet("color: #6200ea;")
            self.theme_button.setText("🌙 Dark Mode")
            self.theme_button.setStyleSheet("background-color: #ddd; color: black;")
            self.language_selector.setStyleSheet("background-color: #eee; color: black; padding: 5px;")
            self.side_menu_frame.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
            self.content_frame.setStyleSheet("background-color: white;")  # Fixed Light Background
            self.date_time_label.setStyleSheet("background-color: lightgray; color: black; padding: 8px;")
            for lbl in [self.balance_label, self.expense_label, self.employee_label]:
                lbl.setStyleSheet("background-color: #ddd; padding: 10px; border-radius: 10px;")

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Embroidery Business Management")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        self.pages = {
            "Home": HomePage(),
            "Party Details": PartyDetailsPage(),
            "Material Details": MaterialDetailsPage(),
            "Employee Details": EmployeeDetailsPage(),
            "Expense Details": ExpenseDetailsPage()
        }
        
        for page in self.pages.values():
            self.stack.addWidget(page)
        
        self.create_menu()
        self.show_home()

        def create_menu(self):
        self.menu_layout = QVBoxLayout()
        self.layout.addLayout(self.menu_layout)

        for name in self.pages.keys():
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, n=name: self.show_page(n))
            self.menu_layout.addWidget(btn)
    
    def show_page(self, page_name):
        self.stack.setCurrentWidget(self.pages[page_name])
    
    def show_home(self):
        self.show_page("Home")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    welcome_page = WelcomePage(stacked_widget)
    main_page = MainPage(stacked_widget)

    stacked_widget.addWidget(welcome_page)
    stacked_widget.addWidget(main_page)

    stacked_widget.setCurrentIndex(0)  # Start with Welcome Page
    stacked_widget.showMaximized()

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()

    sys.exit(app.exec_())
