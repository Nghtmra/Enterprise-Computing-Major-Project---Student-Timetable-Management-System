import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import json
import os
import tempfile

DATA_FILE = "timetable.json"

# ---------- Data functions ----------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"classes": []}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"classes": []}
"""
    Load timetable data from the JSON file.
    - If the file does not exist, return an empty timetable structure.
    - If the file exists but contains invalid JSON (corrupted or empty),
      return a safe empty structure instead of crashing the program.
    Returns:
        dict: A dictionary containing a list of class entries.
"""

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
"""
    Save the current timetable data to the JSON file.
    - Opens the file in write mode.
    - Dumps the 'data' dictionary into the file in a readable format.
    - Ensures persistence of timetable information between program sessions.
"""

# ---------- UI logic ----------

def add_class():
    subject = subject_entry.get().strip()
    day = day_var.get().strip()
    start = start_entry.get().strip()
    end = end_entry.get().strip()
    teacher = teacher_entry.get().strip()
    room = room_entry.get().strip()

    if not subject or not day or not start or not end:
        messagebox.showerror("Error", "Please fill in Subject, Day, Start and End time.")
        return

    new_class = {
        "subject": subject,
        "day": day,
        "start": start,
        "end": end,
        "teacher": teacher,
        "room": room
    }

    data["classes"].append(new_class)
    save_data()
    refresh_table()
    clear_form()

def delete_class():
    selected = table.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a class to delete.")
        return

    item = table.item(selected)
    values = item["values"]

    for c in data["classes"]:
        if (c["day"] == values[0] and
            c["start"] == values[1] and
            c["end"] == values[2] and
            c["subject"] == values[3] and
            c["teacher"] == values[4] and
            c["room"] == values[5]):
            data["classes"].remove(c)
            save_data()
            break

    refresh_table()

def delete_all_classes():
    if not data["classes"]:
        messagebox.showinfo("Nothing to delete", "Your timetable is already empty.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete All",
        "Are you sure you want to delete ALL timetable entries?"
    )

    if confirm:
        data["classes"] = []
        save_data()
        refresh_table()
        messagebox.showinfo("Deleted", "All timetable entries have been removed.")

def print_timetable():
    if not data["classes"]:
        messagebox.showerror("Error", "No timetable data to print.")
        return

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    file_path = temp_file.name

    with open(file_path, "w") as f:
        f.write("STUDENT TIMETABLE\n")
        f.write("=================\n\n")
        for c in data["classes"]:
            f.write(f"{c['day']}  {c['start']} - {c['end']}\n")
            f.write(f"Subject: {c['subject']}\n")
            f.write(f"Teacher: {c['teacher']}\n")
            f.write(f"Room: {c['room']}\n")
            f.write("\n")

    os.startfile(file_path, "print")
    messagebox.showinfo("Printed", "Timetable sent to printer.")

def toggle_theme():
    current = root.style.theme.name
    if current in ["flatly", "cosmo", "litera", "minty"]:
        root.style.theme_use("superhero")
    else:
        root.style.theme_use("flatly")
        
def show_page(page):
    page.lift()

def clear_form():
    subject_entry.delete(0, tk.END)
    day_var.set("Monday")
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    teacher_entry.delete(0, tk.END)
    room_entry.delete(0, tk.END)

def refresh_table():
    for row in table.get_children():
        table.delete(row)

    for i, c in enumerate(data["classes"]):
        tag = "odd" if i % 2 == 0 else "even"
        table.insert(
            "",
            "end",
            values=(c["day"], c["start"], c["end"], c["subject"], c["teacher"], c["room"]),
            tags=(tag,)
        )

# ---------- Main window ----------

root = ttk.Window(themename="flatly")
root.title("School Timetable Portal")
root.geometry("1280x720")

data = load_data()

# Header bar
header = ttk.Frame(root, padding=15, bootstyle="primary")
header.pack(fill="x")

ttk.Label(header,
          text="School Timetable Portal",
          font=("Segoe UI", 22, "bold"),
          bootstyle="inverse-primary").pack(side="left")

ttk.Button(header,
           text="Toggle Theme",
           command=toggle_theme,
           bootstyle="light").pack(side="right", padx=10)

# Main layout: sidebar + content
main_area = ttk.Frame(root)
main_area.pack(fill="both", expand=True)

sidebar = ttk.Frame(main_area, padding=15, bootstyle="dark")
sidebar.pack(side="left", fill="y")

ttk.Label(sidebar, text="Navigation", bootstyle="inverse-dark",
          font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))

