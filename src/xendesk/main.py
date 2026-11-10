from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
import sys

from ui.main_window import MainWindow

app = QApplication(sys.argv)
app.setFont(QFont("Arial", 10))
window = MainWindow()
window.show()

app.exec()