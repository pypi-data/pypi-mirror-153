# todo_app

Started following a tutorial from real-python.


After the end of the tutorial , I will contribute major changes to the project.


I added time of creation of tasks. 
Modified most of the fields and working procedures of those code.

Instalation:
  -- 

Usages: 

    -- At first need to apply init for initializing:
            $ python3 -m todo init

    -- To add a task:
            $ python3 -m todo add 
            or 
            $ python3 -m add [--description/-d] <Description> [--priority/-p] <Priority>
    
    -- To see lists of Tasks:
	    $ python3 -m todo list

    -- To see all the tasks (Including Done tasks):
	    $ python3 -m todo list -a

    -- To Update a task:
	    $ python3 -m todo update
	    or 
	    $ python3 -m todo update [--id] <Task ID> [--status/-s] <Status> [--priority/-p] <Priority>
    
    -- To remove a task:
	    $ python3 -m todo remove <Task ID> [--force/-f]

    -- To clear all tasks:
	    $ python3 -m todo  clear

    -- For Any commands , you can always type --help

 