ttk.Button(sidebar, text="Timetable", width=20,
           bootstyle="secondary",
           command=lambda: show_page(timetable_page)).pack(pady=5)

ttk.Button(sidebar, text="Add Class", width=20,
           bootstyle="secondary",
           command=lambda: show_page(addclass_page)).pack(pady=5)

ttk.Button(sidebar, text="Settings", width=20,
           bootstyle="secondary",
           command=lambda: show_page(settings_page)).pack(pady=5)

content = ttk.Frame(main_area, padding=15)
content.pack(side="left", fill="both", expand=True)

# --- Pages (Frames) ---
timetable_page = ttk.Frame(content)
addclass_page = ttk.Frame(content)
settings_page = ttk.Frame(content)

for page in (timetable_page, addclass_page, settings_page):
    page.place(relx=0, rely=0, relwidth=1, relheight=1)


# Form card
form_card = ttk.Labelframe(content, text="Add New Class",
                           padding=20, bootstyle="info")
form_card.pack(side="left", fill="y", padx=10, pady=10)

ttk.Label(form_card, text="Subject").grid(row=0, column=0, sticky="w", pady=5)
subject_entry = ttk.Entry(form_card, width=25)
subject_entry.grid(row=0, column=1, pady=5)

ttk.Label(form_card, text="Day").grid(row=1, column=0, sticky="w", pady=5)
day_var = tk.StringVar(value="Monday")
day_dropdown = ttk.Combobox(
    form_card,
    textvariable=day_var,
    values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    state="readonly",
    width=22
)
day_dropdown.grid(row=1, column=1, pady=5)

ttk.Label(form_card, text="Start (HH:MM)").grid(row=2, column=0, sticky="w", pady=5)
start_entry = ttk.Entry(form_card, width=25)
start_entry.grid(row=2, column=1, pady=5)

ttk.Label(form_card, text="End (HH:MM)").grid(row=3, column=0, sticky="w", pady=5)
end_entry = ttk.Entry(form_card, width=25)
end_entry.grid(row=3, column=1, pady=5)

ttk.Label(form_card, text="Teacher").grid(row=4, column=0, sticky="w", pady=5)
teacher_entry = ttk.Entry(form_card, width=25)
teacher_entry.grid(row=4, column=1, pady=5)

ttk.Label(form_card, text="Room").grid(row=5, column=0, sticky="w", pady=5)
room_entry = ttk.Entry(form_card, width=25)
room_entry.grid(row=5, column=1, pady=5)

add_button = ttk.Button(form_card, text="Add Class",
                        command=add_class, bootstyle="success", width=20)
add_button.grid(row=6, column=0, columnspan=2, pady=10)

delete_button = ttk.Button(form_card, text="Delete Selected Class",
                           command=delete_class, bootstyle="danger", width=20)
delete_button.grid(row=7, column=0, columnspan=2, pady=5)

delete_all_button = ttk.Button(form_card, text="Delete ALL Classes",
                               command=delete_all_classes, bootstyle="danger", width=20)
delete_all_button.grid(row=8, column=0, columnspan=2, pady=5)

print_button = ttk.Button(form_card, text="Print Timetable",
                          command=print_timetable, bootstyle="info", width=20)
print_button.grid(row=9, column=0, columnspan=2, pady=5)

# Timetable card
table_card = ttk.Labelframe(content, text="Timetable",
                            padding=20, bootstyle="primary")
table_card.pack(side="left", fill="both", expand=True, padx=10, pady=10)

columns = ("Day", "Start", "End", "Subject", "Teacher", "Room")
table = ttk.Treeview(table_card, columns=columns, show="headings", bootstyle="info")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=130, anchor="center")

table.pack(fill="both", expand=True)

# Table styling
style = ttk.Style()
style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
table.tag_configure("odd", background="#f8f9fa")
table.tag_configure("even", background="#ffffff")

refresh_table()

root.mainloop()

# --- Timetable Page ---
#table_card = ttk.Labelframe(timetable_page, text="Student Timetable",
#                            padding=20, bootstyle="primary")
#table_card.pack(fill="both", expand=True, padx=20, pady=20)

#columns = ("Day", "Start", "End", "Subject", "Teacher", "Room")
#table = ttk.Treeview(table_card, columns=columns, show="headings", bootstyle="info")

#for col in columns:
#    table.heading(col, text=col)
#    table.column(col, width=150, anchor="center")

#table.pack(fill="both", expand=True)

# Table styling
#style = ttk.Style()
#style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
#style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
#table.tag_configure("odd", background="#f8f9fa")
#table.tag_configure("even", background="#ffffff")

#show_page(timetable_page)
#refresh_table()