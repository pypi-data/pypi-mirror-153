# Provides code to connect the CLI with the to-do database

"""This module provides the RP To-Do model-controller."""
# todo/todo_.py

from typing import Any, Dict, NamedTuple
from pathlib import Path
from todo.database import DatabaseHandler
from typing import Any, Dict, List, NamedTuple
from todo import DB_READ_ERROR, ID_ERROR
import enum
from datetime import datetime


class Status(enum.Enum):
    ToDo= 0
    InProgress=1
    OnTest=2
    Done=3

class Priority(enum.Enum):
    Low = 1
    Medium = 2
    High = 3
    Urgent = 4
    Burning = 5

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    def add(self,description: List[str], priority: int = 2 ):

        """Add a new to-do to the database."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Status": Status.ToDo.value,
            "created_at": datetime.now().strftime("%d/%m/%y %H:%M"),
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_todos()
        return read.todo_list 

    def set_status(self, todo_id: int, status: int) -> CurrentTodo:

        """
            Set a task to status as done.
            task ->   ToDo = 0
                 ->   InProgress = 1
                 ->   OnTest = 2 
                 ->   Done = 3 
        """
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Status"] = status
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)


    def set_priority(self, todo_id: int, priority: int) -> CurrentTodo:

        """
            Set a updated priority to priority as done.
            Priority: 
                    ->  Low = 1
                    ->  Medium = 2
                    ->  High = 3
                    ->  Urgent = 4
                    ->  Burning = 5
        """
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Priority"] = priority
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentTodo:

        """Remove a to-do from the database using its id or index."""
        
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)

        return CurrentTodo(todo, write.error)

    def remove_all(self) -> CurrentTodo:

        """Remove all to-dos from the database."""

        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)