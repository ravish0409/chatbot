import json
import tkinter as tk
from difflib import get_close_matches
import time

def load_knowledge_base(file_path: str):

    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data



def save_knowledge_base(file_path: str, data: dict):

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:

    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:

    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recruitment Chatbot")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.message_log = tk.Text(self.frame,bg="#dce5de", height=15, width=40)
        self.message_log.pack(fill=tk.BOTH, expand=True)
        
        self.message_log.tag_configure("You", foreground="blue")
        self.message_log.tag_configure("bot", foreground="green")

        self.user_input = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.ask_button = tk.Button(self.frame, text="Ask",bg="#5bd25b", bd = '3', relief=tk.RAISED,command=self.process_question, font=("Arial", 12))
        self.ask_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.knowledge_base = load_knowledge_base('knowledge_base.json')
        self.pending_response = False

    def process_question(self):
        user_input = self.user_input.get()
        self.user_input.delete(0, tk.END)

        if user_input.lower() == 'quit':
            self.root.quit()
        
        if self.pending_response:
            if user_input.lower() == 'skip':
                self.message_log.insert(tk.END, "You: {}\n\n".format(user_input), "You")
                self.pending_response = False
            else:
                self.knowledge_base["questions"].append({"question": self.unknown_question, "answer": user_input})
                save_knowledge_base('knowledge_base.json', self.knowledge_base)
                self.message_log.insert(tk.END, "You: {}\n\n".format(user_input), "You")
                self.message_log.insert(tk.END, "Bot: I've updated my knowledge with your response.\n\n", "bot")
                self.pending_response = False
        else:
            best_match = find_best_match(user_input, [q["question"] for q in self.knowledge_base["questions"]])

            if best_match:
                answer = get_answer_for_question(best_match, self.knowledge_base)
                self.message_log.insert(tk.END, "You: {}\n\n".format(user_input), "You")
                self.message_log.insert(tk.END, "Bot: {}\n\n".format(answer), "bot")
            else:
                self.unknown_question = user_input
                self.message_log.insert(tk.END, "You: {}\n\n".format(user_input), "You")
                self.message_log.insert(tk.END, "Bot: I don't know the answer. Can you teach me? If not, type 'skip'\n\n", "bot")
                self.pending_response = True
        self.message_log.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()