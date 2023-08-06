# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from datetime import datetime
from dateutil.tz import tzutc
from commonconf import override_settings
from uw_gradepage.grading_status import get_grading_status


@override_settings(RESTCLIENTS_GRADEPAGE_HOST='https://gradepage.test.edu')
class TestGradingStatus(TestCase):
    def test_get_grading_status_submitted(self):
        gs = get_grading_status(
            '2013-spring-A A-123-AA-FBB38FE46A7C11D5A4AE0004AC494FFE',
            act_as="bill")
        self.assertEqual(gs.no_grades_submitted, False)
        self.assertEqual(
            gs.section_id,
            '2013-spring-A A-123-AA-FBB38FE46A7C11D5A4AE0004AC494FFE')
        self.assertEqual(gs.display_name, 'A A 123 AA')
        self.assertEqual(gs.grading_status, None)
        self.assertEqual(gs.submitted_date,
                         datetime(2013, 6, 6, 21, 42, 19, tzinfo=tzutc()))
        self.assertEqual(gs.accepted_date,
                         datetime(2013, 6, 6, 21, 42, 20, tzinfo=tzutc()))
        self.assertEqual(gs.section_url, (
            'https://gradepage.test.edu/section/2013-spring-A%20A-123-AA-'
            'FBB38FE46A7C11D5A4AE0004AC494FFE'))

    def test_get_grading_status_not_submitted(self):
        gs = get_grading_status(
            '2013-spring-TRAIN-100-A-FBB38FE46A7C11D5A4AE0004AC494FFE',
            act_as="bill")
        self.assertEqual(gs.no_grades_submitted, True)
        self.assertEqual(
            gs.section_id,
            '2013-spring-TRAIN-100-A-FBB38FE46A7C11D5A4AE0004AC494FFE')
        self.assertEqual(gs.display_name, 'TRAIN 100 A')
        self.assertEqual(gs.grading_status,
                         'No submission information available')
        self.assertEqual(gs.section_url, (
            'https://gradepage.test.edu/section/2013-spring-TRAIN-100-A-'
            'FBB38FE46A7C11D5A4AE0004AC494FFE'))

    def test_get_grading_status_not_accepted(self):
        # Case where grades were submitted, but accepted date is null
        gs = get_grading_status(
            '2013-spring-TRAIN-200-A-FBB38FE46A7C11D5A4AE0004AC494FFE',
            act_as="bill")
        self.assertEqual(gs.no_grades_submitted, True)
