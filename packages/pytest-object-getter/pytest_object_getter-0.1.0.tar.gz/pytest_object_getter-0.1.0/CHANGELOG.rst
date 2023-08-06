=========
Changelog
=========

0.1.0 (2022-06-02)
==================

First `Pytest Object Getter` release!

We provide the *get_object* pytest fixture!

Changes
^^^^^^^

feature
"""""""
- provide fixtures featuring mocking capabilities

documentation
"""""""""""""
- document features and usage

build
"""""
- add mypy dependency in 'typing' extras


0.0.1 (2022-06-01)
=======================================

| This is the first ever release of the **pytest_object_getter** Python Package.
| The package is open source and is part of the **Pytest Object Getter** Project.
| The project is hosted in a public repository on github at https://github.com/boromir674/pytest-object-getter
| The project was scaffolded using the `Cookiecutter Python Package`_ (cookiecutter) Template at https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

| Scaffolding included:

- **CI Pipeline** running on Github Actions at https://github.com/boromir674/pytest-object-getter/actions
  - `Test Workflow` running a multi-factor **Build Matrix** spanning different `platform`'s and `python version`'s
    1. Platforms: `ubuntu-latest`, `macos-latest`
    2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`

- Automated **Test Suite** with parallel Test execution across multiple cpus.
  - Code Coverage
- **Automation** in a 'make' like fashion, using **tox**
  - Seamless `Lint`, `Type Check`, `Build` and `Deploy` *operations*


.. LINKS

.. _Cookiecutter Python Package: https://python-package-generator.readthedocs.io/en/master/
