import importlib
import logging
import os

from platon_hash.abc import (
    BackendAPI,
)
from platon_hash.backends import (
    SUPPORTED_BACKENDS,
)


def auto_choose_backend() -> BackendAPI:
    env_backend = get_backend_in_environment()

    if env_backend:
        return load_environment_backend(env_backend)
    else:
        return choose_available_backend()


def get_backend_in_environment() -> str:
    return os.environ.get('platon_hash_BACKEND', "")


def load_backend(backend_name: str) -> BackendAPI:
    import_path = 'platon_hash.backends.%s' % backend_name
    module = importlib.import_module(import_path)

    try:
        backend = module.backend  # type: ignore
    except AttributeError as e:
        raise ValueError(
            "Import of %s failed, because %r does not have 'backend' attribute" % (
                import_path,
                module,
            )
        ) from e

    if isinstance(backend, BackendAPI):
        return backend
    else:
        raise ValueError(
            "Import of %s failed, because %r is an invalid back end" % (
                import_path,
                backend,
            )
        )


def load_environment_backend(env_backend: str) -> BackendAPI:
    if env_backend in SUPPORTED_BACKENDS:
        try:
            return load_backend(env_backend)
        except ImportError as e:
            raise ImportError(
                "The backend specified in platon_hash_BACKEND, '{0}', is not installed. "
                "Install with `pip install platon-hash[{0}]`.".format(env_backend)
            ) from e
    else:
        raise ValueError(
            "The backend specified in platon_hash_BACKEND, %r, is not supported. "
            "Choose one of: %r" % (env_backend, SUPPORTED_BACKENDS)
        )


def choose_available_backend() -> BackendAPI:
    for backend in SUPPORTED_BACKENDS:
        try:
            return load_backend(backend)
        except ImportError:
            logging.getLogger('platon_hash').debug("Failed to import %s", backend, exc_info=True)
    raise ImportError(
        "None of these hashing backends are installed: %r.\n"
        "Install with `pip install platon-hash[%s]`." % (
            SUPPORTED_BACKENDS,
            SUPPORTED_BACKENDS[0],
        )
    )
