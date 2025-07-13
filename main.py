from PySide6.QtWidgets import QApplication
import sys

from ui import PisoPisoApp
from app_state import AppState

state = AppState()                 

app = QApplication(sys.argv)      
window = PisoPisoApp(state)     
window.show()
sys.exit(app.exec())  