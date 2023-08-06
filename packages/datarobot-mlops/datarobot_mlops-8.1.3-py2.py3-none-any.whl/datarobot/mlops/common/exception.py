from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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

import datarobot.mlops.install_aliases  # noqa: F401


class DRCommonException(Exception):
    pass


class DRConfigKeyNotFound(DRCommonException):
    pass


class DRConfigKeyAlreadyAssigned(DRCommonException):
    pass


class DRUnsupportedType(DRCommonException):
    pass


class DRAlreadyInitialized(DRCommonException):
    pass


class DRApiException(DRCommonException):
    pass


class DRSpoolerException(DRCommonException):
    pass


class DRNotFoundException(DRCommonException):
    pass
