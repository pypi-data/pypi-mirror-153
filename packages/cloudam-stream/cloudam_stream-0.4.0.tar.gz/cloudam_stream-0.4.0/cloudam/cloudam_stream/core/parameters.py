from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class Parameter(Generic[T]):

    def __init__(self,
                 name: Optional[str] = None,
                 required: bool = False,
                 default: [T, list[T]] = None,
                 description: Optional[str] = "",
                 hidden: bool = False,
                 level: str = "basic",
                 many: bool = False,
                 null: bool = False,
                 promoted: bool = False,
                 title: Optional[str] = None,
                 order: Optional[int] = None
                 ):
        self._name = name
        self._required = required
        self._default = default
        self._description = description
        self._hidden = hidden
        self._level = level
        self._many = many
        self._null = null
        self._promoted = promoted
        self._title = title
        self._order = order
        self._clazz = self.__class__.__name__

    def serialize(self):
        pass

    def deserialize(self):
        pass

    def get_args(self):
        return self.__dict__


class StringParameter(Parameter[Optional[str]]):

    def __init__(self, max_length: int = 1000, **kwargs):
        self._max_length = max_length
        super(StringParameter, self).__init__(**kwargs)


class FileInputParameter(StringParameter):

    pass


class FileOutputParameter(StringParameter):

    pass


class NumberParameter(Parameter[T]):

    def __init__(self,
                 min_value: T = None,
                 max_value: T = None,
                 **kwargs):
        self._min_value = min_value
        self._max_value = max_value
        super(NumberParameter, self).__init__(**kwargs)


class IntParameter(NumberParameter[Optional[int]]):

    pass


class FloatParameter(NumberParameter[Optional[float]]):

    pass


class BooleanParameter(Parameter[Optional[bool]]):

    pass


class JsonParameter(Parameter[Optional[dict]]):

    pass


class TupleParameter(Parameter[Optional[tuple]]):

    pass

