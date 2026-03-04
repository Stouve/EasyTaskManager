from infrastructure.database import get_connection
from core.models import Task


class SQLiteTaskRepository:

    def add(self,title:str, description:str):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("INSERT INTO tasks (title,description) VALUES (?,?)",
                       (title,description)
                       )
        conn.commit()
        conn.close()

    def get_all_tasks(self):

         conn=get_connection()
         cursor=conn.cursor()
         cursor.execute("SELECT * FROM tasks")
         tasks=cursor.fetchall()
         conn.close()

         return tasks

    def mark_done(self,task_id):

        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'done' WHERE id=?",
                       (task_id,))
        conn.commit()
        conn.close()

    def delete(self,task_id):

        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?",(task_id,))
        conn.commit()
        conn.close()
