import logging
import pathlib
import random
import string

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from data_center.models import DocumentStatus, ReportType

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'POPULATE CONFIG DATA'
    """
    This management command is useful for populating default config data necessary 
    for the application to function as expected
    """
    def handle(self, *args, **options):
        try:
            DocumentStatus.objects.get_or_create(name="UNPROCESSED")
            DocumentStatus.objects.get_or_create(name="PROCESSED")

            ReportType.objects.get_or_create(name="days_from_suspension_report")
            ReportType.objects.get_or_create(name="agent_collection_report")
            ReportType.objects.get_or_create(name="payment_type_report")
            ReportType.objects.get_or_create(name="all_reports")
            ReportType.objects.get_or_create(name="days_from_suspension_report_per_agent")
        except Exception as exception:
            print(exception.__str__())
