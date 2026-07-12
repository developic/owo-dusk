# This file is part of owo-dusk.
#
# Copyright (c) 2024-present EchoQuill
#
# Portions of this file are based on code by EchoQuill, licensed under the
# GNU General Public License v3.0 (GPL-3.0).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.


def convert_list_items(li: list, item_type: type) -> list:
    new_li = []
    for i, item in enumerate(li):
        try:
            new_li.append(item_type(item))
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Item at index {i} ({item!r}) is not convertible to {item_type.__name__}: {e}"
            ) from e
    return new_li


def expected_fetch(item: dict, key: str, type_exp: type, elem_type: type | None = None):
    if key not in item:
        raise KeyError(f"Missing required key: {key!r}\n{item}")

    value = item[key]

    try:
        if type_exp is list and elem_type is not None:
            return convert_list_items(li=value, item_type=elem_type)
        return type_exp(value)
    except (TypeError, ValueError) as e:
        raise TypeError(
            f"Key {key!r}: expected type convertible to {type_exp.__name__}, "
            f"got {value!r} ({type(value).__name__}): {e}"
        ) from e
