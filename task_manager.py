from asyncio import tasks
from pathlib import Path


from task import Task
import json


class TaskManager():
    """
    Handle operations and tasks persistence
    """

    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)
        self.tasks: List[Task] = []
        self._load_tasks()



    def _load_tasks(self)->None:
        """
        Load tasks from json file
        """
        if not self.file_path.exists():
            self.tasks = []
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                self.tasks = [Task.from_dict(item) for item in data]
        except json.decoder.JSONDecodeError:
            self.tasks = []

    def _save_tasks(self)->None:
        """
        Save tasks to JSON file
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(
                [Task.to_dict() for task in self.tasks],
                f,
                indent=4,
                ensure_ascii=False
            )

    def add_task(self, title):
        task = Task(title)
        self.tasks.append(task)

    def list_tasks(self):
        for task in list(self.tasks):
            print(f"Task : {task.title}, Status : Done") if task.done else print(f"Task : {task.title}, Status : TODO")

    def gest_task(self):


    def complete_task(self):


    def delete_task(self, pos):
        print(f"Deleting Task : {self.tasks[pos]}")

    def _generate_next_id(self):


