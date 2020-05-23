# -*- coding: utf-8 -*-


class Singleton(type):
    """Singleton Pattern

    Design assumptions:
    * Singleton constructor should have no argument or only optional ones
    * Singleton instantiation cannot fail
    * Dependencies with other singletons shall be defined in the init method
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def destroy(mcs):
        mcs._instances = {}
