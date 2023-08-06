# Provides the Typer command-line interface for the application

"""
Enables CLI for the package
"""

from asyncio import tasks
from typing import Optional
import typer
from .__init__ import __app_name__, __version__
from pathlib import Path
from typing import Optional
import typer
from todo import ERRORS, __app_name__, __version__, config, database,  todo_
from todo.todo_ import Status, Priority
from typing import List, Optional

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)

def get_todoer() -> todo_.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return todo_.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
def printing_list(done, priority, desc, id , created_at):

    if done==0:
        font_color= typer.colors.BRIGHT_MAGENTA
    if done==1:
        font_color= typer.colors.YELLOW
    if priority==5 or priority==4:
        font_color=typer.colors.RED
    if done==2:
        font_color= typer.colors.BRIGHT_BLUE
    if done==3:
        font_color= typer.colors.GREEN
    typer.secho(
        f"{id}{ (5-len(str(id))) * ' '}"
        f"| ({Priority(priority).name}){ (11-len(str(Priority(priority).name))) * ' '}"
        f"| {Status(done).name}{(13-len(str(Status(done).name))) * ' '}"
        f"| {created_at} {(14-len(str(created_at))) * ' '}"
        f"| {desc}",
        fg=font_color,
    )


@app.command()
def add(description: List[str] = typer.Option(
        False,
        "--description",
        "-d",
        help="Details of the task",
    ),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=5),) -> None:

    """
    Add a new to-do with a DESCRIPTION:
        priority -->
                Low = 1
                Medium = 2
                High = 3
                Urgent = 4
                Burning = 5
    """
    if description:
        cli_add(description=description, priority=priority)
    else:
        typer.secho("""Adding A New Task:\n""", fg=typer.colors.GREEN)
        typer.secho("""Description: """ , fg=typer.colors.CYAN, nl=False, bold=True)

        
        description=input().split()
        typer.secho("""         Priority Can be =>
                                Low = 1        Medium = 2
                                High = 3       Urgent = 4
                                    Burning = 5\n """, fg=typer.colors.MAGENTA, nl=False)
        typer.secho("\nTask Priority: " , fg=typer.colors.CYAN, bold=True, nl=False)
        priority=int(input())
        cli_add(description=description, priority=priority)



@app.command("cli-add")
def cli_add(
    description: List[str] = typer.Argument(...), ##  When you pass an ellipsis (...) as the first argument to the constructor of Argument, you’re telling Typer that description is required. 
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=5),) -> None:

    """
    Add a new to-do with a DESCRIPTION:
        priority -->
                Low = 1
                Medium = 2
                High = 3
                Urgent = 4
                Burning = 5
    """

    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )
    list_all(is_all=False)


@app.command(name="list")
def list_all(is_all: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Show All Tasks",
    )) -> None:
    """List all to-dos."""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    
    if len(todo_list) == 0:
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Priority     ",
        "| Status       ",
        "| Created At     ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * (2*len(headers)), fg=typer.colors.BLUE)
    for id, todo in enumerate(todo_list, 1):
        desc, priority, done, created_at = todo.values()
        if not is_all :
            if done!=3:
                printing_list(desc=desc, priority=priority, done=done, id=id,  created_at=created_at)
        else:
            printing_list(desc=desc, priority=priority, done=done, id=id, created_at=created_at)
        
        
    typer.secho("-" * (2*len(headers)) + "\n", fg=typer.colors.BRIGHT_BLUE)



