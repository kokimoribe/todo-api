"""Operations are defined here"""
from sqlalchemy.orm import joinedload, raiseload

from todo.models import Board, Task
from todo.exceptions import NotFoundError
from todo.database import session
from todo.schemas import BoardSchema, BoardDetailsSchema, TaskSchema


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


def create_task(board_id, request_body):
    """Create a task"""
    board = Board.query.get(board_id)

    if not board:
        raise NotFoundError('Board not found.')

    board.task_number += 1
    task = Task(board_id=board_id, number=board.task_number, **request_body)
    session.add(task)
    session.commit()

    return TaskSchema().dump(task).data


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


def get_boards():
    """Get boards"""
    boards = Board.query.all()
    return BoardSchema().dump(boards, many=True).data


def create_board(request_body):
    """Create a board"""
    print(request_body)
    board = Board(**request_body)
    session.add(board)
    session.commit()

    return BoardSchema().dump(board).data


def get_board(board_id):
    """Get a board"""
    query = Board.query.filter(Board.id == board_id)
    query = query.options(joinedload(Board.tasks)).options(raiseload('*'))
    board = query.one_or_none()

    if not board:
        raise NotFoundError('Board not found.')

    return BoardDetailsSchema().dump(board).data


def update_board(board_id, request_body):
    """Update a board"""
    board = Board.query.get(board_id)

    if not board:
        raise NotFoundError('Board not found.')

    for key, value in request_body.items():
        setattr(board, key, value)

    session.commit()

    return BoardSchema().dump(board).data


def delete_board(board_id):
    """Delete a board and its tasks"""
    query = Board.query.filter(Board.id == board_id)
    query = query.options(joinedload(Board.tasks)).options(raiseload('*'))
    board = query.one_or_none()

    if not board:
        raise NotFoundError('Board not found.')

    for task in board.tasks:
        session.delete(task)

    session.delete(board)
    session.commit()

    return None, 200


def get_demo_board():
    """Get a demo board"""
    return get_board(1)
