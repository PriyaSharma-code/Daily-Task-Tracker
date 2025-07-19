Here’s a **README.md** you can include with your app. It’s clear, friendly, and includes instructions for running and packaging!

---

# 📝 Daily Task Reminder

A **dark & girly-themed desktop task reminder app** with Microsoft Teams notifications built using Python and Tkinter.

✨ Features:

* Add tasks with a time using a selector or manual entry
* Mark tasks as complete ✅ (moves to bottom)
* Delete tasks ❌
* Automatically sends a Microsoft Teams message at the scheduled time
* Dark & aesthetic theme

---

## 📋 Requirements

* Python 3.8+
* macOS / Windows / Linux
* Internet connection (for Teams notifications)

Python dependencies:

```
requests
```

Install them:

```bash
pip install requests
```

---

## 🚀 How to Run

1️⃣ Clone/download the repository or save the `.py` file.

2️⃣ Open a terminal and navigate to the folder.

3️⃣ Run the app:

```bash
python3 daily_task_reminder.py
```

---

## 🖥 Packaging Into an Executable (Optional)

If you want to run without needing Python every time:

### On macOS / Windows / Linux

1. Install [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller
```

2. Run:

```bash
pyinstaller --onefile --windowed --icon=icon.icns -n "TaskReminder" daily_task_reminder.py
```

3. Find the output in the `dist/` folder:

   * macOS: `.app` file
   * Windows: `.exe` file

4. Share or double-click to run!

---

## 🔗 Microsoft Teams Setup

This app sends reminders to a Teams channel using a webhook.

1️⃣ Go to your Teams channel → More Options → Connectors → Incoming Webhook.

2️⃣ Generate a webhook URL.

3️⃣ Replace the `TEAMS_WEBHOOK_URL` variable in the code with your webhook:

```python
TEAMS_WEBHOOK_URL = "https://outlook.office.com/webhook/your-webhook-url"
```
---

## 🧡 Credits

Developed by \PriyaSharma.
Made with Python, Tkinter & a lot of 💻 + ☕.

---

If you want, I can also generate you a `requirements.txt` and a `LICENSE.md` to make it even more complete — just say the word!
