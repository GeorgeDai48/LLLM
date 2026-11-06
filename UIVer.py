from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageSequence


#ai setup
ai_name = "Clanker"
ai_model = "qwen3:8b"
with open("chatbot/ai_template.txt", "r", encoding="utf-8") as f:
    personality = f.read()
    
template = personality + """

Conversation history: {context}

User: {question}

AI:
"""

model = OllamaLLM(model = ai_model, temperature = 0.9, think = False)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
message_count = 0
context = ""

#Functions
def greeting():
    entry_prompt = "User has entered the chat"
    response = chain.invoke({"context":"", "question": entry_prompt})
    chat_log.insert(tk.END, f"{ai_name}: {response}\n\n","responder")

def send():
    global context, message_count
    message_count += 1
    user_input = entry.get()
    response = chain.invoke({"context": context, "question": user_input})
    chat_log.insert(tk.END, f"You: {user_input}","entry")
    chat_log.insert(tk.END, f"\n{ai_name}: {response}\n\n","responder")
    context += f"\nUser: {user_input}\nAI: {response}"
    entry.delete(0, tk.END)
    
def clear():
    global context, message_count
    chat_log.insert(tk.END, "Memory wipe beam goes pew pew...\n\n","entry")
    context = ""

def exit():
    global context, message_count
    if (message_count < 5):
        exit_prompt = "User is leaving the chat after a short chat."
    else:
        exit_prompt = "User is leaving the chat."
    farewell = chain.invoke({"context": context, "question": exit_prompt})
    
    chat_log.insert(tk.END, f"{ai_name}: {farewell}\n","responder")
    root.after(8000, root.destroy)  

#Tkinter setup
#Size
root = tk.Tk()
root.title(f"{ai_name}")
root.geometry("1000x950")
root.state("zoomed")

#Colour Def 
BG_COLOR = "#383838"        # window background
CHAT_BG = "#292929"          # chat log background
CHAT_FG = "#FFFFFF"          # chat log text color
ENTRY_BG = "#2E2E2E"         # entry background
ENTRY_FG = "#FFFFFF"         # entry text color
BUTTON_BG = "#3A3A3A"        # button background
BUTTON_FG = "#FFFFFF"        # button text color

#image
image = Image.open("chatbot/frog-spin.gif")
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(image)]

label = tk.Label(root)
label.pack()

frame_index = 0

def update():
    global frame_index
    label.config(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    root.after(50, update)


#Output box
chatFont = tkFont.Font(family="Arial Unicode MS", weight="bold", size=16)
chat_log = tk.Text(root, height=20, width=50, wrap="word", padx=10, pady=10, bg=CHAT_BG, fg=CHAT_FG, font=chatFont, insertbackground=CHAT_FG)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_log.tag_config("responder", foreground="cyan")
chat_log.tag_config("entry", foreground="magenta")

#Entry box
entry = tk.Entry(root, width=80, font=chatFont)
entry.pack(padx=10, pady=(0, 10))
entry.bind("<Return>", lambda event: send())

#Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=(0, 10))

send_button = tk.Button(button_frame, text="Send", command=send, font=chatFont)
send_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear Memory", command=clear, font=chatFont)
clear_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=exit, font=chatFont)
exit_button.pack(side=tk.LEFT, padx=10)

#main
greeting()
update()
root.mainloop()