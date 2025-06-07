import sys
import sqlite3
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from compiled.main_window.Main import Ui_MainWindow 
from compiled.dialog.About import Ui_aboutDialog

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

        if hasattr(self.ui, "actionAbout"):
            self.ui.actionAbout.triggered.connect(self.show_about)

    def load_database_table(self):
        conn = sqlite3.connect('wifi_stuff.db')
        c = conn.cursor()

        search_text = self.ui.searchInput.text() if hasattr(self.ui, "searchInput") else ""
        if search_text:
            query = """
                SELECT ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated
                FROM onu_info
                WHERE ip LIKE ? OR mac LIKE ? OR ssid_24 LIKE ? OR ssid_5 LIKE ?
            """
            like = f"%{search_text}%"
            c.execute(query, (like, like, like, like))
        else:
            c.execute("""
                SELECT ip, mac, ssid_24, ssid_5, wlan_pwd_24, wlan_pwd_5, source, last_updated
                FROM onu_info
            """)
        rows = c.fetchall()
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
        conn.close()

    def show_about(self):
        about = AboutDialog(self)
        about.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())