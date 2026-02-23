import sys

from task_manager import TaskManager

manager=TaskManager()

command = sys.argv[1]

if command =="add":
    title=sys.argv[2]
    task=manager.add_task(title)
    print(f"Task added: {task}")

elif command =="list":
    list=manager.list_tasks()
    for task in list:
        print(task)

elif command =="done":
    task_id=int(sys.argv[2])
    if manager.complete_task(task_id):
        print(f"Task {task_id} | Done")
    else:
        print(f"Task {task_id} | NOT FOUND")

elif command =="undone":
    task_id=int(sys.argv[2])
    if manager.reset_task(task_id):
        print(f"Task {task_id} | reset to Undone")
    else:
        print(f"Task {task_id} | NOT FOUND")

elif command =="delete":
    task_id=int(sys.argv[2])
    if manager.delete_task(task_id):
        print(f"Task {task_id} | DELETED")
    else:
        print(f"Task {task_id} | NOT FOUND")
else:
    print(f"Unknown command, please use : ")
    print(f"-python app.py list")
    print(f"-python app.py add $title")
    print(f"-python app.py done $id")
    print(f"-python app.py undone $id")
    print(f"-python app.py delete $id")
