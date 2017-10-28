"""Operations are defined here"""

from todo.models import Task
from todo.exceptions import NotFoundError
from todo.database import session
from todo.schemas import TaskSchema


def get_tasks():
    """Get all tasks"""
    tasks = Task.query.all()
    return TaskSchema().dump(tasks, many=True).data


def get_task(task_id):
    """Get task by id"""
    task = Task.query.get(task_id)
    if not task:
        raise NotFoundError('Task not found.')

    return TaskSchema().dump(task).data


def create_task(request_body):
    """Create a task"""
    request_body = Task(**request_body)
    session.add(request_body)
    session.commit()

    return TaskSchema().dump(request_body).data


def update_task(task_id, request_body):
    """Update a task"""
    task = Task.query.get(task_id)
    if not task:
        raise NotFoundError('Task not found.')

    for key, value in request_body.items():
        setattr(task, key, value)

    session.commit()

    return TaskSchema().dump(task).data


def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    if not task:
        raise NotFoundError('Task not found.')

    session.delete(task)
    session.commit()

    return None, 200
