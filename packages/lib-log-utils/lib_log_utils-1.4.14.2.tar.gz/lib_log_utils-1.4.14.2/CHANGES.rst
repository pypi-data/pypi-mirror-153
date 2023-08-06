Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes


v1.4.14.2
---------
2022-06-02: update to github actions checkout@v3 and setup-python@v3

v1.4.14
--------
2022-03-29: remedy mypy type error in lob_log_utils_cli

v1.4.13
---------
2022-03-25:
 - fix ValueError: underlying buffer has been detached on github Actions Windows
 - implement github actions
 - update documentation and tests
 - list ./dist dir if existing
 - fix requirements.txt

v1.4.10
---------
2020-10-09: service release
    - update travis build matrix for linux 3.9-dev
    - update travis build matrix (paths) for windows 3.9 / 3.10

v1.4.9
--------
2020-08-08: service release
    - fix documentation
    - fix travis
    - deprecate pycodestyle
    - implement flake8

v1.4.8
---------
2020-08-01: fix doctests in windows

v1.4.7
---------
2020-08-01: fix pypi deploy

v1.4.6
---------
2020-07-31: fix travis build

v0.4.5
---------
2020-07-29: fix environ.pop issue in doctest


v0.4.4
---------
2020-07-29: feature release
    - use the new pizzacutter template

v0.4.3
---------
2020-07-27: feature release
    - use cli_exit_tools
    - add banner parameter, to temporary disable/enable banner

v0.4.2
---------
2020-07-23: separate travis profile

v0.4.1
---------
2020-07-23: change color profiles

v0.4.0
---------
2020-07-23: feature release
    - correct print_exception_traceback is stdout, stderr = None
    - added formatting parameter, custom log formatter

v0.3.0
---------
2020-07-22: feature release
    - autodetect travis settings
    - autodetect binder/jupyter settings

v0.2.0
---------
2020-07-22: feature release
    - log_exception_traceback and print_exception_traceback will also report stdout, stderr if present


v0.1.4
---------
2020-07-17: feature release
    - bump coverage

v0.1.3
---------
2020-07-17: feature release
    - comprehensive *--colortest*
    - automatically select 8 colors profile for travis

v0.1.2
---------
2020-07-16: feature release
    - store settings in environment for commandline use
    - cleanup
    - release on pypi
    - fix cli test
    - enable traceback option on cli errors
    - jupyter notebook

v0.1.1
---------
2020-07-06: patch release
    - new click cli
    - use PizzaCutter Template

v0.0.2
---------
development

v0.0.1
---------
2019-09-03: Initial public release
