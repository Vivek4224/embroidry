import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QComboBox
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
        self.stacked_widget.setCurrentIndex(1)

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
            "Home": HomePage()
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
        self.stacked_widget.widget(0).update_theme()

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
    stacked_widget = QStackedWidget()

    welcome_page = WelcomePage(stacked_widget)
    main_page = MainPage(stacked_widget)

    stacked_widget.addWidget(welcome_page)
    stacked_widget.addWidget(main_page)

    stacked_widget.setCurrentIndex(0)
    stacked_widget.showMaximized()

    sys.exit(app.exec_())
