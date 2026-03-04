from infrastructure.database import init_db
1from infrastructure.repository import SQLiteTaskRepository
from core.services import TaskService

def main():

        init_db()
        repository=SQLiteTaskRepository()

        manager = TaskService(repository)

        while True:
            print("\n1. Add task")
            print("2. List tasks")
            print("3. Complete task")
            print("4. Remove task")
            print("5. Exit")

            choice=input("Enter your choice:")
            if choice=="1":
                name=input("Title:")
                desc=input("Description:")
                manager.create_task(name, desc)

            elif choice=="2":
                tasks=manager.list_tasks()
                for element in tasks:
                    print(element)

            elif choice=="3":
                id=int(input("Task ID:"))
                manager.complete_task(id)

            elif choice=="4":
                id=int(input("Task ID:"))
                manager.delete_task(id)

            elif choice=="5":
                break

if __name__ == '__main__':
    main()
