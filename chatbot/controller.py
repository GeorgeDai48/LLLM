
from PySide6.QtCore import QThread, QTimer

from chatbot.memory import ChatMemory
from chatbot.ai import ai_name, chain, summarizer_chain
from chatbot.worker import AIWorker


class ChatController:

    def __init__(self, window):

        # Reference to the GUI
        self.window = window

        # Initialize memory
        self.memory = ChatMemory()

        # Background thread and worker references
        self.active_thread = None
        self.active_worker = None

        # Exit state
        self.closing_after_farewell = False

        # Connect GUI signals
        self.window.message_submitted.connect(self.send)
        self.window.clear_requested.connect(self.clear)
        self.window.exit_requested.connect(self.exit_chat)


    # Start an AI worker in a background thread
    def start_worker(self, user_input, result_handler, history=None, summary=None):

        # Prevent multiple simultaneous workers
        if self.active_thread is not None:
            return

        # Use current memory unless alternative values are supplied
        if history is None:
            history = list(self.memory.history)

        if summary is None:
            summary = self.memory.memory_summary

        # Create background thread
        self.active_thread = QThread()

        # Create worker
        self.active_worker = AIWorker(
            user_input,
            list(history),
            summary,
            chain,
            summarizer_chain
        )

        # Move worker into background thread
        self.active_worker.moveToThread(self.active_thread)

        # Connect signals
        self.active_thread.started.connect(self.active_worker.run)

        self.active_worker.result_ready.connect(result_handler)
        self.active_worker.error_occurred.connect(self.handle_error)

        # Finish worker and thread
        self.active_worker.finished.connect(self.active_thread.quit)
        self.active_worker.finished.connect(self.active_worker.deleteLater)

        # Clean up thread
        self.active_thread.finished.connect(self.active_thread.deleteLater)
        self.active_thread.finished.connect(self.worker_finished)

        # Start background thread
        self.active_thread.start()


    # Handle successful AI response
    def handle_response(self, response, updated_history, updated_summary):

        # Update memory
        self.memory.history = updated_history
        self.memory.memory_summary = updated_summary
        self.memory.message_count += 1

        # Display AI response
        self.window.append_message(ai_name, response, "assistant")


    # Handle farewell response
    def handle_farewell(self, response, _updated_history, _updated_summary):

        self.window.append_message(ai_name, response, "assistant")


    # Handle greeting response
    def handle_greeting(self, response, _updated_history, _updated_summary):

        self.window.append_message(ai_name, response, "assistant")


    # Handle errors
    def handle_error(self, error):

        self.window.append_message(
            ai_name,
            f"Error: {error}",
            "assistant"
        )


    # Handle thread completion
    def worker_finished(self):

        if self.closing_after_farewell:

            # Keep GUI disabled
            self.window.disable_input()

            # Close after 8 seconds
            QTimer.singleShot(8000, self.window.close)

        else:

            # Re-enable GUI
            self.window.set_busy(False)

        # Release references
        self.active_thread = None
        self.active_worker = None


    # Send message
    def send(self, user_input):

        if self.active_thread is not None:
            return

        # Display user message
        self.window.append_message("You", user_input, "user")

        # Show thinking status
        self.window.set_busy(True)

        self.start_worker(
            user_input,
            self.handle_response
        )


    # Clear memory and generate a new greeting
    def clear(self):

        if self.active_thread is not None:
            return

        # Clear memory and chat
        self.memory.clear()
        self.window.clear_chat()

        self.window.append_message(
            ai_name,
            "Memory wipe beam goes pew pew...",
            "assistant"
        )

        # Show thinking status
        self.window.set_busy(True)

        # Generate new greeting
        self.start_worker(
            "User has entered the chat",
            self.handle_greeting,
            history=[],
            summary=""
        )


    # Generate initial greeting
    def start_greeting(self):

        self.window.set_busy(True)

        self.start_worker(
            "User has entered the chat",
            self.handle_greeting,
            history=[],
            summary=""
        )


    # Exit
    def exit_chat(self):

        if self.active_thread is not None:
            return

        self.closing_after_farewell = True

        self.window.set_busy(True)

        self.window.status_label.setText(
            f"{ai_name} is getting ready to return to the oblivion..."
        )

        if self.memory.message_count < 5:
            exit_prompt = "User is leaving the chat after a short chat."
        else:
            exit_prompt = "User is leaving the chat."

        self.start_worker(
            exit_prompt,
            self.handle_farewell
        )
