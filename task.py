from dataclasses import dataclass, asdict


@dataclass
class Task():
    id: int
    title: str
    done: bool = False

    def mark_done(self):
        self.done = True

    def __str__(self):
        return(self.title + " : " + self.done)

    def to_dict(self)->dict:
        #asdict transform dataclass into dict
        return{asdict(self)}

    @classmethod
    def from_dict(cls, data:dict):
        #** break dictionary in named arguments
        return cls(**data)

