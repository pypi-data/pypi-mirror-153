# pylint: disable=redefined-outer-name
import pytest


@pytest.fixture
def attribute_getter():
    from typing import Any

    class AttributeGetter(object):
        def __init__(self, debug_message_factory):
            self.debug_message_factory = debug_message_factory

        def __call__(self, object_ref: Any, attribute: str) -> Any:
            object_reference = getattr(object_ref, attribute)
            if object_reference is None:
                raise RuntimeError(self.debug_message_factory(object_ref, attribute))
            return object_reference

    return AttributeGetter


@pytest.fixture
def generic_object_getter_class(attribute_getter, monkeypatch):
    """Class instances can extract a requested object from within a module and optionally patch any object in the module's namespace at runtime."""
    from importlib import import_module
    from typing import Any, Generic, TypeVar

    T = TypeVar('T')

    class AbstractGenericObjectGetter(Generic[T]):
        def __init__(self, debug_message=None):
            self._get_object_callback = {
                True: self._get_production_object,
                False: self._build_object,
            }
            if debug_message:
                self._attr_getter = attribute_getter(
                    lambda _object, name: "{msg}. Did not find {name} on object of type {type}".format(
                        msg=debug_message, name=name, type=type(_object).__name__
                    )
                )
            else:
                self._attr_getter = attribute_getter(
                    lambda _object, name: "Did not find {name} on object of type {type}".format(
                        name=name, type=type(_object).__name__
                    )
                )

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            return self.get(*args, **kwargs)

        def get(self, request: T, overrides={}):
            d = {'overrides': overrides}
            use_production_object: bool = not bool(d.get('overrides'))
            return self._get_object_callback[use_production_object](request, **d)

        def _get_production_object(self, request: T, **kwargs):
            object_module = self._get_object_module(request)
            computed_object = self._get_object(request, object_module)
            return computed_object

        def _build_object(self, request: T, overrides={}):
            object_module = self._get_object_module(request)
            for symbol_name, factory in overrides.items():
                monkeypatch.setattr(object_module, symbol_name, factory())
            computed_object = self._get_object(request, object_module)
            return computed_object

        def _get_object_module(self, request: T):
            return import_module(self._extract_module_string(request))

        def _extract_module_string(self, request: T) -> str:
            """Extract the module 'path' from the request as dot (.) separated words (module/subpackages names)."""
            raise NotImplementedError

        def _extract_object_symbol_name(self, request: T) -> str:
            """Extract the name of the reference (symbol in code) that points to the object requested for getting at runtime."""
            raise NotImplementedError

        def _get_object(self, request: T, object_module):
            return self._attr_getter(object_module, self._extract_object_symbol_name(request))

    return AbstractGenericObjectGetter


@pytest.fixture
def object_getter_class(generic_object_getter_class):
    """Do a dynamic import of a module and get an object from its namespace.

    This fixture returns a Python Class that can do a dynamic import of a module
    and get an object from its namespace.

    Instances of this class are callable's (they implement the __call__ protocol
    ) and uppon calling the return a reference to the object "fetched" from the
    namespace.

    Callable instances arguments:
    * 1st: object with the 'symbol_namel': str and 'object_module_string': str
        attributes expected "on it"

    Returns:
        ObjectGetter: Class that can do a dynamic import and get an object
    """
    from abc import ABC, abstractmethod

    class RequestLike(ABC):
        @property
        @abstractmethod
        def symbol_name(self) -> str:
            # how the object (ie a get_job method) is imported into the namespace of a module (ie a metadata_provider module)
            raise NotImplementedError

        @property
        @abstractmethod
        def object_module_string(self) -> str:
            # the module (in a \w+\.\w+\.\w+ kind of format) where the object reference is present/computed
            raise NotImplementedError

    class ObjectGetter(generic_object_getter_class[RequestLike]):
        def _extract_module_string(self, request) -> str:
            return request.object_module_string

        def _extract_object_symbol_name(self, request) -> str:
            return request.symbol_name

    return ObjectGetter


@pytest.fixture
def get_object(object_getter_class):
    """Import an object from a module and optionally mock any object in its namespace.

    A callable that can import an object, given a reference (str), from a module
    , given its "path" (string represented as 'dotted' modules: same way python
    code imports modules), and provide the capability to monkeypatch/mock any
    object found in the module's namespace at runtime.

    The client code must supply the first 2 arguments at runtime, correspoding
    to the object's symbol name (str) and module "path" (str).

    The client code can optionally use the 'overrides' kwarg to supply a python
    dictionary to specify what runtime objects to mock and how.

    Each dictionary entry should model your intention to monkeypatch one of the
    module namespace' objects with a custom 'mock' value.

    Each dictionary key should be a string corresponding to an object's
    reference name (present in the module's namespace) and each value should be
    a callable that can construct the 'mock' value.
    The callable should take no arguments and acts as a "factory", that when
    called should provide the 'mock' value.

    Example:

        def mocked_request_get()
        business_method = get_object(
            "business_method",
            "business_package.methods",
            overrides={"production": lambda: 'mocked'}
        )

    Args:
        symbol (str): the object's reference name
        module (str): the module 'path' represented as module names "joined" by
            "." (dots)
        overrides (dict, optional): declare what to monkeypatch and with what "mocks". Defaults to None.

    Returns:
        Any: the object imported from the module with its namespace potentially mocked
    """

    class ObjectGetterAdapter(object_getter_class):
        """Adapter Class of the ObjectGetter class, see object_getter_class fixture.

        Returns:
            ObjectGetterAdapter: the Adapter Class
        """

        def __call__(self, symbol_ref: str, module: str, **kwargs):
            return super().__call__(
                type(
                    "RequestLike",
                    (),
                    {"symbol_name": symbol_ref, "object_module_string": module},
                ),
                **kwargs,
            )

    return ObjectGetterAdapter()
