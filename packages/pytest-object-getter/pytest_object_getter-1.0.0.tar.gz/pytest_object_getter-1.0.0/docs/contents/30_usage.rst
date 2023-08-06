=====
Usage
=====

------------
Installation
------------

| **pytest_object_getter** is available on PyPI hence you can use `pip` to install it.

It is recommended to perform the installation in an isolated `python virtual environment` (env).
You can create and activate an `env` using any tool of your preference (ie `virtualenv`, `venv`, `pyenv`).

Assuming you have 'activated' a `python virtual environment`:

.. code-block:: shell

  python -m pip install pytest-object-getter


---------------
Simple Use Case
---------------

| Common Use Case for the pytest_object_getter is to use the 'get_obejct' fixture
| to mock an object in your python test case (using pytest).

Let's see a test that mocks the `requests.get` method to avoid
actual network communication:

Install Python dependencies:

.. code-block:: shell

    python3 -m pip install ask-pypi

Test case:

.. code-block:: python

    import pytest

    @pytest.fixture
    def mock_response():
        def init(self, package_name: str):
            self.status_code = 200 if package_name == 'existing-package' else 404
        return type('MockResponse', (), {
            '__init__': init
        })

    @pytest.fixture
    def create_mock_requests(mock_response):
        def _create_mock_requests():
            def mock_get(*args, **kwargs):
                package_name = args[0].split('/')[-1]
                return mock_response(package_name)
            return type('MockRequests', (), {
                'get': mock_get,
            })
        return _create_mock_requests

    def test_fixture(get_object, create_mock_requests):

        from ask_pypi import is_pypi_project

        assert is_pypi_project('numpy') == True
        assert is_pypi_project('pandas') == True
        assert is_pypi_project('existing-package') == False

        get_object('is_project', 'ask_pypi.pypi_project',
            overrides={'requests': lambda: create_mock_requests()})

        assert is_pypi_project('existing-package') == True

        assert is_pypi_project('numpy') == False
        assert is_pypi_project('pandas') == False
        assert is_pypi_project('so-magic') == False
