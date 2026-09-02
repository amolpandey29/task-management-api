def get_all_tasks(connection):
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    cursor.close()

    return tasks


def create_task(connection, title, completed):
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO tasks(title, completed) VALUES (%s, %s)",
        (title, completed)
    )
    connection.commit()

    last_row_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (last_row_id,)
    )
    new_task = cursor.fetchone()

    cursor.close()

    return new_task


def get_task(connection, task_id):
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )
    task = cursor.fetchone()

    cursor.close()

    return task


def update_task(connection, task_id, title, completed):
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    existing_task = cursor.fetchone()

    if existing_task is None:
        cursor.close()
        return None

    if title is not None and completed is not None:
        cursor.execute(
            "UPDATE tasks SET title = %s, completed = %s WHERE id = %s",
            (title, completed, task_id)
        )
        connection.commit()

    elif title is not None:
        cursor.execute(
            "UPDATE tasks SET title = %s WHERE id = %s",
            (title, task_id)
        )
        connection.commit()

    elif completed is not None:
        cursor.execute(
            "UPDATE tasks SET completed = %s WHERE id = %s",
            (completed, task_id)
        )
        connection.commit()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    updated_task = cursor.fetchone()

    cursor.close()

    return updated_task


def delete_task(connection, task_id):
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )
    existing_task = cursor.fetchone()

    if existing_task is None:
        cursor.close()
        return None

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )
    connection.commit()

    cursor.close()

    return {"message": "Task deleted"}
