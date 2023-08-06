#!/usr/bin/env python3

from logilab.common.configuration import REQUIRED

options = (
    (
        "a-required-string-option",
        {
            "type": "string",
            "default": REQUIRED,
            "help": "",
            "group": "test",
            "level": 1,
        },
    ),
    (
        "a-required-int-option",
        {
            "type": "int",
            "default": REQUIRED,
            "help": "",
            "group": "test",
        },
    ),
    (
        "a-required-yn-option",
        {
            "type": "yn",
            "default": REQUIRED,
            "help": "",
            "group": "test",
        },
    ),
)
