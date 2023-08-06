# utesting-py

**GitHub:** https://github.com/s0urce18/utesting-py

**PyPi:** https://pypi.org/project/utesting/

Python module for unit testing

## Installation:

```console
pip install utesting
```

## Importing:

```py
from utesting import ResultState # not necessary
from utesting import ResultStates # not necessary
from utesting import Unit # not necessary
from utesting import TestCase # necessary (for creating test cases)
from utesting import TestGroup # not necessary
from utesting import TestCaseResult # not necessary
from utesting import Test # necessary (for additing and running testing)
```

## Using:

`test(group, output)` — test test group

`test_async(group, output)` — async version of test

`@mark_test_unit(cases, asynchronous, only_errors, only_time, no_print)` — decorator for marking test unit

`add_test_unit(callback, cases, asynchronous, only_errors, only_time, no_print)` — same as mark_test_unit, but can't be used as decorator

`test_all(file_name)` — running testing all marked(added) units

`test_all_asyc(file_name)` — async version of test_all

And other documentation in `utesting/__init__.py` and examples in `examples.py`
