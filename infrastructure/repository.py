from datetime import datetime
from typing import Optional

from infrastructure.database import get_connection
from core.models import Task, TaskStatus


class SQLiteTaskRepository:

    #-------------------------------
    #CREATE
    #-------------------------------
    def add(self,title:str, description:Optional[str])->Task:

        conn=get_connection()
        cursor=conn.cursor()

        now=datetime.now(datetime.UTC).isoformat()

        cursor.execute("INSERT INTO tasks (title,description,status,created_at) VALUES (?,?,?,?)",
                       (title,description,TaskStatus.PENDING.value,now),
                       )

        #get the id of the last id generated
        task_id=cursor.lastrowid

        conn.commit()
        conn.close()

        return Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.fromordinal(now),
        )

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
