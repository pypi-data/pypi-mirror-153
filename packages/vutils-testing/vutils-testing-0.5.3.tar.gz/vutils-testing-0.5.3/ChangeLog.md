# Change Log

## 0.5.3

* Fix PEP 585 issue
* Remove deprecated `pylint` warnings from `pyproject.toml`
* Run tests with `cover_typing` as last

## 0.5.2

* Fixed typo in class name in `README.md`
* Switch to Python 3.10+ typing notation
* Drop Python 3.6, add Python 3.10

## 0.5.1

* Fixed key-value arguments loss when `PatchSpec` instance is called more than
  once

## 0.5.0

* New class `LazyInstance`

## 0.4.0

* New class `AssertRaises`

## 0.3.0

* `make_mock` now passes its arguments to `unittest.mock.Mock`
* New method `TestCase.assert_not_called`

## 0.2.0

* Added functions
  * `cover_typing`
  * `make_callable`
  * `make_mock`
  * `make_type`
* Added classes
  * `PatcherFactory`

## 0.1.0

* Initial development version
