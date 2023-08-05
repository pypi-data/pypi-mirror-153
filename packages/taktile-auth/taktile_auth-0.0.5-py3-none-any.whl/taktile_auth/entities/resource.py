from __future__ import annotations

import re
import typing as t

import pydantic

from taktile_auth.enums import Wildcard

PARTIAL_RE = re.compile(r"(^[^\*]*$)|(^[^\*]*\*$)")


def is_full_wildcard(v: str) -> str:
    assert v == "*" or "*" not in v
    return v


def is_partial_wildcard(v: str) -> str:
    assert re.fullmatch(PARTIAL_RE, v)
    return v


def is_full_specified(v: str) -> str:
    assert "*" not in v
    return v


WILDCARD_CHECK = {
    Wildcard.allowed: is_full_wildcard,
    Wildcard.partial: is_partial_wildcard,
    Wildcard.not_allowed: is_full_specified,
}


class Resource(pydantic.BaseModel):
    def __contains__(self, o: Resource) -> bool:
        """Checks if the queried resource 'o' is either equal
        or contained inside of 'self'.
        For each arg of the resource, checks if it is either a
        match with query's corresponding arg (including wildcards).
        """

        if self.schema()["title"] != o.schema()["title"]:
            return False

        for arg in self.dict().keys():
            allowed = getattr(self, arg)
            queried = getattr(o, arg)
            if not re.fullmatch(allowed.replace("*", ".*"), queried):
                return False
        return True

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))


class ResourceDefinition(pydantic.BaseModel):
    resource_name: str
    args: t.Dict[str, Wildcard]

    def get_resource(self) -> t.Type[Resource]:
        fields: t.Any = {
            field_name: (str, ...) for field_name in self.args.keys()
        }
        validators = {
            f"{field_name}_validator": (
                pydantic.validator(field_name, allow_reuse=True)(
                    WILDCARD_CHECK[check]
                )
            )
            for field_name, check in self.args.items()
        }
        return t.cast(
            t.Type[Resource],
            pydantic.create_model(
                self.resource_name,
                **fields,
                __validators__=validators,
                __base__=Resource,
            ),
        )
