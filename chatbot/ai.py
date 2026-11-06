
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# AI setup
ai_name = "Clanker"
ai_model = "qwen3:8b"

with open("chatbot/ai_template.txt", "r", encoding="utf-8") as f:
    personality = f.read()

template = personality + """

Conversation history:
{context}

User: {question}

AI:
"""

model = OllamaLLM(
    model=ai_model,
    temperature=0.9,
    think=False
)

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


# Memory summarization setup
summarizer_template = """
You are summarizing an older portion of a chatbot conversation.

Previous conversation summary:
{existing_summary}

New conversation messages to incorporate:
{old_messages}

Create an updated, condensed summary of the conversation.

Preserve:
- Important facts about the user
- User preferences and personality
- Important names, dates, events and details
- Ongoing projects and discussions
- Important context that may be useful in future conversations
- Key takeaways from previous interactions
- Previously established location and date information when relevant
- Distinguish historical information from current information

Remove:
- Repetitive information
- Unimportant small talk
- Unnecessary wording

Keep the summary concise while retaining important information.
Never invent missing information.

Updated Summary:
"""

summarizer_prompt = ChatPromptTemplate.from_template(summarizer_template)
summarizer_chain = summarizer_prompt | model
