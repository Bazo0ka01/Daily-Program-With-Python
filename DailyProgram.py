import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
import time
import pyttsx3

window_width = 400
window_height = 500

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def alarm_trigger(window, idx, task_text):
    messagebox.showinfo("Task Time", f"Time is up: {task_text}")
    speak(f"Task time: {task_text}")

    if idx < len(alarms):
        task_listbox.delete(idx)
        del alarms[idx]

def check_alarms(window):
    while True:
        now = datetime.datetime.now()
        triggered_indices = []
        for i, alarm in enumerate(alarms):
            alarm_time, task_text = alarm
            if now >= alarm_time:
                triggered_indices.append(i)

        for i in reversed(triggered_indices):
            alarm_time, task_text = alarms[i]
            window.after(0, alarm_trigger, window, i, task_text)
            del alarms[i]
            task_listbox.delete(i)

        time.sleep(5)

def add_task():
    global alarms
    task = task_entry.get()
    if task == "" or task == placeholder_text:
        messagebox.showwarning("Warning", "Please enter a task!")
        return

    try:
        year = int(year_combo.get())
        month = int(month_combo.get())
        day = int(day_combo.get())
        hour = int(hour_combo.get())
        minute = int(minute_combo.get())
        alarm_time = datetime.datetime(year, month, day, hour, minute)
    except Exception:
        messagebox.showwarning("Warning", "Please select a valid date and time!")
        return

    if alarm_time <= datetime.datetime.now():
        messagebox.showwarning("Warning", "Selected time cannot be in the past!")
        return

    alarms.append((alarm_time, task))
    display_text = f"{task} - {alarm_time.strftime('%Y-%m-%d %H:%M')}"
    task_listbox.insert(tk.END, display_text)

    task_entry.delete(0, tk.END)
    task_entry.insert(0, placeholder_text)
    task_entry.config(fg="gray")

def delete_task():
    global alarms
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to delete!")
        return
    idx = selected[0]
    if idx < len(alarms):
        task_listbox.delete(idx)
        del alarms[idx]
    else:
        messagebox.showerror("Error", "Failed to delete task, index error.")

def on_entry_click(event):
    if task_entry.get() == placeholder_text:
        task_entry.delete(0, tk.END)
        task_entry.config(fg="black")

def on_focus_out(event):
    if task_entry.get() == "":
        task_entry.insert(0, placeholder_text)
        task_entry.config(fg="gray")

def draw_window():
    global task_entry, task_listbox, placeholder_text
    global year_combo, month_combo, day_combo, hour_combo, minute_combo
    global alarms

    alarms = []

    window = tk.Tk()
    window.title("Daily Planner")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)
    window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    main_label = tk.Label(window, text="DAILY PLANNER", font=("Arial", 16))
    main_label.pack(pady=10)

    placeholder_text = "Write your task here..."
    task_entry = tk.Entry(window, fg="gray", width=40)
    task_entry.insert(0, placeholder_text)
    task_entry.bind("<FocusIn>", on_entry_click)
    task_entry.bind("<FocusOut>", on_focus_out)
    task_entry.pack(pady=5)

    frame = tk.Frame(window)
    frame.pack(pady=5)

    year_combo = ttk.Combobox(frame, width=5, values=[str(y) for y in range(2023, 2031)])
    year_combo.set(str(datetime.datetime.now().year))
    year_combo.grid(row=0, column=0)

    month_combo = ttk.Combobox(frame, width=3, values=[f"{m:02}" for m in range(1, 13)])
    month_combo.set(f"{datetime.datetime.now().month:02}")
    month_combo.grid(row=0, column=1)

    day_combo = ttk.Combobox(frame, width=3, values=[f"{d:02}" for d in range(1, 32)])
    day_combo.set(f"{datetime.datetime.now().day:02}")
    day_combo.grid(row=0, column=2)

    hour_combo = ttk.Combobox(frame, width=3, values=[f"{h:02}" for h in range(0, 24)])
    hour_combo.set(f"{datetime.datetime.now().hour:02}")
    hour_combo.grid(row=0, column=3)

    minute_combo = ttk.Combobox(frame, width=3, values=[f"{m:02}" for m in range(0, 60)])
    minute_combo.set(f"{datetime.datetime.now().minute:02}")
    minute_combo.grid(row=0, column=4)

    add_button = tk.Button(window, text="Add Task", command=add_task)
    add_button.pack(pady=10)

    task_listbox = tk.Listbox(window, width=60, height=15)
    task_listbox.pack(pady=10)

    delete_button = tk.Button(window, text="Delete Selected Task", command=delete_task)
    delete_button.pack(pady=5)

    t = threading.Thread(target=check_alarms, args=(window,), daemon=True)
    t.start()

    window.mainloop()

if __name__ == "__main__":
    draw_window()
