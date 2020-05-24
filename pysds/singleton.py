# -*- coding: utf-8 -*-
import inspect


class Singleton(type):
    """Singleton Pattern

    Design assumptions:
    * Singleton constructor shall have no arguments or arguments with default values
    * Constructor shall identify dependencies with other singletons using their class reference
    """
    _instances = {}

    def __init__(cls, *args, **kwargs):
        if '__init__' in args[2]:
            # check the init signature and identify dependencies with other singletons
            argspec = inspect.getfullargspec(args[2]['__init__'])
            if len(argspec.args) > 1 and (argspec.defaults is None or len(argspec.defaults) != len(argspec.args)-1):
                raise Exception(f"{cls} does not have a valid init method")
        super(Singleton, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __repr__(self):
        return f"<Singleton({self.__name__})>"

    def destroy(self):
        if self in self._instances:
            del self._instances[self]

