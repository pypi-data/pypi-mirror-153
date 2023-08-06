#  Copyright (c) 2019 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2022.
#
#  DataRobot, Inc. Confidential.
#  This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.
#  The copyright notice above does not evidence any actual or intended publication of
#  such source code.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datarobot.mlops.install_aliases  # noqa: F401
from decimal import Decimal
import os

import six


# Using a `default` argument can impact performance so we leave it on the responsibility of the
# caller to pass this function in to one of the `dumps` functions.
def default_serializer(obj):
    """
    Help serialize a few extra datatypes we commonly see, especially in Prediction Data payloads.
    """
    if isinstance(obj, Decimal):
        return float(obj)  # close enough approximation for our needs
    raise TypeError("Type %s not JSON serializable" % type(obj))


# Orjson is a Python 3 only library that has been measured to be much faster than all other
# JSON libraries. However, it is also **not** a drop-in replacement for the standard library
# so a shim is required until we can drop Python 2 support.
if six.PY2 or os.environ.get("MLOPS_DISABLE_FAST_JSON") == "1":
    from json import loads, dumps

    def json_dumps_str(obj, default=None):
        return dumps(obj, default=default)

    # to be compatible with orjson we need to encode str output as UTF-8 (bytes)
    def json_dumps_bytes(obj, default=None):
        return dumps(obj, default=default).encode("utf-8")
else:
    from orjson import loads, dumps

    def json_dumps_bytes(obj, default=None):
        return dumps(obj, default=default)

    # to be compatible with std-lib we need a version that returns a str
    def json_dumps_str(obj, default=None):
        return dumps(obj, default=default).decode("utf-8")


# For loading JSON, both libraries have similar enough APIs that we can use the same function
def json_loads(data):
    return loads(data)
