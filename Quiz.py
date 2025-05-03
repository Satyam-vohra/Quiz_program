import requests
import html
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import io
import base64

# Predefined users
USERS = {
    "student": {"password": "1234", "role": "student"}
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("600x400")
        self.user_role = None
        self.topic = None
        self.questions = []
        self.score = 0
        self.current_question = 0
        self.user_answers = []
        self.selected_difficulty = tk.StringVar(value="medium")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.category_icons = self.load_icons()

        self.create_login_screen()

    def load_icons(self):
        icon_data = {
            "Science": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAALCAYAAACp9...",
            "History": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAALCAYAAACp9...",
            "Maths": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAALCAYAAACp9...",
            "Geography": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAALCAYAAACp9...",
            "General Knowledge": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAALCAYAAACp9..."
        }
        icons = {}
        for key, b64 in icon_data.items():
            try:
                image = Image.open(io.BytesIO(base64.b64decode(b64)))
                icons[key] = ImageTk.PhotoImage(image.resize((30, 30)))
            except:
                icons[key] = None
        return icons

    def fade_transition(self, func):
        def fade():
            alpha = self.root.attributes('-alpha')
            if alpha > 0:
                alpha -= 0.1
                self.root.attributes('-alpha', alpha)
                self.root.after(30, fade)
            else:
                func()
                self.fade_in()
        fade()

    def fade_in(self):
        def fade():
            alpha = self.root.attributes('-alpha')
            if alpha < 1:
                alpha += 0.1
                self.root.attributes('-alpha', alpha)
                self.root.after(30, fade)
        fade()

    def create_login_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Load and display circular login image
        try:
            image_path = "C:\\Users\\shiva\\OneDrive\\Pictures\\student.jpg"  # Replace with your image path
            login_img = Image.open(image_path).resize((150, 150)).convert("RGBA")

            # Create circular mask
            mask = Image.new("L", (150, 150), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 150, 150), fill=255)

            # Apply mask to image
            circular_img = Image.new("RGBA", (150, 150))
            circular_img.paste(login_img, (0, 0), mask)

            self.login_photo = ImageTk.PhotoImage(circular_img)
            tk.Label(self.main_frame, image=self.login_photo).pack(pady=10)
        except Exception as e:
            print("Error loading login image:", e)

        tk.Label(self.main_frame, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack()

        tk.Label(self.main_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack()

        self.login_error = tk.Label(self.main_frame, text="", fg="red")
        self.login_error.pack()

        tk.Button(self.main_frame, text="Login", command=self.handle_login).pack(pady=10)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        user = USERS.get(username)
        if user and user["password"] == password:
            self.user_role = user["role"]
            self.fade_transition(self.create_topic_selection)
        else:
            self.login_error.config(text="Invalid username or password")

    def create_topic_selection(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text=f"Welcome, {self.user_role}!", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.main_frame, text="Select a Difficulty", font=("Arial", 14)).pack(pady=10)
        diff_frame = tk.Frame(self.main_frame)
        diff_frame.pack(pady=5)

        for level in ["easy", "medium", "hard"]:
            ttk.Radiobutton(diff_frame, text=level.capitalize(), variable=self.selected_difficulty,
                            value=level).pack(side="left", padx=5)

        tk.Label(self.main_frame, text="Select a Topic", font=("Arial", 16)).pack(pady=20)
        topics = {
            "Science": 17,
            "History": 23,
            "Maths": 19,
            "Geography": 22,
            "General Knowledge": 9
        }

        for topic, category_id in topics.items():
            frame = tk.Frame(self.main_frame)
            frame.pack(pady=5)
            if self.category_icons.get(topic):
                tk.Label(frame, image=self.category_icons[topic]).pack(side="left", padx=5)
            api_url = f"https://opentdb.com/api.php?amount=10&category={category_id}&difficulty={self.selected_difficulty.get()}&type=multiple"
            tk.Button(frame, text=topic, font=("Arial", 12), command=lambda url=api_url: self.fade_transition(lambda: self.start_quiz(url))).pack(side="left")

    def start_quiz(self, api_url):
        self.questions = self.get_questions(api_url)
        if not self.questions:
            tk.Label(self.main_frame, text="Failed to fetch questions.", fg="red").pack()
            return
        self.current_question = 0
        self.score = 0
        self.user_answers = [None] * len(self.questions)
        self.show_question()

    def get_questions(self, api_url):
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            return []

    def show_question(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if self.current_question >= len(self.questions):
            self.show_review_screen()
            return

        question = self.questions[self.current_question]
        tk.Label(self.main_frame, text=f"Q{self.current_question + 1}: {html.unescape(question['question'])}", font=("Arial", 12), wraplength=500).pack(pady=10)

        choices = question["incorrect_answers"] + [question["correct_answer"]]
        random.shuffle(choices)

        self.selected_answer = tk.StringVar()
        if self.user_answers[self.current_question]:
            self.selected_answer.set(self.user_answers[self.current_question])

        for choice in choices:
            ttk.Radiobutton(self.main_frame, text=html.unescape(choice), variable=self.selected_answer, value=choice).pack(anchor="w")

        nav_frame = tk.Frame(self.main_frame)
        nav_frame.pack(pady=10)

        if self.current_question > 0:
            tk.Button(nav_frame, text="Previous", command=lambda: self.fade_transition(self.prev_question)).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Next", command=lambda: self.fade_transition(self.next_question)).pack(side="left", padx=5)

    def next_question(self):
        self.user_answers[self.current_question] = self.selected_answer.get()
        self.current_question += 1
        self.show_question()

    def prev_question(self):
        self.user_answers[self.current_question] = self.selected_answer.get()
        self.current_question -= 1
        self.show_question()

    def show_review_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Review Your Answers", font=("Arial", 16)).pack(pady=10)

        review_canvas = tk.Canvas(self.main_frame)
        review_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=review_canvas.yview)
        review_frame = tk.Frame(review_canvas)

        review_frame.bind(
            "<Configure>", lambda e: review_canvas.configure(scrollregion=review_canvas.bbox("all"))
        )

        review_canvas.create_window((0, 0), window=review_frame, anchor="nw")
        review_canvas.configure(yscrollcommand=review_scrollbar.set)

        for i, question in enumerate(self.questions):
            q_text = html.unescape(question['question'])
            correct = question['correct_answer']
            answer = self.user_answers[i] or "Not answered"
            correct_text = "✅ Correct" if answer == correct else f"❌ Incorrect (Correct: {html.unescape(correct)})"
            tk.Label(review_frame, text=f"Q{i+1}: {q_text}\nYour answer: {html.unescape(answer)}\n{correct_text}", wraplength=550, justify="left").pack(pady=5, anchor="w")

        review_canvas.pack(side="left", fill="both", expand=True)
        review_scrollbar.pack(side="right", fill="y")

        tk.Button(self.main_frame, text="Submit Quiz", command=lambda: self.fade_transition(self.submit_quiz)).pack(pady=10)

    def submit_quiz(self):
        self.calculate_score()
        self.show_result()

    def calculate_score(self):
        self.score = 0
        for i, answer in enumerate(self.user_answers):
            if answer == self.questions[i]["correct_answer"]:
                self.score += 1

    def show_result(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text=f"Quiz Completed!", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.main_frame, text=f"Your Score: {self.score} / {len(self.questions)}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.main_frame, text="Play Again", command=lambda: self.fade_transition(self.create_topic_selection)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-alpha', 1.0)
    app = QuizApp(root)
    root.mainloop()
