# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This is the interface for interacting with the GradePage Web Service.
"""

from uw_gradepage.models import GradingStatus
from uw_gradepage import get_resource
from urllib.parse import quote

GRADING_STATUS_URL = "/api/v1/grading_status/{section_id}"


def get_grading_status(section_id, act_as=None):
    """
    Return a restclients.models.gradepage.GradePageStatus object
    for the given course
    """
    url = GRADING_STATUS_URL.format(section_id=quote(section_id))
    headers = {}

    if act_as is not None:
        headers["X-UW-Act-as"] = act_as

    return GradingStatus.from_json(get_resource(url, headers))
