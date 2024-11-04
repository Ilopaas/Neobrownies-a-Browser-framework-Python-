from PyQt5.QtWidgets import QToolBar, QAction, QLineEdit
from PyQt5.QtCore import QUrl

class Toolbar(QToolBar):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Omnibox (URL input)
        self.omnibox = QLineEdit(self)
        self.omnibox.setPlaceholderText("t y p e ?")
        self.omnibox.returnPressed.connect(self.navigate_to_url)
        self.addWidget(self.omnibox)

        # Back button
        self.back_button = QAction("↩", self)
        self.back_button.triggered.connect(self.go_back)
        self.addAction(self.back_button)

        # Forward button
        self.forward_button = QAction("↪", self)
        self.forward_button.triggered.connect(self.go_forward)
        self.addAction(self.forward_button)

        # Reload button
        self.reload_button = QAction("↻", self)
        self.reload_button.triggered.connect(self.reload_page)
        self.addAction(self.reload_button)

        # New Tab button
        self.add_tab_button = QAction("+ New Tab", self)
        self.add_tab_button.triggered.connect(self.add_new_tab)
        self.addAction(self.add_tab_button)

        # Pin Tab button
        self.pin_tab_button = QAction("⚲ Pin Tab", self)
        self.pin_tab_button.triggered.connect(self.pin_current_tab)
        self.addAction(self.pin_tab_button)

        # Customize the style
        self.setStyleSheet("""
            QToolBar {
                background-color: rgb(50, 50, 50);
                color: white;
            }
            QToolButton {
                color: white;
            }
            QToolButton:hover {
                background-color: rgb(80, 80, 80);
            }
        """)

    def navigate_to_url(self):
        url = self.omnibox.text()
        # Check if the URL starts with http/https, if not prepend https://
        if not url.startswith("http"):
            url = "https://" + url
        current_tab = self.main_window.tabs.currentWidget()
        current_tab.setUrl(QUrl(url))

    def go_back(self):
        current_tab = self.main_window.tabs.currentWidget()
        current_tab.back()

    def go_forward(self):
        current_tab = self.main_window.tabs.currentWidget()
        current_tab.forward()

    def reload_page(self):
        current_tab = self.main_window.tabs.currentWidget()
        current_tab.reload()

    def add_new_tab(self):
        self.main_window.add_new_tab()

    def pin_current_tab(self):
        current_index = self.main_window.tabs.currentIndex()
        if current_index != -1:
            self.main_window.pin_tab(current_index)


