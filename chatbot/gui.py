
import html

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMovie, QFont


class ClankerGUI(QMainWindow):

    # Signals for communicating with the main program
    message_submitted = Signal(str)
    clear_requested = Signal()
    exit_requested = Signal()

    def __init__(self, ai_name="Clanker"):
        super().__init__()

        self.ai_name = ai_name

        # Window setup
        self.setWindowTitle(ai_name)
        self.setGeometry(100, 100, 1000, 950)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Font
        chat_font = QFont("Arial", 16)
        chat_font.setBold(True)

        # Animated GIF
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.movie = QMovie("chatbot/frog-spin.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        main_layout.addWidget(self.gif_label)

        # Chat log
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setFont(chat_font)

        main_layout.addWidget(self.chat_log, stretch=1)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.status_label)

        # Input box
        self.entry = QLineEdit()
        self.entry.setFont(chat_font)
        self.entry.setPlaceholderText("Type your message...")

        main_layout.addWidget(self.entry)

        # Buttons
        button_layout = QHBoxLayout()

        self.send_button = QPushButton("Send")
        self.clear_button = QPushButton("Clear Memory")
        self.exit_button = QPushButton("Exit")

        for button in (
            self.send_button,
            self.clear_button,
            self.exit_button
        ):
            button.setFont(chat_font)
            button_layout.addWidget(button)

        main_layout.addLayout(button_layout)

        # Connections
        self.send_button.clicked.connect(self.send_message)
        self.entry.returnPressed.connect(self.send_message)

        self.clear_button.clicked.connect(
            self.clear_requested.emit
        )

        self.exit_button.clicked.connect(
            self.exit_requested.emit
        )

        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #383838;
            }

            QWidget {
                background-color: #383838;
                color: white;
            }

            QTextEdit {
                background-color: #292929;
                color: white;
                border: none;
                padding: 10px;
            }

            QLineEdit {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #555555;
                padding: 10px;
            }

            QPushButton {
                background-color: #3A3A3A;
                color: white;
                padding: 10px 20px;
                border: 1px solid #555555;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #505050;
            }

            QPushButton:pressed {
                background-color: #222222;
            }
        """)

    # Send message
    def send_message(self):
        user_input = self.entry.text().strip()

        if not user_input:
            return

        self.entry.clear()
        self.message_submitted.emit(user_input)

    # Display a message
    def append_message(self, sender, message, role="assistant"):

        colors = {
            "user": "magenta",
            "assistant": "cyan"
        }

        color = colors.get(role, "white")

        safe_sender = html.escape(str(sender))
        safe_message = html.escape(str(message)).replace("\n", "<br>")

        self.chat_log.append(
            f'<span style="color:{color};">'
            f'<b>{safe_sender}:</b> {safe_message}'
            f'</span><br>'
        )

        # Automatically scroll to bottom
        scrollbar = self.chat_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # Clear displayed conversation
    def clear_chat(self):
        self.chat_log.clear()

    # Disable input during exit
    def disable_input(self):
        self.entry.setEnabled(False)
        self.send_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.exit_button.setEnabled(False)

    # Enable/disable input during AI generation
    def set_busy(self, busy):

        self.entry.setEnabled(not busy)
        self.send_button.setEnabled(not busy)
        self.clear_button.setEnabled(not busy)
        self.exit_button.setEnabled(not busy)

        if busy:
            self.status_label.setText("All those GBs of RAM are getting put to use...")
        else:
            self.status_label.setText("")
