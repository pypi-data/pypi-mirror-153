import time
import functools
from datetime import timedelta


def timeit(program_name=None):
    def _timeit(func):
        """Print the runtime of the decorated function"""

        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start = time.perf_counter()
            value = func(*args, **kwargs)
            end = time.perf_counter()
            run_time = str(timedelta(seconds=end - start))
            text = program_name if program_name else func.__name__
            print(f"✅{text!r} end in {run_time} s.⏰")
            return value

        return wrapper_timer
    return _timeit
