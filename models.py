from database import get_connection


def add_task(title, priority, deadline):
    if not title or title.strip() == "":
        raise ValueError("Task title cannot be empty")

    if priority not in ["Low", "Medium", "High"]:
        raise ValueError("Invalid priority value")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, priority, deadline, completed) VALUES (?, ?, ?, ?)",
        (title.strip(), priority, deadline, 0)
    )

    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()

    conn.close()
    return tasks


def mark_task_complete(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def filter_tasks_by_priority(priority):
    if priority not in ["Low", "Medium", "High"]:
        raise ValueError("Invalid priority value")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE priority = ? ORDER BY id DESC", (priority,))
    tasks = cursor.fetchall()

    conn.close()
    return tasks