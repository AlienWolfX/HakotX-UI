import sys
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from PyQt6.QtCore import QUrl
from compiled.main_window.Main import Ui_MainWindow 
from compiled.dialog.About import Ui_aboutDialog
from scripts.sqlite_functions import (
    display_onu_info,
    insert_onu_info,
    update_onu_info,
    search_onu_info
)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_aboutDialog()
        self.ui.setupUi(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_database_table()

        if hasattr(self.ui, "searchButton"):
            self.ui.searchButton.clicked.connect(self.load_database_table)

        if hasattr(self.ui, "searchInput"):
            self.ui.searchInput.textChanged.connect(self.load_database_table)

        if hasattr(self.ui, "actionAbout"):
            self.ui.actionAbout.triggered.connect(self.show_about)

        if hasattr(self.ui, "actionScan"):
            self.ui.actionScan.triggered.connect(self.ip_scanner_tab)

        if hasattr(self.ui, "goButton"):
            self.ui.goButton.clicked.connect(self.go_to_url)
        if hasattr(self.ui, "urlBar"):
            self.ui.urlBar.returnPressed.connect(self.go_to_url)
        if hasattr(self.ui, "refreshButton"):
            self.ui.refreshButton.clicked.connect(self.refresh_page)
        if hasattr(self.ui, "backButton"):
            self.ui.backButton.clicked.connect(self.go_back)
        if hasattr(self.ui, "forwardButton"):
            self.ui.forwardButton.clicked.connect(self.go_forward)
        if hasattr(self.ui, "homeButton"):
            self.ui.homeButton.clicked.connect(self.go_home)
        if hasattr(self.ui, "zoomInButton"):
            self.ui.zoomInButton.clicked.connect(self.zoom_in)
        if hasattr(self.ui, "zoomOutButton"):
            self.ui.zoomOutButton.clicked.connect(self.zoom_out)

    def ip_scanner_tab(self):
        if hasattr(self.ui, "tabWidget"):
            for i in range(self.ui.tabWidget.count()):
                if self.ui.tabWidget.tabText(i).lower() == "ip scanner":
                    self.ui.tabWidget.setCurrentIndex(i)
                    break

    def load_database_table(self):
        search_text = self.ui.searchInput.text() if hasattr(self.ui, "searchInput") else ""
        if search_text:
            rows = search_onu_info(search_text)
        else:
            rows = display_onu_info(return_rows=True)
        if rows:
            self.ui.databaseTable.setRowCount(len(rows))
            self.ui.databaseTable.setColumnCount(8)
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    if col_idx == 7:
                        try:
                            dt = datetime.datetime.fromisoformat(value)
                            value = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except Exception:
                            pass
                    self.ui.databaseTable.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            self.ui.databaseTable.setRowCount(1)
            self.ui.databaseTable.setColumnCount(8)
            for col in range(8):
                self.ui.databaseTable.setItem(0, col, QTableWidgetItem(""))
            self.ui.databaseTable.setItem(0, 0, QTableWidgetItem("Not found"))

    def go_to_url(self):
        url = self.ui.urlBar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.ui.webView.setUrl(QUrl(url))

    def refresh_page(self):
        self.ui.webView.reload()

    def go_back(self):
        self.ui.webView.back()

    def go_forward(self):
        self.ui.webView.forward()

    def go_home(self):
        self.ui.webView.setUrl(QUrl(self.home_url))
        self.ui.urlBar.setText(self.home_url)

    def zoom_in(self):
        current_zoom = self.ui.webView.zoomFactor()
        self.ui.webView.setZoomFactor(current_zoom + 0.1)

    def zoom_out(self):
        current_zoom = self.ui.webView.zoomFactor()
        self.ui.webView.setZoomFactor(max(0.1, current_zoom - 0.1))

    def show_about(self):
        about = AboutDialog(self)
        about.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())