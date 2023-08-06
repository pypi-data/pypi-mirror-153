from pydantic import validator, Field
from typing import List, Tuple, Union

from openmodule.models.base import OpenModuleModel


class Replacement(OpenModuleModel):
    c_from: str = Field(alias="from")
    c_to: str = Field(alias="to")

    @validator("c_from")
    def c_from_is_uppercase(cls, v):
        return v.upper()

    @validator("c_to")
    def c_to_is_uppercase(cls, v):
        return v.upper()


class Charset(OpenModuleModel):
    replacements: List[Replacement] = []
    allowed: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖ_"

    @validator("allowed")
    def allowed_is_uppercase(cls, v):
        return v.upper()


class CharsetConverter:
    def __init__(self, charset: Charset):
        self.replacements = charset.replacements
        self.allowed_chars = charset.allowed

    def _replace(self, text):
        for replacement in self.replacements:
            text = text.replace(replacement.c_from, replacement.c_to)
        return text

    def _remove_unknown(self, text):
        return "".join(x for x in text if x in self.allowed_chars)

    def clean(self, text):
        return self._remove_unknown(self._replace(text.upper()))


def _build_charset(allowed: str, replacements: Union[List, Tuple]) -> Charset:
    return Charset(
        allowed=allowed,
        replacements=({"from": f, "to": t} for f, t in replacements)
    )


legacy_lpr_charset = _build_charset(
    allowed="0123456789abcdefghijklmnprstuvwxyz",
    replacements=(("Ä", "A"), ("Ü", "U"), ("Ö", "O"), ("O", "0"), ("Q", "0"))
)

full_lpr_charset = _build_charset(
    allowed="0123456789ABCDEFGHIJKLMNOQPRSTUVWXYZÄÜÖ",
    replacements=((" ", ""), ("-", ""), (".", ""))
)
