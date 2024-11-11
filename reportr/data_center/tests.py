import csv
import os
import random
import shutil
import string
from datetime import datetime
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from data_center.management.commands.populateconfigdata import Command as populateconfigdata_command
from data_center.models import ReportType, DocumentStatus, Report, PaymentDocument, Agent, Payment

from data_center.services.report_services import ConstantStrings, days_from_suspension_report, ReportTypes
from data_center.services.sync_payment_doc_agents import sync_payment_doc_agents
from data_center.services.sync_payment_doc_payments import sync_payment_doc_payments


# Create your tests here.
class PopulateConfigSystemDataTest(TestCase):
    def test_populateconfigdata(self):
        print("Method: test_populateconfigdata.")
        populateconfigdata_command().handle()

        self.assertTrue(DocumentStatus.objects.get(name="UNPROCESSED"), 'UNPROCESSED instance exists in "DocumentStatus" model')
        self.assertTrue(DocumentStatus.objects.get(name="PROCESSED"), 'PROCESSED instance exists in "DocumentStatus" model')
        self.assertTrue(ReportType.objects.get(name="days_from_suspension_report"), 'days_from_suspension_report instance exists in "ReportType" model')
        self.assertTrue(ReportType.objects.get(name="agent_collection_report"), 'agent_collection_report instance exists in "ReportType" model')
        self.assertTrue(ReportType.objects.get(name="payment_type_report"), 'payment_type_report instance exists in "ReportType" model')
        self.assertTrue(ReportType.objects.get(name="all_reports"), 'all_reports instance exists in "ReportType" model')


class SyncPaymentDocTest(TestCase):
    def setUp(self):
        print("setUp: SyncPaymentDocTest.")
        populateconfigdata_command().handle()
        test_file_original_path = '../Test Files/2024_09_10_payments.csv'
        self.test_file_destination_path = './media/documents/2024_09_10_payments.csv'
        datetime_now = datetime.now().strftime(ConstantStrings.strftime_format)

        if not os.path.exists(self.test_file_destination_path):
            shutil.copy(src=test_file_original_path, dst=self.test_file_destination_path)
        self.assertTrue(os.path.isfile(self.test_file_destination_path), f'payments_document test file {os.path.basename(self.test_file_destination_path)} exists in documents folder')

        self.payment_document, payment_document_created = PaymentDocument.objects.get_or_create(
            name=datetime_now,
            process_status=DocumentStatus.objects.get(name="UNPROCESSED")
        )
        self.assertTrue(payment_document_created, 'payments_document model instance is created successfully')

        self.payment_document.file = File(open(self.test_file_destination_path))
        self.payment_document.save()
        self.assertTrue(os.path.isfile(self.payment_document.file.path), f'payments_document file field has valid file')

    def test_sync_payment_doc_agents(self):
        """
        Test the sync_payment_doc_agents function.

        This test method verifies that the sync_payment_doc_agents function correctly inserts the expected number
        of agents into the Agent model from the payments document.

        The method calls sync_payment_doc_agents with a document ID, retrieves all Agent objects, and checks if
        the number of agents inserted matches the expected number.

        :return: None
        """
        print("Method: test_sync_payment_doc_agents.")
        sync_payment_doc_agents(1)
        agents = Agent.objects.filter()
        expected_number_of_agents = 2
        self.assertEqual(len(list(agents)), expected_number_of_agents,
                         "expected number of agents inserted from payments doc to agents model")

    def test_sync_payment_doc_payments(self):
        """
        Test the sync_payment_doc_payments function.

        This test method verifies that the sync_payment_doc_payments function correctly inserts the expected number
        of payments into the Payment model from the payments document.

        The method calls sync_payment_doc_payments with a document ID, retrieves all Payment objects, and checks if
        the number of payments inserted matches the expected number.

        :return: None
        """
        print("Method: test_sync_payment_doc_payments.")
        sync_payment_doc_payments(1)
        payments = Payment.objects.filter()
        expected_number_of_payments = 4
        self.assertEqual(len(list(payments)), expected_number_of_payments,
                         "expected number of payments inserted from payments doc to payments model")

    def tearDown(self):
        print("tearDown: SyncPaymentDocTest.")
        os.remove(self.test_file_destination_path)
        self.assertFalse(os.path.exists(self.test_file_destination_path),
                         f'Test file {os.path.basename(self.test_file_destination_path)} has been deleted')

        shutil.rmtree(os.path.dirname(self.payment_document.file.path))
        self.assertFalse(os.path.exists(self.payment_document.file.path),
                         f'payment_document test file {os.path.basename(self.payment_document.file.path)} has been deleted')


class ReportServicesTest(TestCase):
    def setUp(self):
        print("setUp: ReportServicesTest.")
        populateconfigdata_command().handle()

        test_file_original_path = '../Test Files/2024_09_10_payments.csv'
        self.test_file_destination_path = './media/documents/2024_09_10_payments.csv'
        datetime_now = datetime.now().strftime(ConstantStrings.strftime_format)

        if not os.path.exists(self.test_file_destination_path):
            shutil.copy(src=test_file_original_path, dst=self.test_file_destination_path)

        self.payment_document, payment_document_created = PaymentDocument.objects.get_or_create(
            name=datetime_now,
            process_status=DocumentStatus.objects.get(name="UNPROCESSED")
        )

        self.payment_document.file = File(open(self.test_file_destination_path))
        self.payment_document.save()

        sync_payment_doc_agents(1)
        sync_payment_doc_payments(1)

        datetime_now = datetime.now().strftime(ConstantStrings.strftime_format)
        report_1, report_created = Report.objects.get_or_create(
            name=datetime_now,
            report_type=ReportType.objects.get(name=ReportTypes.days_from_suspension_report),
            payments_document=self.payment_document
        )
        self.assertTrue(report_created,
                        'report model instance is created successfully')

    def test_days_from_suspension_report(self):
        """
        Test the days_from_suspension_report function.

        This test method checks if the report file is created successfully and if the number of successful payments in the report is as expected.

        The test method first calls the days_from_suspension_report function to create the report file.
        Then, it asserts if the report file is created successfully by checking if the file exists.
        Finally, the test method asserts if the number of successful payments in the report is as expected by comparing the expected number of successful payments with the actual number of successful payments.

        :return: None
        """
        print("Method: test_days_from_suspension_report.")
        self.days_from_suspension_doc_path = days_from_suspension_report(1)
        self.assertTrue(os.path.isfile(self.days_from_suspension_doc_path),
                        f'days_from_suspension_report file {os.path.basename(self.days_from_suspension_doc_path)} successfully created')
        expected_successful_payments = 3
        actual_successful_payments = 0

        with open(self.days_from_suspension_doc_path, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for idx, line in enumerate(reader):
                if idx > 0:
                    # count actual records excluding heading
                    actual_successful_payments = actual_successful_payments + 1
        self.assertEqual(expected_successful_payments, actual_successful_payments,
                         'expected number of successful payments equals actual number of successful payments')

    def tearDown(self):
        print("tearDown: ReportServicesTest.")
        shutil.rmtree(os.path.dirname(self.days_from_suspension_doc_path))
        self.assertFalse(os.path.exists(self.days_from_suspension_doc_path),
                         f'Test file {os.path.basename(self.days_from_suspension_doc_path)} has been deleted')

        shutil.rmtree(os.path.dirname(self.payment_document.file.path))
        self.assertFalse(os.path.exists(self.payment_document.file.path),
                         f'payment_document test file {os.path.basename(self.payment_document.file.path)} has been deleted')
