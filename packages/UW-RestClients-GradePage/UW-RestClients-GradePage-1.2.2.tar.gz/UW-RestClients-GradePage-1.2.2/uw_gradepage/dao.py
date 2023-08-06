# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Contains UW GradePage DAO implementations.
"""
from restclients_core.dao import DAO
from os.path import abspath, dirname
import os


class GradePage_DAO(DAO):
    def service_name(self):
        return 'gradepage'

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "resources"))]
        return path