@app.command(name="update")
def set_updated_status(todo_id: int = typer.Option(
        0,
        "--id",
        help="Task ID..",
    ), 
    status: int = typer.Option(-1, "--status", "-s", min=-1, max=3),
    priority: int = typer.Option(-1, "--priority", "-p", min=-1, max=5)) -> None:
    print(ERRORS)
    """
    Update Status of a  todo by setting it as Status Numbers as Following:
    Update Status as: \n
                    ->   ToDo = 0 \n
                    ->   InProgress = 1 \n
                    ->   OnTest = 2 \n
                    ->   Done = 3 \n
    Update Priority as: \n
                    ->  Low = 1  \n
                    ->  Medium = 2  \n
                    ->  High = 3  \n
                    ->  Urgent = 4  \n
                    ->  Burning = 5  \n
    """

    if todo_id!=0:
        set_status(todo_id=todo_id, status=status, priority=priority)
    else:
        typer.secho("""Updating A Task:\n""", fg=typer.colors.GREEN)
        typer.secho("""\nTask ID: """, fg=typer.colors.CYAN, bold=True, nl=False)
        try:
            task_id = int(input())
        except:
            typer.secho(
                    f'Updating to-do # "{todo_id}" failed with "{ERRORS[6]}"\ncommand: todo list [-a] to see all the tasks',
            fg=typer.colors.RED,)
            raise typer.Exit(1)
            
        typer.secho("""         Priority Can be =>    (Keep empty if you do not want to change the priority)
                                Low = 1        Medium = 2
                                High = 3       Urgent = 4
                                    Burning = 5\n """, fg=typer.colors.MAGENTA, nl=False)
        typer.secho("""\nPriority: """, fg=typer.colors.CYAN, bold=True, nl=False)
        priority = input()
        if priority!='':
            priority=int(priority) 
        else:
            priority=-1
        typer.secho("""         Status Can be =>    (Keep empty if you do not want to change the Status)
                                ToDo = 0        InProgress = 1
                                OnTest = 2      Done = 3
                                    \n """, fg=typer.colors.MAGENTA, nl=False)
        typer.secho("""\nStatus: """, fg=typer.colors.CYAN, bold=True, nl=False)
        status=input()
        if status!='':
            status=int(status)
        else:
            status=-1
        print(f"{todo_id =: }{ priority =: }{ task_id =: }{ status =: }")
        if priority==-1 and status==-1:
            typer.secho("""\nNothing is updated,  please update with a valid Status or Priority.""", fg=typer.colors.MAGENTA, bold=True, nl=False)
            list_all(is_all=False)
        else:
            set_status(todo_id=task_id, status=status, priority=priority)



@app.command(name="cli-update")
def set_status(todo_id: int = typer.Argument(...), 
    status: int = typer.Option(-1, "--status", "-s", min=0, max=3),
    priority: int = typer.Option(-1, "--priority", "-p", min=1, max=5)) -> None:


    """
    Update Status of a  todo by setting it as Status Numbers as Following:
    Update Status as: \n
                    ->   ToDo = 0 \n
                    ->   InProgress = 1 \n
                    ->   OnTest = 2 \n
                    ->   Done = 3 \n
    Update Priority as: \n
                    ->  Low = 1  \n
                    ->  Medium = 2  \n
                    ->  High = 3  \n
                    ->  Urgent = 4  \n
                    ->  Burning = 5  \n
    """

    todoer = get_todoer()
    if status!=-1: 
        todo, error = todoer.set_status(todo_id,status)
    if priority!=-1:    
        todo, error = todoer.set_priority(todo_id,priority)
    if error:
        typer.secho(
            f'Updating to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do # {todo_id} "{todo['Description']}" Updated!""",
            fg=typer.colors.GREEN,
        )
    list_all(is_all=False)


@app.command()
def remove(
    todo_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation.",
    ),
) -> None:

    """Remove a to-do using its TODO_ID."""

    todoer = get_todoer()

    def _remove():
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'Removing to-do # {todo_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""to-do # {todo_id}: '{todo["Description"]}' was removed""",
                fg=typer.colors.GREEN,
            )

    if force:
        _remove()
    else:
        todo_list = todoer.get_todo_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho("Invalid TODO_ID", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete to-do # {todo_id}: {todo['Description']}?"
        )
        if delete:
            _remove()
        else:
            typer.echo("Operation canceled")
    list_all(is_all=False)
    


@app.command(name="clear")
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt="Delete all to-dos?",
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove all to-dos."""
    todoer = get_todoer()
    if force:
        error = todoer.remove_all().error
        if error:
            typer.secho(
                f'Removing to-dos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho("All to-dos were removed", fg=typer.colors.GREEN)
    else:
        typer.echo("Operation canceled")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()



@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


