import pytest

from core.services import TaskService, InvalidTaskError
from core.models import Task, TaskStatus
from datetime import datetime

class FakeRepository:
    def __init__(self):
        self.tasks = {}
        self.counter = 1
