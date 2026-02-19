from dataclasses import dataclass, asdict

@dataclass
class Task():
    """
    This represents a task

    Attributes:
        id(int) : unique identifier of the task
        title (str) : title of the task
        done (bool) : whether the task is done or not
    """
    id: int
    title: str
    done: bool = False

    def mark_done(self):
        """
        Marks the task as done
        """
        self.done = True

    def mark_undone(self):
        """
        Marks the task as undone
        """
        self.done = False

    def to_dict(self)->dict:
        """
        Transforms the task to a serializable dict JSON
        """
        #asdict transform dataclass into dict
        return{asdict(self)}

    @classmethod
    def from_dict(cls, data:dict)->Task:
        """
        Create the task from a serializable dict JSON
        Args:
            data (dict): JSON data
        Returns:
            Task: Task object
        """
        #** break dictionary in named arguments
        return cls(**data)

    def __str__(self):
        """
        String representation of the task
        """
        status = "X" if self.done else " "
        return f"{self.id} - {self.title} |{status}|"

