import json
import sys


def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def list_tasks():
    try:
        with open("tasks.json", "r") as f:
            tasks=json.load(f)
            for element in tasks:
                print(f"Task : {element["title"]}, DONE") if element["done"] is True else print(f"Task : {element["title"]}, TODO")

    except FileNotFoundError:
        print("Tasks file not found.")


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)

def end_task(pos):
    tasks = load_tasks()
    tasks[int(pos)-1]["done"] = True
    save_tasks(tasks)

def remove_task(pos):

    try:
        tasks = load_tasks()
        print(f"Deleting task: {tasks[int(pos)-1]['title']} ")
        tasks.pop(int(pos)-1)
        save_tasks(tasks)

    except IndexError:
        print(f"Error Task number {pos} not found. Please check tasks.json file")

if __name__ == "__main__":
    command = sys.argv[1]

    if command == "add":
        add_task(sys.argv[2])
    elif command == "list":
        list_tasks()
    elif command == "remove":
        remove_task(sys.argv[2])
    elif command == "done":
        end_task(sys.argv[2])