from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Optional, Union

from pydantic import ValidationError
from sgqlc.types import Input
from tdm.datamodel.fact.value import ValueType

from talisman_api.adapters.schemas.api_schema import DateTimeIntervalInput, DateTimeValueInput, DoubleValueInput, \
    GeoPointInput, GeoPointWithNameFormInput, IntValueInput, IntervalDouble, IntervalInt, LinkValueInput, StringFilter, \
    StringLocaleValueInput, StringValueInput, ValueInput
from tp_interfaces.abstract import ImmutableBaseModel


class BaseValueTypes(Enum):
    STRING = "String"
    DATE = "Date"
    INT = "Int"
    DOUBLE = "Double"
    GEO = "Geo"
    STRING_LOCALE = "StringLocale"
    LINK = 'Link'


class AbstractGQLMapper(metaclass=ABCMeta):
    @property
    @abstractmethod
    def filter_name(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_value_input(self, value: ValueType) -> ValueInput:
        pass

    @abstractmethod
    def get_value_filter(self, value: ValueType) -> Union[Input, str]:
        pass

    @abstractmethod
    def _get_value(self, value: ValueType) -> ImmutableBaseModel:
        pass

    def check_value(self, value: ValueType) -> bool:
        try:
            self._get_value(value)
            return True
        except ValidationError:
            return False


class Locale(Enum):
    en = 'en'
    ru = 'ru'
    other = 'other'


class StringLocaleValue(ImmutableBaseModel):
    value: str
    locale: Locale

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class StringLocaleGQLMapper(AbstractGQLMapper):
    @property
    def filter_name(self) -> str:
        raise NotImplementedError

    def get_value_input(self, value: ValueType) -> ValueInput:
        value = self._get_value(value)
        string_locale_input = StringLocaleValueInput()
        string_locale_input.value = value.value
        string_locale_input.locale = value.locale

        value_input = ValueInput()
        value_input.string_locale_value_input = string_locale_input
        return value_input

    def get_value_filter(self, value: ValueType) -> str:
        return self._get_value(value).value

    def _get_value(self, value: ValueType) -> StringLocaleValue:
        return StringLocaleValue(**value)


class StringValue(ImmutableBaseModel):
    value: str


class StringGQLMapper(AbstractGQLMapper):
    @property
    def filter_name(self) -> str:
        return 'string_filter'

    def get_value_input(self, value: ValueType) -> ValueInput:
        value = self._get_value(value)
        string_input = StringValueInput()
        string_input.value = value.value

        value_input = ValueInput()
        value_input.string_value_input = string_input
        return value_input

    def get_value_filter(self, value: ValueType) -> StringFilter:
        value = self._get_value(value)
        string_filter = StringFilter()
        string_filter.str = value.value

        return string_filter

    def _get_value(self, value: ValueType) -> StringValue:
        return StringValue(**value)


class IntValue(ImmutableBaseModel):
    value: int


class IntGQLMapper(AbstractGQLMapper):
    @property
    def filter_name(self) -> str:
        return 'int_filter'

    def get_value_input(self, value: ValueType) -> ValueInput:
        value = self._get_value(value)
        int_input = IntValueInput()
        int_input.value = value.value

        value_input = ValueInput()
        value_input.int_value_input = int_input
        return value_input

    def get_value_filter(self, value: ValueType) -> IntervalInt:
        value = self._get_value(value)
        int_value = IntervalInt()
        int_value.start = value.value
        int_value.end = value.value
        return int_value

    def _get_value(self, value: ValueType) -> IntValue:
        return IntValue(**value)


class DoubleValue(ImmutableBaseModel):
    value: float


class DoubleGQLMapper(AbstractGQLMapper):
    @property
    def filter_name(self) -> str:
        return 'double_filter'

    def get_value_input(self, value: ValueType) -> ValueInput:
        value = self._get_value(value)
        double_input = DoubleValueInput()
        double_input.value = value.value

        value_input = ValueInput()
        value_input.double_value_input = double_input
        return value_input

    def get_value_filter(self, value: ValueType) -> IntervalDouble:
        value = self._get_value(value)
        double_value = IntervalDouble()
        double_value.start = value.value
        double_value.end = value.value
        return double_value

    def _get_value(self, value: ValueType) -> DoubleValue:
        return DoubleValue(**value)


class DateValue(ImmutableBaseModel):
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]


class TimeValue(ImmutableBaseModel):
    hour: int
    minute: int
    second: int


class DateTimeValue(ImmutableBaseModel):
    date: DateValue
    time: Optional[TimeValue]


class DateGQLMapper(AbstractGQLMapper):
    @property
    def filter_name(self) -> str:
        return 'date_time_filter'

    def get_value_input(self, value: ValueType) -> ValueInput:
        value = self._get_value(value)
        date_input = DateTimeValueInput(value.dict(exclude_none=True))

        value_input = ValueInput()
        value_input.date_time_value_input = date_input
        return value_input

    def get_value_filter(self, value: ValueType) -> DateTimeIntervalInput:
        value = self._get_value(value)
        date_input = DateTimeValueInput(value.dict(exclude_none=True))

        date_value = DateTimeIntervalInput()
        date_value.start = date_input
        date_value.end = date_input
        return date_value

    def _get_value(self, value: ValueType) -> DateTimeValue:
        return DateTimeValue(**value)


class CoordinateValue(ImmutableBaseModel):
    latitude: float
    longitude: float


class GeoValue(ImmutableBaseModel):
    point: Optional[CoordinateValue]
    name: Optional[str]


class GeoGQLMapper(AbstractGQLMapper):
    @property
    def filter_name(self) -> str:
        return 'geo_filter'

    def get_value_input(self, value: ValueType) -> ValueInput:
        value = self._get_value(value)
        geo_input = GeoPointInput(value.dict(exclude_none=True))

        value_input = ValueInput()
        value_input.geo_point_value_input = geo_input
        return value_input

    def get_value_filter(self, value: ValueType) -> GeoPointWithNameFormInput:
        value = self._get_value(value)
        geo_value = GeoPointWithNameFormInput(value.dict(exclude_none=True))
        geo_value.radius = 0.0001
        return geo_value

    def _get_value(self, value: ValueType) -> GeoValue:
        return GeoValue(**value)


class LinkValue(ImmutableBaseModel):
    link: str


class LinkGQLMapper(AbstractGQLMapper):
    @property
    def filter_name(self) -> Optional[str]:
        raise None

    def get_value_input(self, value: ValueType) -> ValueInput:
        value = self._get_value(value)
        link_input = LinkValueInput()
        link_input.link = value.link

        value_input = ValueInput()
        value_input.link_value_input = link_input
        return value_input

    def get_value_filter(self, value: ValueType) -> Union[Input, str]:
        raise NotImplementedError

    def _get_value(self, value: ValueType) -> LinkValue:
        return LinkValue(**value)


def get_map_helper(base_value: BaseValueTypes) -> AbstractGQLMapper:
    if base_value is BaseValueTypes.STRING:
        return StringGQLMapper()
    if base_value is BaseValueTypes.STRING_LOCALE:
        return StringLocaleGQLMapper()
    if base_value is BaseValueTypes.INT:
        return IntGQLMapper()
    if base_value is BaseValueTypes.DOUBLE:
        return DoubleGQLMapper()
    if base_value is BaseValueTypes.DATE:
        return DateGQLMapper()
    if base_value is BaseValueTypes.GEO:
        return GeoGQLMapper()
    if base_value is BaseValueTypes.LINK:
        return LinkGQLMapper()
