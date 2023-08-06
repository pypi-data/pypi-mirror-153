def test_fixture(testdir):
    testdir.makepyfile(
        """
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

        _ = get_object('is_project', 'ask_pypi.pypi_project',
            overrides={'requests': lambda: create_mock_requests()})

        assert is_pypi_project('existing-package') == True

        assert is_pypi_project('numpy') == False
        assert is_pypi_project('pandas') == False
        assert is_pypi_project('so-magic') == False

    """
    )
    result = testdir.runpytest("--verbose")
    result.stdout.fnmatch_lines("test_fixture.py::test_fixture PASSED*")
