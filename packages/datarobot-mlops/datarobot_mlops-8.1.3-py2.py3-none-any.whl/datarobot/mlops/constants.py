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

# WARNING: This file must never import any 3rd party modules because it is used in setup.py.


class Constants(object):
    """
    Various constants related to MLOps
    """

    OFFICIAL_NAME = "datarobot-mlops"
    MLOPS_VERSION = "8.1.3"

    # Constants used to upload actuals
    ACTUALS_ASSOCIATION_ID_KEY = "associationId"
    ACTUALS_WAS_ACTED_ON_KEY = "wasActedOn"
    ACTUALS_TIMESTAMP_KEY = "timestamp"
    ACTUALS_VALUE_KEY = "actualValue"
