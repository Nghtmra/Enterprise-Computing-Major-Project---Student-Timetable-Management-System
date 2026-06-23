#📘 Student Timetable Management System
A modern, easy‑to‑use timetable manager built with Python, Tkinter, and ttkbootstrap.

#📌 Overview
The Student Timetable Management System is a desktop application that allows students to:
- Add new classes
- View their timetable
- Delete individual or all classes
- Print their timetable
- Switch between light/dark mode

Navigate between multiple pages (Timetable, Add Class, Settings)
All data is saved locally in a JSON file, so your timetable is preserved between sessions.

#🚀 Features
✔ Modern UI using ttkbootstrap

✔ Multi‑page navigation (Timetable / Add Class / Settings)

✔ JSON‑based data storage

✔ Add, delete, and print classes

✔ Light/Dark theme toggle

✔ Alternating row colours for readability

✔ No internet required

🛠 Requirements
Before running the program, you must have:

1. Python 3.10 – 3.12
Download from:
https://www.python.org/downloads/

⚠️ Python 3.14 is NOT supported by ttkbootstrap.

2. ttkbootstrap
Install using pip:

Code
pip install ttkbootstrap
Built‑in modules (already included with Python)
You do not need to install these:

tkinter

json

os

tempfile

📥 Installation
Follow these steps:

1. Download the project
Download or clone the project folder containing:

timetable.py

timetable.json (auto‑created if missing)

2. Install dependencies
Open a terminal (Command Prompt, PowerShell, or macOS/Linux terminal):

Code
pip install ttkbootstrap
3. Run the program
Navigate to the folder containing timetable.py:

Code
cd path/to/project
Run the program:

Code
python timetable.py
The application window will open.

📂 Project Structure
Code
📁 Timetable-System
│
├── timetable.py        # Main application
├── timetable.json      # Saved timetable data
└── README.md           # Documentation
🧠 How It Works
Data Storage
All timetable entries are stored in:

Code
timetable.json
Example structure:

json
{
  "classes": [
    {
      "subject": "Math",
      "day": "Monday",
      "start": "09:00",
      "end": "10:00",
      "teacher": "Mr Smith",
      "room": "A1"
    }
  ]
}
Pages
Timetable Page → Displays all saved classes

Add Class Page → Form to add/delete/print classes

Settings Page → Theme toggle

🖨 Printing
The program uses Windows’ built‑in printing system:

Code
os.startfile(file_path, "print")
This means printing works only on Windows.

❗ Troubleshooting
“ModuleNotFoundError: No module named 'ttkbootstrap'”
Install it:

Code
pip install ttkbootstrap
The program opens but UI looks plain/white
You are using Python 3.14.
Install Python 3.12 instead.

Printing does nothing
Printing only works on Windows.
macOS/Linux users must manually open the generated .txt file.

📜 License
This project is free for educational use.

🙌 Author
Created by Giant for the Enterprise Computing Major Project.
