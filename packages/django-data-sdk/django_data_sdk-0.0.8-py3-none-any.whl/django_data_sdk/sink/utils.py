import importlib


def get_backend_instance(fullpath: str, backend_kwargs):
    module, name = fullpath.rsplit(".", 1)
    module_obj = importlib.import_module(module)
    backend_cls = getattr(module_obj, name)
    return backend_cls(backend_kwargs)
