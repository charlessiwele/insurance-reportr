import os.path
from pathlib import Path
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
import shutil
from data_center.models import PaymentDocument, DocumentStatus, Report, GeneratedReport
from data_center.services.report_services import days_from_suspension_report, agent_collection_report, \
    payment_type_report, ReportTypes, days_from_suspension_report_per_agent
from data_center.services.sync_payment_doc_agents import sync_payment_doc_agents
from data_center.services.sync_payment_doc_payments import sync_payment_doc_payments
from django.contrib import messages


# Create your views here.
class SyncDocumentPaymentsView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        sync_payment_result = sync_payment_doc_payments(kwargs.get('document_id'))
        new_process_status = DocumentStatus.objects.get(name='PROCESSED')
        document = PaymentDocument.objects.get(pk=kwargs.get('document_id'))
        document.process_status = new_process_status
        document.save()
        messages.success(request, str(sync_payment_result) + " Payment Records Processed")
        redirect_to='/admin/data_center/paymentdocument/' + str(document.pk) + '/change/'
        return HttpResponseRedirect(redirect_to=redirect_to)


class SyncDocumentAgentsView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        sync_payment_result = sync_payment_doc_agents(kwargs.get('document_id'))
        new_process_status = DocumentStatus.objects.get(name='PROCESSED')
        document = PaymentDocument.objects.get(pk=kwargs.get('document_id'))
        document.process_status = new_process_status
        document.save()
        messages.success(request, str(sync_payment_result) + " Agent Records Processed")
        redirect_to='/admin/data_center/paymentdocument/' + str(document.pk) + '/change/'
        return HttpResponseRedirect(redirect_to=redirect_to)


class GenerateReportsView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        report = Report.objects.get(pk=kwargs.get('report_id'))
        result = {}
        report_path = ""
        if report.report_type.name == ReportTypes.days_from_suspension_report:
            report_path = days_from_suspension_report(kwargs.get('report_id'))
            file_reader = open(report_path, 'rb')
            generated_report = GeneratedReport.objects.get_or_create(
                name=os.path.basename(report_path),
                description='days to suspension report',
                file=File(file_reader, name=report.name + '_' + os.path.basename(report_path)),
                report=report
            )
            generated_reports = [generated_report]
            file_reader.close()
            os.remove(report_path)
        elif report.report_type.name == ReportTypes.days_from_suspension_report_per_agent:
            report_path = days_from_suspension_report_per_agent(kwargs.get('report_id'))
            file_reader = open(report_path, 'rb')
            generated_report = GeneratedReport.objects.get_or_create(
                name=os.path.basename(report_path),
                description='days to suspension report per agent',
                file=File(file_reader, name=report.name + '_' + os.path.basename(report_path)),
                report=report
            )
            file_reader.close()
            generated_reports = [generated_report]
            os.remove(report_path)
        elif report.report_type.name == ReportTypes.payment_type_report:
            report_path = payment_type_report(kwargs.get('report_id'))
            file_reader = open(report_path, 'rb')
            generated_report = GeneratedReport.objects.get_or_create(
                name=os.path.basename(report_path),
                description='payment type report',
                file=File(file_reader, name=report.name + '_' + os.path.basename(report_path)),
                report=report
            )
            file_reader.close()
            generated_reports = [generated_report]
            os.remove(report_path)
        elif report.report_type.name == ReportTypes.agent_collection_report:
            report_path = agent_collection_report(kwargs.get('report_id'))
            file_reader = open(report_path, 'rb')
            generated_report = GeneratedReport.objects.get_or_create(
                name=os.path.basename(report_path),
                description='agent collections report',
                file=File(file_reader, name=report.name + '_' + os.path.basename(report_path)),
                report=report
            )
            file_reader.close()
            generated_reports = [generated_report]
            os.remove(report_path)
        elif report.report_type.name == ReportTypes.all_reports:

            suspension_report_path = days_from_suspension_report(kwargs.get('report_id'))
            payment_type_report_path = payment_type_report(kwargs.get('report_id'))
            collection_report_path = agent_collection_report(kwargs.get('report_id'))

            suspension_report_reader = open(suspension_report_path, 'rb')
            payment_type_report_reader = open(payment_type_report_path, 'rb')
            collection_report_reader = open(collection_report_path, 'rb')

            generated_suspension_report = GeneratedReport.objects.get_or_create(
                name=os.path.basename(suspension_report_path),
                description='days to suspension report',
                file=File(suspension_report_reader, name=report.name + '_' + os.path.basename(suspension_report_path)),
                report=report
            )

            generated_agent_collections_report = GeneratedReport.objects.get_or_create(
                name=os.path.basename(collection_report_path),
                description='agent collections report',
                file=File(collection_report_reader, name=report.name + '_' + os.path.basename(collection_report_path)),
                report=report
            )

            generated_payment_type_report = GeneratedReport.objects.get_or_create(
                name=os.path.basename(payment_type_report_path),
                description='payment type report',
                file=File(payment_type_report_reader, name=report.name + '_' + os.path.basename(payment_type_report_path)),
                report=report
            )

            suspension_report_reader.close()
            payment_type_report_reader.close()
            collection_report_reader.close()

            generated_reports = [
                generated_suspension_report,
                generated_agent_collections_report,
                generated_payment_type_report
            ]

            os.remove(suspension_report_path)
            os.remove(payment_type_report_path)
            os.remove(collection_report_path)

        messages.info(request, "Completed Generating All Reports")
        redirect_to='/admin/data_center/report/' + str(report.pk) + '/change/'
        return HttpResponseRedirect(redirect_to=redirect_to)
