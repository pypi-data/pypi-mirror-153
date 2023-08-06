# Decorator Manager
Decorator Manager is a Python module for decorating different functions, classes or methods.

## Usage
* timeit
```python
from rcd_dev_kit import decorator_manager

@decorator_manager.timeit(program_name="my func") # Any descriptive text for the func
def my_func():
    return "hello"
```

* debug
```python
from rcd_dev_kit import decorator_manager
@decorator_manager.debug
def my_func():
    return "hello"
```

## Roadmap
* add logging decorator.

## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
