# ez-task - simple python multiprocessing


ez-task wraps the standard Python multiprocessing library to simplify the management and usage of multiple long-running processes.
ez-task is designed for low-latency applications.

## Installation
 > `pip3 install --no-deps ez-task`

# Usage


## Using TaskManager
```
from ez_task.manager import TaskManager
import time

def foo():
    time.sleep(1)
    return 'Foo Call'

def bar(text):
    time.sleep(2)
    return text

def baz(text, key = 'key'):
    time.sleep(3)
    return f'{text} {key}'

with TaskManager() as manager:
    foo_task, bar_task, baz_task = manager.define_task_set(foo, bar, baz)

    # Execute tasks concurrently
    foo_task.run()
    bar_task.run('bar')
    baz_task.run('baz', key='booz')

    # Sychronously block for output
    print('foo task:', foo_task.get_result()) # foo task: foo task Foo

    print('bar task:', bar_task.get_result()) # bar task: bar

    print('baz task:', baz_task.get_result()) # baz task: baz booz

    # Total time taken is 3 seconds

 ```
 









