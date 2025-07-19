import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import threading
import time
import requests

TEAMS_WEBHOOK_URL = "https://outlook.office.com/webhook/your-webhook-url"  # Replace
tasks = []

def send_teams_message(task, time_str):
    message = {"text": f"⏰ Reminder: *{task}* scheduled for {time_str}"}
    response = requests.post(TEAMS_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print("Failed to send to Teams", response.text)

def reminder_thread():
    while True:
        now = datetime.now()
        for task in tasks[:]:
            task_time = task['time']
            if now >= task_time:
                send_teams_message(task['task'], task_time.strftime("%I:%M %p"))
                tasks.remove(task)
        time.sleep(30)

def add_task(event=None):
    task = task_entry.get().strip()
    hour = hour_var.get()
    minute = minute_var.get()
    manual_time = time_entry.get().strip()

    if not task: return

    try:
        if manual_time:
            task_time = datetime.strptime(manual_time, "%H:%M")
        else:
            task_time = datetime.strptime(f"{hour}:{minute}", "%H:%M")

        today = datetime.today()
        task_time = task_time.replace(year=today.year, month=today.month, day=today.day)
        if task_time < datetime.now():
            task_time += timedelta(days=1)

        task_data = {"task": task, "time": task_time}
        tasks.append(task_data)
        insert_task(task_data, completed=False)

        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Invalid Time", "Enter time as HH:MM or select from dropdown")

def insert_task(task_data, completed):
    card = tk.Frame(task_list_frame, bg="#2c2b4f", bd=1, relief=tk.RIDGE)
    card.pack(fill="x", pady=4, padx=10)

    def on_hover(e): card.configure(bg="#3a3960")
    def on_leave(e): card.configure(bg="#2c2b4f")

    card.bind("<Enter>", on_hover)
    card.bind("<Leave>", on_leave)

    check = tk.Button(card, text="✓", fg="#bb86fc", bg="#1f1f2e", bd=0, font=("Arial", 12, "bold"),
                      command=lambda: complete_task(card, task_data))
    check.pack(side=tk.LEFT, padx=5)

    task_lbl = tk.Label(
        card,
        text=f"{task_data['task']}  •  {task_data['time'].strftime('%I:%M %p')}",
        bg="#2c2b4f",
        fg="#f5c2e7" if not completed else "#666",
        font=("Arial", 12)
    )
    task_lbl.pack(side=tk.LEFT, padx=10)

    delete_btn = tk.Button(card, text="❌", fg="#f28b82", bg="#1f1f2e", bd=0, font=("Arial", 12),
                           command=lambda: delete_task(card, task_data))
    delete_btn.pack(side=tk.RIGHT, padx=5)

    if completed:
        task_lbl.config(fg="#666")
        card.pack_forget()
        card.pack(side=tk.BOTTOM, fill="x", pady=4, padx=10)

def complete_task(card, task_data):
    card.pack_forget()
    tasks.remove(task_data)
    insert_task(task_data, completed=True)

def delete_task(card, task_data):
    card.destroy()
    tasks.remove(task_data)

# === Main App ===
app = tk.Tk()
app.title("🌙✨ Daily Task Reminder")
app.geometry("520x600")
app.configure(bg="#1e1e2f")

tk.Label(app, text="Task", bg="#1e1e2f", fg="#f5c2e7", font=("Arial", 12)).pack()
task_entry = tk.Entry(app, width=40, font=("Arial", 12), bg="#2c2b4f", fg="#f5c2e7", insertbackground="white")
task_entry.pack(pady=3)
task_entry.bind("<Return>", add_task)

tk.Label(app, text="Time", bg="#1e1e2f", fg="#f5c2e7", font=("Arial", 12)).pack(pady=3)

time_frame = tk.Frame(app, bg="#1e1e2f")
time_frame.pack()

hour_var = tk.StringVar()
minute_var = tk.StringVar()

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#2c2b4f", background="#2c2b4f", foreground="#f5c2e7")

hour_dropdown = ttk.Combobox(time_frame, textvariable=hour_var, width=5, values=[f"{i:02d}" for i in range(24)], font=("Arial", 11))
hour_dropdown.set("09")
hour_dropdown.pack(side=tk.LEFT, padx=2)

tk.Label(time_frame, text=":", bg="#1e1e2f", fg="#f5c2e7").pack(side=tk.LEFT)

minute_dropdown = ttk.Combobox(time_frame, textvariable=minute_var, width=5, values=[f"{i:02d}" for i in range(0, 60, 5)], font=("Arial", 11))
minute_dropdown.set("00")
minute_dropdown.pack(side=tk.LEFT, padx=2)

tk.Label(app, text="or enter time (HH:MM)", bg="#1e1e2f", fg="#f5c2e7", font=("Arial", 11)).pack(pady=3)
time_entry = tk.Entry(app, width=20, font=("Arial", 11), bg="#2c2b4f", fg="#f5c2e7", insertbackground="white")
time_entry.pack(pady=2)

add_btn = tk.Button(app, text="➕ Add Task", command=add_task, bg="#bb86fc", fg="#1e1e2f", font=("Arial", 12), width=20)
add_btn.pack(pady=10)

separator = tk.Frame(app, height=2, bd=1, relief=tk.SUNKEN, bg="#444")
separator.pack(fill="x", pady=5)

task_list_frame = tk.Frame(app, bg="#1e1e2f")
task_list_frame.pack(pady=10, fill="both", expand=True)

threading.Thread(target=reminder_thread, daemon=True).start()

app.mainloop()
