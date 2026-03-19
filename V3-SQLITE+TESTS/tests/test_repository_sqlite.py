from core.models import TaskStatus

def test_add_and_get(repo):
    task = repo.add("Test",None)

    tasks=repo.get_all_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "Test"

def test_get_by_id(repo):
    task = repo.add("Test",None)

    result=repo.get_by_id(task.id)
    assert result is not None
    assert result.id == task.id

def mark_done(repo):
    task = repo.add("Test",None)

    repo.mark_done(task.id)

    updated_task = repo.get_by_id(task.id)

    assert updated_task.status == TaskStatus.DONE

def test_delete(repo):
    task = repo.add("Test",None)

    repo.delete(task.id)

    tasks=repo.get_all_tasks()

    assert len(tasks) == 0

