"""Operations are defined here"""
from sqlalchemy.orm import joinedload, raiseload

from todo.models import Board, Task
from todo.exceptions import NotFoundError
from todo.database import session
from todo.schemas import BoardSchema, BoardDetailsSchema, TaskSchema
from todo.auth import requires_auth


@requires_auth
def create_task(board_id, request_body, user_id):
    """Create a task"""
    query = Board.query.filter(Board.id == board_id, Board.user_id == user_id)
    board = query.one_or_none

    if not board:
        raise NotFoundError('Board not found.')

    board.task_number += 1
    task = Task(board_id=board_id, number=board.task_number, **request_body)
    session.add(task)
    session.commit()

    return TaskSchema().dump(task).data


@requires_auth
def update_task(task_id, request_body, user_id):
    """Update a task"""
    query = Task.query.join(Board).filter(
        Task.id == task_id, Board.user_id == user_id)
    task = query.one_or_none()

    if not task:
        raise NotFoundError('Task not found.')

    for key, value in request_body.items():
        setattr(task, key, value)

    session.commit()

    return TaskSchema().dump(task).data


@requires_auth
def delete_task(task_id, user_id):
    """Delete a task"""
    query = Task.query.join(Board).filter(
        Task.id == task_id, Board.user_id == user_id)
    task = query.one_or_none()

    if not task:
        raise NotFoundError('Task not found.')

    session.delete(task)
    session.commit()

    return None, 200


@requires_auth
def get_boards(user_id):
    """Get boards"""
    boards = Board.query.filter(Board.user_id == user_id).all()
    return BoardSchema().dump(boards, many=True).data


@requires_auth
def create_board(request_body, user_id):
    """Create a board"""
    board = Board(**request_body, user_id=user_id)
    session.add(board)
    session.commit()

    return BoardSchema().dump(board).data


@requires_auth
def get_board(board_id, user_id):
    """Get a board"""
    query = Board.query.filter(Board.id == board_id, Board.user_id == user_id)
    query = query.options(joinedload(Board.tasks)).options(raiseload('*'))
    board = query.one_or_none()

    if not board:
        raise NotFoundError('Board not found.')

    return BoardDetailsSchema().dump(board).data


@requires_auth
def update_board(board_id, request_body, user_id):
    """Update a board"""
    query = Board.query.filter(Board.id == board_id, Board.user_id == user_id)
    board = query.one_or_none()

    if not board:
        raise NotFoundError('Board not found.')

    for key, value in request_body.items():
        setattr(board, key, value)

    session.commit()

    return BoardSchema().dump(board).data


@requires_auth
def delete_board(board_id, user_id):
    """Delete a board and its tasks"""
    query = Board.query.filter(Board.id == board_id, Board.user_id == user_id)
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
    demo_board_id = 1
    query = Board.query.filter(Board.id == demo_board_id)
    query = query.options(joinedload(Board.tasks)).options(raiseload('*'))
    board = query.one()

    return BoardDetailsSchema().dump(board).data
