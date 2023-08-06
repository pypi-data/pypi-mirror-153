"""Dynamic library core."""
import inspect


class DynamicLibrary:
    """
    Dynamic library core inspired by SeleniumLibrary for Robot Framework.

    You can create dynamic libraries by inheriting this class.

    Example usage:

    .. code-block:: python

        from tos.task_object_storage import TaskObjectStorage
        from module import another_module

        class TOSLibrary(DynamicLibrary):

            def __init__(self):
                super(TOSLibrary, self).__init__()
                tos = TaskObjectStorage()

                self.add_component(self)
                self.add_component(tos)
                self.add_component(another_module)

    """

    # TODO:
    # In the future it might be sensible to use PythonLibCore:
    # https://github.com/robotframework/PythonLibCore

    def __init__(self):
        self.keywords = {}

    def add_component(self, component):
        """Add external (class) methods to the library.

        This registers an arbitrary collection of functions as keywords
        callable from Robot Framework.

        :param component: class, instance, or module that contains functions
                          or methods (callables).
        """
        for name in dir(component):
            func = getattr(component, name)
            # FIXME: consider using @keyword decorator in TaskObjectStorage
            if not callable(func) or name.startswith("_") or name == "tos":
                continue  # pragma: no cover
                # (The above line doesn't show up in coverage
                # correctly even though it's executed)
            self.keywords[name] = func

    def get_keyword_names(self):
        """Robot Framework dynamic API keyword collector.

        :returns: all keywords registered for the library.
        :rtype: list
        """
        return sorted(self.keywords)

    def run_keyword(self, name, args, kwargs):
        """Call the keyword method by name.

        :param name: Name of the keyword.
        :param args: args passed from Robot Framework (can be empty).
        :param kwargs: kwargs passed from Robot Framework (can be empty).
        :returns: call to a registered keyword by name.
        """
        print(f"Running keyword {name}")
        return self.keywords[name](*args, **kwargs)

    def __getattr__(self, name):
        """Expose the dynamically added keywords as class attributes."""
        if name in self.keywords:
            return self.keywords[name]
        raise AttributeError(
            f"{type(self).__name__} object has no attribute {name}"
        )

    def __dir__(self):
        """Expose the dynamically added keywords as class attributes."""
        my_attrs = super().__dir__()
        return sorted(set(my_attrs) | set(self.keywords))

    # The below methods mainly help with robot.libdoc
    # TODO: they should be reviewed and refactored as needed

    def get_keyword_arguments(self, name):
        kw = self.keywords[name] if name != "__init__" else self.__init__
        args, defaults, varargs, kwargs = self._get_arg_spec(kw)
        args += ['{}={}'.format(name, value) for name, value in defaults]
        if varargs:
            args.append(f"*{varargs}")
        if kwargs:
            args.append(f"**{kwargs}")

        return args

    def _get_arg_spec(self, kw):
        spec = inspect.getfullargspec(kw)
        keywords = spec.varkw
        args = spec.args[1:] if inspect.ismethod(kw) else spec.args  # drop self
        defaults = spec.defaults or ()
        nargs = len(args) - len(defaults)
        mandatory = args[:nargs]
        defaults = zip(args[nargs:], defaults)

        return mandatory, defaults, spec.varargs, keywords

    def get_keyword_documentation(self, name):
        if name == '__init__':
            return inspect.getdoc(self.__init__) or ''
        kw = self.keywords[name]
        doc = inspect.getdoc(kw) or ''

        return doc
