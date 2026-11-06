
import sys

from PySide6.QtWidgets import QApplication

from chatbot.gui import ClankerGUI
from chatbot.controller import ChatController
from chatbot.ai import ai_name


# Initialize application
app = QApplication(sys.argv)

# Initialize GUI
window = ClankerGUI(ai_name)

# Initialize controller
controller = ChatController(window)

# Display window
window.show()

# Generate initial greeting asynchronously
controller.start_greeting()

# Run application
sys.exit(app.exec())
