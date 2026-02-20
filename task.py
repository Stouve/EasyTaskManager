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

    def __post_init__(self) -> None:
        """
        Post initialization Validiation
        """
        if not isinstance(self.id, int):
            raise TypeError("Task id must be an integer")
        if self.id < 0:
            raise ValueError("Task id must be greater than 0")
        if not isinstance(self.title, str):
            raise TypeError("Task title must be an string")
        if not self.title.strip():
            raise ValueError("Task title must not be empty")
        if not isinstance(self.done, bool):
            raise TypeError("Task done must be a boolean")

    def mark_done(self) -> None:
        """
        Marks the task as done
        """
        self.done = True

    def mark_undone(self) -> None:
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

