from tp_interfaces.knowledge_base.interfaces import DisambiguationKB


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class KBManager(metaclass=_Singleton):
    def __init__(self):
        self._kb = None

    @property
    def knowledge_base(self) -> DisambiguationKB:
        if self._kb is None:
            raise AttributeError("Knowledge bae is not initialized")
        return self._kb

    @knowledge_base.setter
    def knowledge_base(self, kb: DisambiguationKB):
        if self._kb is not None:
            raise AttributeError("Knowledge base already initialized")
        self._kb = kb

    @knowledge_base.deleter
    def knowledge_base(self):
        self._kb = None
