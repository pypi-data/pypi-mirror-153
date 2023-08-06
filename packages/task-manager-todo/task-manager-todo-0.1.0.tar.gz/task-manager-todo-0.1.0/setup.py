from setuptools import setup, find_packages


setup(
    name='task-manager-todo',
    version="0.1.0",
    license='MIT',
    author="Shipu",
    author_email='shipankar.shipu@gmail.com',
    packages=find_packages('todo'),
    package_dir={'': 'todo'},
    url='https://github.com/Shipu12345/todo_app',
    keywords=["todo app", "task manager", "task", "jira like", "cli"],
    install_requires=[
        
        'python  >=3.8',
        'attrs == 21.4.0',
        'click == "7.1.2"',
        'colorama == "0.4.4"',
        'iniconfig == "1.1.1"',
        'packaging == "21.3"',
        'pluggy == "0.13.1"',
        'py == "1.11.0"',
        'pyparsing == "3.0.9"',
        'shellingham == "1.4.0"',
        'toml == "0.10.2"',
        'typer == "0.3.2"',
        'pytest == "6.2.4"',

      ],
)