[![Coverage Status](https://coveralls.io/repos/github/i386x/vutils-testing/badge.svg?branch=main)](https://coveralls.io/github/i386x/vutils-testing?branch=main)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/i386x/vutils-testing.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/i386x/vutils-testing/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/i386x/vutils-testing.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/i386x/vutils-testing/context:python)

# vutils-testing: Auxiliary Library for Writing Tests

This package provides a set of tools that help with writing tests. It helps
with creating test data and types, mocking objects, patching, and verifying
test results.

## Installation

To install the package, type
```sh
$ pip install vutils-testing
```

## How to Use

For more details, please follow the subsections below.

### Type Factories

Sometimes tests require new types to be defined. To do this,
`vutils.testing.utils` provides `make_type` function, which is a wrapper of
`type`:
```python
# Create type derived directly from object:
my_type = make_type("MyType")

# Create class derived directly from Exception:
my_error = make_type("MyError", Exception)

# Create class derived from A and B:
my_class = make_type("MyClass", (A, B))

# Create class derived from A with foo member:
my_another_class = make_type("MyAnotherClass", A, {"foo": 42})

# Create class derived from object with foo member:
my_test_class = make_type("MyTestClass", members={"foo": 42})

# Key-value arguments other than bases and members are passed to
# __init_subclass__:
my_fourth_class = make_type("MyFourthClass", bases=A, foo=42)
```

### Mocking Objects and Patching

`make_mock`, `make_callable`, and `PatcherFactory` from `vutils.testing.mock`
allow to create mock objects and patching things.

`make_mock(*args, **kwargs)` is a shortcut for `unittest.mock.Mock`

`make_callable(x)` creates also instance of `unittest.mock.Mock`, but it
specifies its function-related behavior: if `x` is callable, it is used to do a
side-effect, otherwise it is used as the return value.
```python
# func_a() returns 3
func_a = make_callable(3)

container = []

# func_b() appends 42 to container
func_b = make_callable(lambda *x, **y: container.append(42))

# func_c() returns func_b
func_c = make_callable(lambda *x, **y: func_b)
```

`PatcherFactory` allows to use `unittest.mock.patch` multiple-times without
need of nested `with` statements. When instantiated, `setup` method is called.
`setup` method, implemented in the subclass, then may define set of patcher
specifications via `add_spec` method:
```python
class MyPatcher(PatcherFactory):

    @staticmethod
    def setup_foo(mock):
        mock.foo = "foo"

    @staticmethod
    def setup_baz(baz):
        baz["quux"] = 42

    def setup(self):
        self.baz = {}
        # When self.patch() is called:
        # - create a mock object, apply setup_foo on it, and patch foopkg.foo
        #   with it:
        self.add_spec("foopkg.foo", self.setup_foo)
        # - patch foopkg.bar with 42:
        self.add_spec("foopkg.bar", new=42)
        # - apply setup_baz on baz and patch foopkg.baz with it (create=True
        #   and other possible key-value arguments are passed to
        #   unittest.mock.patch):
        self.add_spec("foopkg.baz", self.setup_baz, new=self.baz, create=True)

patcher = MyPatcher()

with patcher.patch():
   # Patches are applied in order as specified by add_spec and reverted in
   # reverse order.
   do_something()
```

### Covering `mypy` Specific Code

When a module contains code that is visible only to `mypy`, it is not executed
during unit tests and hence reported as not covered. Function `cover_typing`
from `vutils.testing.utils` module has the ability to execute such a code and
therefore improve coverage reports:
```python
# In foopkg/foo.py module:
if typing.TYPE_CHECKING:
    from foopkg import _A, _B, _C

# In test_coverage.py:
import pytest

from vutils.testing.utils import cover_typing

# Ensure the test run as last (this feature is available after installing
# pytest-order). cover_typing reloads the module which may have negative
# consequences on other tests
@pytest.mark.order("last")
def test_typing_code_is_covered():
    # When called, following happens:
    # - typing.TYPE_CHECKING is patched to True
    # - foopkg is patched with _A, _B, and _C symbols if they do not exist
    # - finally, foopkg.foo is reloaded
    cover_typing("foopkg.foo", ["_A", "_B", "_C"])
```
The story behind `cover_typing` is to keep source files clean from directives
telling the `pytest` and linters what to do.

### Deferred Instance Initialization

Patching may take no effect if the patched object appears in constructor and
this constructor is called outside of patcher context. `LazyInstance` from
`vutils.testing.utils` can defer initialization up to the time of method call:
```python
class StderrWriter:
    def __init__(self):
        self.stream = sys.stderr

    def write(self, text):
        self.stream.write(text)

class StderrPatcher(PatcherFactory):
    def setup(self):
        self.stream = io.StringIO
        self.add_spec("sys.stderr", new=self.stream)

class MyTestCase(TestCase):
    def test_deferred_initialization(self):
        writerA = StderrWriter()
        writerB = LazyInstance(StderrWriter).create()
        patcher = StderrPatcher()

        # Patch sys.stderr:
        with patcher.patch():
            # Write Hello! to standard error output:
            writerA.write("Hello!\n")
            # Write Hi! to StringIO instance:
            writerB.write("Hi!\n")
```

### Deferred `assertRaises`

Sometimes there are callable objects with a very similar prototypes and
behavior so they can be run and checked with one universal function. However,
if one of them raises an exception under specific circumstances, this must be
also handled by the universal function, which adds to its complexity. For this
reason, `vutils.testing.utils` introduces `AssertRaises` class which wraps
exception raising assertions:
```python
class FooError(Exception):
    detail = "foo"

def func_a(obj):
    obj.foo = 42

def func_b(obj):
    func_a(obj)
    raise FooError()

def Foo(TestCase):
    def run_and_check(self, func):
        obj = make_mock()
        func(obj)
        self.assertEqual(obj.foo, 42)

    def test_func(self):
        wfunc_b = AssertRaises(self, func_b, FooError)

        self.run_and_check(func_a)
        # Catch and store FooError:
        self.run_and_check(wfunc_b)
        # Check the caught exception:
        self.assertEqual(wfunc_b.get_exception().detail, "foo")
```

### Enhanced `TestCase`

Module `vutils.testing.testcase` provides `TestCase` which is a subclass of
`unittest.TestCase` extended about these methods:

* `assert_called_with` - assert that the mock object has been called once with
  the specified arguments and then reset it:
  ```python
  class ExampleTestCase(TestCase):
      def test_assert_called_with(self):
          mock = make_mock(["foo"])

          mock.foo(1, 2, bar=3)
          self.assert_called_with(mock, 1, 2, bar=3)

          mock.foo(4)
          self.assert_called_with(mock, 4)
  ```
* `assert_not_called` - assert that the mock object has not been called:
  ```python
  class ExampleTestCase(TestCase):
      def test_assert_not_called(self):
          mock = make_mock(["foo"])

          self.assert_not_called(mock.foo)
  ```
