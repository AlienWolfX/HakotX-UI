import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
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
        
        if hasattr(self.ui, "actionAbout"):
            self.ui.actionAbout.triggered.connect(self.show_about)

    def show_about(self):
        about = AboutDialog(self)
        about.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())