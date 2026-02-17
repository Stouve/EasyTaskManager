import uuid


class Task():

    def __init__(self,pos:int, title:str, done: bool=False):
        self.id = pos
        self.title = title
        self.done = done

    def mark_done(self):
        self.done = True

    def __str__(self):
        return(self.title + " : " + self.done)

    def to_dict(self)->dict:
        return{
            "id":self.id,
            "title":self.title,
            "done":self.done
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            task_id=data["id"],
            title=data["title"],
            done=data["done"]
        )

