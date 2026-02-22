from asyncio import tasks
from pathlib import Path

import task
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

    def add_task(self, title)->None:
        """
        Add a new task
        """
        task_id = self._generate_next_id()
        task = Task(task_id, title)
        self.tasks.append(task)

    def list_tasks(self)->List[Task]:
        """
        return all tasks
        """
        return self.tasks


    def gest_task(self,task_id:int)->Task:
        """
        Return task by ID
        """
        for task in self.tasks:
            if task.id == task_id:
                return task

        return  None

    def complete_task(self,task_id:int)->bool:
        """
        Complete task
        """
        task=self.gest_task(task_id)

        if not task:
            return False

        task.mark_done()
        self._save_tasks()
        return True

    def delete_task(self, task_id:int)->bool:
        """
        Delete task by ID
        """
        task=self.gest_task(task_id)

        if not task:
            return False

        self.tasks.remove(task)
        return True

        print(f"Deleting Task : {self.tasks[pos]}")

    def _generate_next_id(self)-> int:
        """
        Generate next task ID
        """
        if not self.tasks:
            return 1

        return max(task.id for task in self.tasks) + 1

