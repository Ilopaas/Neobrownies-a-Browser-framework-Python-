from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QProgressBar, QTabBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from .toolbar import Toolbar
from .consolelog import ConsoleLog  # Import the ConsoleLog class

class CustomTabBar(QTabBar):
    def __init__(self):
        super().__init__()
        self.setMovable(True)
        self.setShape(QTabBar.RoundedWest)
        self.setStyleSheet("""
            QTabBar::tab {
                background: #444444;
                color: white;
                height: 50px;
                padding-left: 5px;
                padding-right: 5px;
                text-align: left;
            }
            QTabBar::tab:selected {
                background: #007BFF;
            }
            QTabBar::close-button {
                subcontrol-position: left;
                margin-left: 5px;
            }
        """)

    def tabSizeHint(self, index):
        size_hint = super().tabSizeHint(index)
        size_hint.setHeight(50)
        return size_hint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neobrownies v1")
        self.setGeometry(100, 100, 1200, 800)

        self.layout = QVBoxLayout()
        self.tabs = QTabWidget(self)
        self.tabs.setTabBar(CustomTabBar())
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setMovable(True)
        self.tabs.setTabPosition(QTabWidget.West)

        self.setCentralWidget(self.tabs)
        self.add_new_tab("https://www.google.com")  # Default start page

        self.toolbar = Toolbar(self)
        self.addToolBar(self.toolbar)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximumHeight(5)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #333;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
            }
        """)
        self.layout.addWidget(self.progress_bar)

        self.console_log = ConsoleLog()  # Create an instance of ConsoleLog

    def add_new_tab(self, url="https://www.google.com"):
        for index in range(self.tabs.count()):
            if self.tabs.widget(index).url().toString() == url:
                self.tabs.setCurrentIndex(index)
                return

        new_tab = QWebEngineView()
        new_tab.setUrl(QUrl(url))

        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

        new_tab.loadFinished.connect(lambda: self.update_tab_title(new_tab))
        new_tab.iconChanged.connect(lambda icon: self.update_tab_icon(index, icon))

    def update_tab_title(self, tab):
        index = self.tabs.indexOf(tab)
        if index >= 0:
            self.tabs.setTabText(index, tab.title())

    def update_tab_icon(self, index, icon):
        self.tabs.setTabIcon(index, icon)

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            self.progress_bar.hide()
        else:
            self.progress_bar.show()

    def navigate_to_url(self):
        url = self.toolbar.omnibox.text()  # Get the URL from the omnibox
        if not url.startswith("http"):
            url = "https://" + url
        
        # Check for the console log URL
        if url.lower() == "consolelog.py":
            self.console_log.deiconify()  # Show the console log window
            return

        current_tab = self.tabs.currentWidget()
        current_tab.setUrl(QUrl(url))
        
        # Log the navigation
        self.console_log.log(f"Navigated to: {url}")  # Log the URL to the console log
