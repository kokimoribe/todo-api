"""Script to reset tables and insert demo data"""
#!/usr/bin/env python
import string
import sys

from todo.models import Board, Task
from todo.database import session, drop_tables, create_tables
from todo.constants import TO_DO, IN_PROGRESS, DONE


def main():
    drop_tables()
    create_tables()

    board = Board(name='Demo Board')
    session.add(board)
    session.commit()

    for i in range(6):
        board.task_number += 1
        title = 'Example task {}'.format(string.ascii_uppercase[i])
        description = 'Description of {}'.format(title)

        if i in [0, 1, 2]:
            status = TO_DO
        elif i in [3, 4]:
            status = IN_PROGRESS
        else:
            status = DONE

        task = Task(
            number=board.task_number,
            title=title,
            description=description,
            board_id=board.id,
            status=status)
        session.add(task)
    session.commit()

    return 0


if __name__ == '__main__':
    sys.exit(main())
