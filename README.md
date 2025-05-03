
** I'D = "student"
** Password = "1234"


# 🎓 Python GUI Quiz App

This is a feature-rich quiz application built with Python's Tkinter library. It fetches real-time multiple-choice questions from the Open Trivia Database and supports login, topic and difficulty selection, and a dynamic review system with a smooth fade-in/fade-out GUI experience.

## ✨ Features

- 👤 User login (predefined users)
- 🧠 Topics: Science, History, Maths, Geography, General Knowledge
- 🎚️ Difficulty selection: Easy, Medium, Hard
- 🔄 Dynamic question loading from [Open Trivia DB](https://opentdb.com)
- 🖼️ Circular avatar image on login screen
- ✅ Review screen showing correct/incorrect answers
- 🌗 Smooth fade-in/fade-out transitions

---

## 🚀 How to Run

1. **Clone or download the repo:**
   ```bash
   git clone https://github.com/your-username/quiz-app.git
   cd quiz-app
## Install dependencies:
pip install requests pillow
Update avatar image path in create_login_screen() to your own image file.

## Run the application:
python quiz_app.py

## Convert Python to EXE using PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed quiz_app.py

## [Setup]
AppName=Quiz App
AppVersion=1.0
DefaultDirName={pf}\QuizApp
DefaultGroupName=Quiz App
OutputBaseFilename=QuizAppInstaller

## [Files]
Source: "dist\quiz_app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

## [Icons]
Name: "{group}\Quiz App"; Filename: "{app}\quiz_app.exe"
Name: "{commondesktop}\Quiz App"; Filename: "{app}\quiz_app.exe"; Tasks: desktopicon

## Note
If you use custom icons or images, include them in your Inno Setup build.

The app is designed for single-user demo purposes and not multi-user or secure login handling.

## License
This project is licensed under the MIT License.

## DOWNLODE :- 👉[![Download Quiz.exe](https://img.shields.io/badge/Download-Quiz.exe-blue?style=for-the-badge&logo=github)](https://github.com/Satyam-vohra/Quiz_program/releases/download/Quiz_3/Quiz.exe)




