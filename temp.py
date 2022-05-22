import sys
import PySide6.QtWidgets as qt
from PySide6.QtCore import Slot



@Slot()
def on_button_click():
    print("ncjgf")

window = qt.QApplication(sys.argv)
label = qt.QLabel("<font color=green size=100> Hello <font>")
label.show()

button = qt.QPushButton("CLICK ME")
button.clicked.connect(on_button_click)
button.show()

window.exec()

