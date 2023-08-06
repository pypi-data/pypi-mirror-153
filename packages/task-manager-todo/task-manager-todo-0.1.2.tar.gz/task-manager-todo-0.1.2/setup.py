from setuptools import setup, find_packages
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name='task-manager-todo',
    version="0.1.2",
    license='MIT',
    author="Shipu",
    author_email='shipankar.shipu@gmail.com',
    packages=find_packages('todo'),
    package_dir={'': 'todo'},
     # Short description of your library
    description='A simple cli based task-manager app',
    long_description = long_description,
    long_description_context_type = 'text/markdown',
    url='https://github.com/Shipu12345/todo_app',
    keywords=["todo app", "task manager", "task", "jira like", "cli"],
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
],
    python_requires='>=3.8',

    install_requires=[
    
        'attrs==21.4.0',
        'click==7.1.2',
        'colorama==0.4.4',
        'iniconfig==1.1.1',
        'packaging==21.3',
        'pluggy==0.13.1',
        'py==1.11.0',
        'pyparsing==3.0.9',
        'shellingham==1.4.0',
        'toml==0.10.2',
        'typer==0.3.2',
        'pytest==6.2.4',

      ],
)