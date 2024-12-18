import typing
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, validator, ValidationError
from pydantic.dataclasses import dataclass as pydataclass

Unit = typing.Union[str, int]


class AddressType(str, Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    OTHER = "other"


print()
print("=" * 25 + " Address Class " + "=" * 25)


class Address:
    def __init__(self, street: str, number: int, unit: Unit):
        self.street = street
        self.number = number
        self.unit = unit

    def __repr__(self):
        return f"ADDRESS: {self.street} {self.number}, {self.unit}"


Address("Piccadilly Lane", 1304, "B")
Address("Main Street", 1017, 12)
try:
    print(Address("my street", 123, 1.76))
except Exception as e:
    print(e)

print()
print("=" * 25 + " Address DataClass " + "=" * 25)


@dataclass
class AddressDataclass:
    street: str
    number: int
    unit: Unit
    type: AddressType = AddressType.HOUSE


print(AddressDataclass(street="main st", number=123, unit="a"))
try:
    print(AddressDataclass(street="main st", number=123, unit="a", type="condo"))
except Exception as e:
    print(e)

print()
print("=" * 25 + " Pydantic Address Class " + "=" * 25)


class AddressPydantic(BaseModel):
    street: str
    number: int
    unit: Unit
    type: AddressType = AddressType.HOUSE

    @validator("unit")
    def unit_must_be_alphanumeric(cls, v: Unit):
        if isinstance(v, int):
            return v
        if not v.isalnum():
            raise ValueError("must be alphanumeric")
        return v


print(AddressPydantic(street="main st", number=123, unit="a"))
try:
    print(AddressPydantic(street="main st", number=123, unit="a", type="condo"))
except ValidationError as e:
    print(e)

try:
    print(AddressPydantic(street="main st", number=123, unit="*/&!", type="condo"))
except ValueError as e:
    print(e)

print()
print("=" * 25 + " Address Pydantic DataClass " + "=" * 25)


@pydataclass
class AddressPydanticDataclass:
    street: str
    number: int
    unit: Unit
    type: AddressType = AddressType.HOUSE


print(AddressPydanticDataclass(street="main st", number=123, unit="a"))
try:
    print(AddressPydanticDataclass(street="main st", number=123, unit="a", type="condo"))
except Exception as e:
    print(e)
