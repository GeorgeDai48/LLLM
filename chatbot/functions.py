
# Build conversation context
def build_context(memory_summary, history):

    context = ""

    if memory_summary:
        context += (
            f"Previous conversation summary:\n"
            f"{memory_summary}\n\n"
        )

    for user_msg, ai_msg in history:
        context += (
            f"User: {user_msg}\n"
            f"AI: {ai_msg}\n"
        )

    return context


# Condense conversation memory
def condense_memory(summarizer_chain, memory):

    if len(memory.history) >= 50:

        # Get the 10 oldest exchanges
        oldest_messages = memory.history[:10]

        old_messages = ""

        for user_msg, ai_msg in oldest_messages:
            old_messages += (
                f"User: {user_msg}\n"
                f"AI: {ai_msg}\n"
            )

        # Generate updated summary
        updated_summary = summarizer_chain.invoke({
            "existing_summary": memory.memory_summary,
            "old_messages": old_messages
        })

        # Update memory
        memory.memory_summary = updated_summary
        memory.history = memory.history[10:]

        print("Memory condensed.")
