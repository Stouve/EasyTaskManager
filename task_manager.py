from task import Task

class TaskManager():

    def __init__(self):
        self.tasks = []

    def addTask(self, title):
        task = Task(title)
        self.tasks.append(task)

    def listTasks(self):
        for task in list(self.tasks):
            print(f"Task : {task.title}, Status : Done") if task.done else print(f"Task : {task.title}, Status : TODO")

    def removeTask(self, pos):
        print(f"Deleting Task : {self.tasks[pos]}")



