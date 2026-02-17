import json
import sys


def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)


if __name__ == "__main__":
    command = sys.argv[1]

    if command == "add":
        add_task(sys.argv[2])
