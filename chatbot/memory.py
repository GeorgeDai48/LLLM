class ChatMemory:

    def __init__(self):
        self.history = []
        self.memory_summary = ""
        self.message_count = 0

    def build_context(self):

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

        return context

    def add_exchange(self, user_msg, ai_msg):

        self.history.append((user_msg, ai_msg))
        self.message_count += 1

    def clear(self):

        self.history.clear()
        self.memory_summary = ""
        self.message_count = 0
