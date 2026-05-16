import pytest
from models import add_task, filter_tasks_by_priority
from database import init_db, get_connection
from models import get_all_tasks, mark_task_complete, delete_task


@pytest.fixture(autouse=True)
def setup_database():
    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()


def test_add_task_valid():
    add_task("Study SCD", "High", "2026-06-20")
    tasks = get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Study SCD"


def test_add_task_empty_title():
    with pytest.raises(ValueError):
        add_task("", "Low", "2026-06-20")


def test_add_task_invalid_priority():
    with pytest.raises(ValueError):
        add_task("Buy Laptop", "Urgent", "2026-06-20")


def test_mark_task_complete():
    add_task("Do Assignment", "Medium", None)
    tasks = get_all_tasks()
    task_id = tasks[0]["id"]

    mark_task_complete(task_id)

    updated_tasks = get_all_tasks()
    assert updated_tasks[0]["completed"] == 1


def test_delete_task():
    add_task("Temporary Task", "Low", None)
    tasks = get_all_tasks()
    task_id = tasks[0]["id"]

    delete_task(task_id)

    tasks_after = get_all_tasks()
    assert len(tasks_after) == 0


def test_filter_tasks_by_priority():
    add_task("Task A", "Low", None)
    add_task("Task B", "High", None)

    high_tasks = filter_tasks_by_priority("High")
    assert len(high_tasks) == 1
    assert high_tasks[0]["title"] == "Task B"


def test_filter_tasks_invalid_priority():
    with pytest.raises(ValueError):
        filter_tasks_by_priority("SuperHigh")