from .exception import DetailedException

def make_tree(module_dict, **kwargs):
    for name, exception_injector in kwargs.items():
        exception_injector(name, DetailedException, module_dict)

def exception(*args, **kwargs):
    """
        Registers an exception. To be used inside of a `make_tree` call. All arguments
        will be treated as detail labels for the generated exception and all keyword
        arguments must be calls to this function to register the child exceptions.

        The return value can be chained with a call to `.set(**kwargs)` that passes the
        given keyword arguments to the class argument list of the product exception.

        For examples see the `make_tree` documentation.
    """

    def exception_injector(name, parent, module_dict):
        class product_exception(parent, details=args, **exception_injector._kwargs):
            pass

        module_name = module_dict["__name__"]
        product_exception.__name__ = name
        product_exception.__qualname__ = name
        product_exception.__module__ = module_name
        product_exception.__doc__ = f"{name} exception"
        module_dict[name] = product_exception

        for name, child_injector in kwargs.items():
            child_injector(name, product_exception, module_dict)

    exception_injector._kwargs = {}

    def set(**kwargs):
        exception_injector._kwargs.update(kwargs)
        return exception_injector

    exception_injector.set = set

    return exception_injector
