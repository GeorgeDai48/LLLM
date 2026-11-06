from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from colorama import Fore, Style, init

init() #initialize colorama

ai_model = "qwen3:8b"
template = """
You are a talking frog.
You're familiar with the user.
Never break character

Conversation history: {context}

User: {question}

AI:
"""

model = OllamaLLM(model = ai_model, temperature = 0.9, think = False)

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    while True:
        user_input = input(f"{Fore.MAGENTA}Enter input(e to exit, c to clear): {Style.RESET_ALL}")
        if user_input.lower() == "e":
            print(Fore.CYAN+ai_model + ":  " + Style.RESET_ALL + chain.invoke({"context": "","question": "I'm leaving, see ya."}))
            break
        if user_input.lower() == "c":
            context = ""
            print("Memory wipe beam goes pew pew...")
            continue
        result = chain.invoke({"context": context, "question": user_input})
        print(f"{Fore.CYAN}{ai_model}:  {Style.RESET_ALL}{result}")
        context += f"\nUser: {user_input}\nAI: {result}"
        


handle_conversation()
