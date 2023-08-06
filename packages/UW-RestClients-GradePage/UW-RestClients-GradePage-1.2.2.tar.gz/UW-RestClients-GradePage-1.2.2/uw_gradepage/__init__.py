# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with the GradePage Web Service.
"""

from uw_gradepage.dao import GradePage_DAO
from restclients_core.exceptions import DataFailureException
import json

GradePageDao = GradePage_DAO()


def get_resource(url, headers={}):
    response = GradePageDao.getURL(url, headers)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    return json.loads(response.data)
