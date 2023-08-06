#
# Copyright (c) 2022, Gabriel Linder <linder.gabriel@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

from dataclasses import (
    asdict,
    dataclass,
    field,
    fields,
)
from typing import Any, Dict, Protocol


class DataClass(Protocol):
    __dataclass_fields__: Dict[str, Any]


def asdict_shallow(self: DataClass) -> Dict[str, Any]:
    # Returns a shallow dict from a dataclass.
    # Similar to but faster than asdict, which creates a deep copy.
    return {f.name: getattr(self, f.name) for f in fields(self)}


__all__ = (
    'DataClass',
    'asdict',
    'asdict_shallow',
    'dataclass',
    'field',
    'fields',
)
