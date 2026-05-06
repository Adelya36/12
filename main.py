import tkinter as tk
from tkinter import messagebox
import json
import random
import os

TASKS_FILE = "tasks.json"

# Предопределённые задачи
PREDEFINED_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть лекцию", "type": "учёба"},
    {"name": "Сходить на пробежку", "type": "спорт"},
    {"name": "Провести встречу", "type": "работа"},
]

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def generate_task():
    task = random.choice(PREDEFINED_TASKS)
    history.append(task)
    save_tasks(history)
    update_history_list()

def add_task():
    name = entry_task_name.get().strip()
    task_type = entry_task_type.get().strip().lower()
    if not name or not task_type:
        messagebox.showwarning("Ошибка", "Поля не должны быть пустыми!")
        return
    task = {"name": name, "type": task_type}
    history.append(task)
    save_tasks(history)
    entry_task_name.delete(0, tk.END)
    entry_task_type.delete(0, tk.END)
    update_history_list()

def filter_tasks():
    selected_type = filter_var.get()
    if selected_type == "все":
        filtered = history
    else:
        filtered = [t for t in history if t["type"] == selected_type]
    update_history_list(filtered)

def update_history_list(filtered=None):
    list_history.delete(0, tk.END)
    tasks_to_show = filtered if filtered is not None else history
    for t in tasks_to_show:
        list_history.insert(tk.END, f"{t['name']} ({t['type']})")

# Загрузка истории
history = load_tasks()

# Создание окна
root = tk.Tk()
root.title("Random Task Generator")

# Кнопка генерации задачи
btn_generate = tk.Button(root, text="Сгенерировать задачу", command=generate_task)
btn_generate.pack(pady=5)

# Поля для добавления задачи
frame_add = tk.Frame(root)
frame_add.pack(pady=5)
tk.Label(frame_add, text="Название задачи:").pack(side=tk.LEFT)
entry_task_name = tk.Entry(frame_add)
entry_task_name.pack(side=tk.LEFT, padx=5)
tk.Label(frame_add, text="Тип (учёба/спорт/работа):").pack(side=tk.LEFT)
entry_task_type = tk.Entry(frame_add)
entry_task_type.pack(side=tk.LEFT, padx=5)
btn_add = tk.Button(root, text="Добавить задачу", command=add_task)
btn_add.pack(pady=5)

# Фильтр по типу
filter_var = tk.StringVar(value="все")
types = ["все", "учёба", "спорт", "работа"]
for t in types:
    tk.Radiobutton(root, text=t.capitalize(), variable=filter_var, value=t, command=filter_tasks).pack(anchor=tk.W)

# Список истории
list_history = tk.Listbox(root, width=50, height=10)
list_history.pack(pady=10)
update_history_list()

root.mainloop()