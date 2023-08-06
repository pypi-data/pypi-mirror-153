# copyright 2003-2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.
"""CubicWeb web client core. You'll need a apache-modpython or twisted
publisher to get a full CubicWeb web application
"""

from logging import getLogger

from logilab.common.deprecation import callable_moved

from cubicweb import _
from cubicweb._exceptions import (
    Forbidden,
    Unauthorized,
    ValidationError,
)
from cubicweb.utils import json_dumps
from cubicweb.web._exceptions import (
    DirectResponse,
    InvalidSession,
    LogOut,
    NotFound,
    NothingToEdit,
    ProcessFormError,
    PublishException,
    Redirect,
    RemoteCallFailed,
    RequestError,
    StatusResponse,
)

assert json_dumps is not None, "no json module installed"

json_dumps = callable_moved("cubicweb.utils", "json_dumps")
eid_param = callable_moved("cubicweb.uilib", "eid_param")

INTERNAL_FIELD_VALUE = "__cubicweb_internal_field__"


class stdmsgs:
    """standard ui message (in a class for bw compat)"""

    BUTTON_OK = (_("button_ok"), "OK_ICON")
    BUTTON_APPLY = (_("button_apply"), "APPLY_ICON")
    BUTTON_CANCEL = (_("button_cancel"), "CANCEL_ICON")
    BUTTON_DELETE = (_("button_delete"), "TRASH_ICON")
    YES = (_("yes"), None)
    NO = (_("no"), None)


LOGGER = getLogger("cubicweb.web")

# XXX deprecated
FACETTES = set()


def jsonize(function):
    def newfunc(*args, **kwargs):
        value = function(*args, **kwargs)
        try:
            return json_dumps(value)
        except TypeError:
            return json_dumps(repr(value))

    return newfunc


__all__ = [
    "DirectResponse",
    "Forbidden",
    "InvalidSession",
    "LogOut",
    "NotFound",
    "NothingToEdit",
    "ProcessFormError",
    "PublishException",
    "Redirect",
    "RemoteCallFailed",
    "RequestError",
    "StatusResponse",
    "Unauthorized",
    "ValidationError",
    "jsonize",
    "LOGGER",
    "INTERNAL_FIELD_VALUE",
    "stdmsgs",
]
