
from PySide6.QtCore import QObject, Signal, Slot


class AIWorker(QObject):

    # Signals
    result_ready = Signal(str, list, str)
    error_occurred = Signal(str)
    finished = Signal()

    def __init__(
        self,
        user_input,
        history,
        memory_summary,
        chain,
        summarizer_chain
    ):
        super().__init__()

        self.user_input = user_input
        self.history = history
        self.memory_summary = memory_summary
        self.chain = chain
        self.summarizer_chain = summarizer_chain

    @Slot()
    def run(self):

        try:
            # Build conversation context
            context = ""

            if self.memory_summary:
                context += (
                    f"Previous conversation summary:\n"
                    f"{self.memory_summary}\n\n"
                )

            for user_msg, ai_msg in self.history:
                context += (
                    f"User: {user_msg}\n"
                    f"AI: {ai_msg}\n"
                )

            # Generate AI response
            response = self.chain.invoke({
                "context": context,
                "question": self.user_input
            })

            # Update conversation history
            updated_history = self.history + [
                (self.user_input, response)
            ]

            updated_summary = self.memory_summary

            # Check if memory needs condensing
            if len(updated_history) >= 50:

                oldest_messages = updated_history[:10]

                old_messages = ""

                for user_msg, ai_msg in oldest_messages:
                    old_messages += (
                        f"User: {user_msg}\n"
                        f"AI: {ai_msg}\n"
                    )

                try:
                    # Summarize oldest 10 exchanges
                    updated_summary = self.summarizer_chain.invoke({
                        "existing_summary": updated_summary,
                        "old_messages": old_messages
                    })

                    # Remove summarized exchanges
                    updated_history = updated_history[10:]

                    print("Memory condensed!")

                except Exception as e:
                    print(f"Memory summarization failed: {e}")
                    # Keep the original history if summarization fails.

            # Send results back to GUI
            self.result_ready.emit(
                response,
                updated_history,
                updated_summary
            )

        except Exception as e:

            self.error_occurred.emit(str(e))

        finally:

            self.finished.emit()
