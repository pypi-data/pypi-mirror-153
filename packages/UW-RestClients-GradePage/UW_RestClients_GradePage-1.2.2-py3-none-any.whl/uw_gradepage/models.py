# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core import models
from dateutil.parser import parse
from commonconf import settings


class GradingStatus(models.Model):
    section_id = models.CharField(max_length=256)
    grading_period_open = models.NullBooleanField(default=False)
    no_grades_submitted = models.NullBooleanField(default=True)
    grading_status = models.CharField(max_length=64)
    display_name = models.CharField(max_length=64)
    section_url = models.CharField(max_length=256)
    status_url = models.CharField(max_length=256)
    submitted_count = models.PositiveSmallIntegerField(null=True)
    unsubmitted_count = models.PositiveSmallIntegerField(null=True)
    submitted_by = models.CharField(max_length=128, null=True)
    submitted_date = models.DateTimeField(blank=True, null=True)
    accepted_date = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def from_json(data):
        status = GradingStatus()
        gs_data = data.get('grading_status')
        status.section_id = gs_data['section_id']
        status.grading_period_open = gs_data['grading_period_open']
        status.display_name = gs_data['display_name']
        status.status_url = gs_data['status_url']
        status.grading_status = gs_data['grading_status']

        status.section_url = gs_data['section_url']
        if status.section_url:
            # Add the host to this URL for displayed links
            status.section_url = (
                getattr(settings, 'RESTCLIENTS_GRADEPAGE_HOST', '') +
                status.section_url)

        try:
            status.submitted_count = gs_data['submitted_count']
            status.unsubmitted_count = gs_data['unsubmitted_count']
            status.submitted_by = gs_data['submitted_by']
            status.submitted_date = parse(gs_data["submitted_date"])
            status.accepted_date = parse(gs_data["accepted_date"])
            status.no_grades_submitted = False
        except (TypeError, KeyError):
            status.no_grades_submitted = True
        return status

    def json_data(self):
        return {
            'section_id': self.section_id,
            'grading_period_open': self.grading_period_open,
            'no_grades_submitted': self.no_grades_submitted,
            'grading_status': self.grading_status,
            'display_name': self.display_name,
            'section_url': self.section_url,
            'status_url': self.status_url,
            'submitted_count': self.submitted_count,
            'unsubmitted_count': self.unsubmitted_count,
            'submitted_by': self.submitted_by,
            'submitted_date': (str(self.submitted_date)
                               if self.submitted_date else None),
            'accepted_date': (str(self.accepted_date)
                              if self.accepted_date else None),
        }
