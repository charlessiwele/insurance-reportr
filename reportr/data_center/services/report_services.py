import csv
import os
import datetime
import sqlite3
from data_center.models import Payment, PaymentDocument, Report
from reportr.settings import DATABASES, MEDIA_ROOT
import shutil


def days_from_suspension_report(report_pk):
    report = Report.objects.get(pk=report_pk)
    payments_document = PaymentDocument.objects.get(pk=report.payments_document.pk)
    payments_document_name_parts = os.path.basename(payments_document.file.path).split('_')
    report_date = datetime.date(int(payments_document_name_parts[0]),
                                int(payments_document_name_parts[1]),
                                int(payments_document_name_parts[2]))

    select_statement = f"SELECT id, device_id, " \
                       f"strftime('%Y-%m-%d', payment_created) AS payment_created," \
                       f"strftime('%Y-%m-%d', '{report_date}') AS report_date, " \
                       f"90 - (JULIANDAY(strftime('%Y-%m-%d', '{report_date}')) - " \
                       f"JULIANDAY(strftime('%Y-%m-%d', payment_created))) AS days_to_client_suspension " \
                       f'FROM data_center_payment ' \
                       f"where payments_document_id = {report.payments_document.pk} " \
                       f'AND payment_status = "SUCCESSFUL"' \
                       f'order by days_to_client_suspension DESC;'

    clients_suspension_report_records = Payment.objects.raw(select_statement)
    report_files_path = os.path.join(MEDIA_ROOT, report.name)
    os.makedirs(report_files_path, exist_ok=True)
    suspension_report_document_path = os.path.join(report_files_path, 'clients_suspension_report.csv')
    with open(suspension_report_document_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['device_id', 'days_to_client_suspension'])
        for record in clients_suspension_report_records:
            writer.writerow([record.device_id, record.days_to_client_suspension])
    return suspension_report_document_path


def days_from_suspension_report_per_agent(report_pk):
    report = Report.objects.get(pk=report_pk)
    payments_document = PaymentDocument.objects.get(pk=report.payments_document.pk)
    payments_document_name_parts = os.path.basename(payments_document.file.path).split('_')
    report_date = datetime.date(int(payments_document_name_parts[0]),
                                int(payments_document_name_parts[1]),
                                int(payments_document_name_parts[2]))

    select_statement = f"SELECT id, device_id, agent_id, " \
                       f"strftime('%Y-%m-%d', payment_created) AS payment_created," \
                       f"strftime('%Y-%m-%d', '{report_date}') AS report_date, " \
                       f"90 - (JULIANDAY(strftime('%Y-%m-%d', '{report_date}')) - " \
                       f"JULIANDAY(strftime('%Y-%m-%d', payment_created))) AS days_to_client_suspension " \
                       f'FROM data_center_payment ' \
                       f"where payments_document_id = {report.payments_document.pk} " \
                       f'AND payment_status = "SUCCESSFUL"' \
                       f'order by days_to_client_suspension DESC;'

    clients_suspension_report_records = Payment.objects.raw(select_statement)
    report_zip_files_path = os.path.join(MEDIA_ROOT, report.name, 'zip_files')
    os.makedirs(report_zip_files_path, exist_ok=True)
    agent_reports = {}
    for record in clients_suspension_report_records:
        if not agent_reports.get(record.agent_id):
            agent_reports[str(record.agent_id)] = []

        agent_reports[str(record.agent_id)].append({
                'agent_id': record.agent_id, 
                'device_id': record.device_id, 
                'days_to_client_suspension': record.days_to_client_suspension
            })
    for agent in agent_reports:
        suspension_report_document_path = os.path.join(report_zip_files_path, f'clients_suspension_report_agent_{agent}.csv')
        print('writing to ', suspension_report_document_path)
        with open(suspension_report_document_path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(['device_id', 'agent_id', 'days_to_client_suspension'])

            for agent_record in agent_reports[agent]:
                writer.writerow([agent_record.get('device_id'), agent_record.get('agent_id'), agent_record.get('days_to_client_suspension')])

    print('archiving/zipping to ', suspension_report_document_path)
    suspension_report_archive_path = os.path.join(report_zip_files_path, f"suspension_reports")
    output_path = shutil.make_archive(suspension_report_archive_path, 'zip', os.path.join(report_zip_files_path))

    for agent in agent_reports:
        suspension_report_document_path = os.path.join(report_zip_files_path, f'clients_suspension_report_agent_{agent}.csv')
        print('suspension_report_document_path', suspension_report_document_path)
        suspension_report_document_path
        os.remove(suspension_report_document_path)

    return output_path


def agent_collection_report(report_pk, db_config=None):
    report = Report.objects.get(pk=report_pk)
    select_statement = f"SELECT agent_id, strftime('%Y-%m-%d', payment_created) AS payment_day, payment_type, " \
                       f"SUM(payment_amount) AS total_payment_amount FROM data_center_payment " \
                       f"where payments_document_id = {report.payments_document.pk} " \
                       f'AND payment_status = "SUCCESSFUL"' \
                       f"GROUP BY agent_id, payment_day, payment_type;"

    if db_config:
        conn = sqlite3.connect(db_config.get('default').get('NAME'))
    else:
        conn = sqlite3.connect(DATABASES.get('default').get('NAME'))
    cursor = conn.execute(select_statement)

    report_files_path = os.path.join(MEDIA_ROOT, report.name)
    os.makedirs(report_files_path, exist_ok=True)
    agent_collection_report_document_path = os.path.join(report_files_path, 'agent_collection_report.csv')
    with open(agent_collection_report_document_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['agent_id', 'payment_day', 'payment_type', 'total_payment_amount'])
        for record in cursor:
            writer.writerow([record[0], record[1], record[2], record[3]])
    conn.close()
    return agent_collection_report_document_path


def payment_type_report(report_pk):
    report = Report.objects.get(pk=report_pk)
    select_statement = f"SELECT payment_type, " \
                       f"SUM(payment_amount) AS total_payment_amount " \
                       f"FROM data_center_payment " \
                       f"where payments_document_id = {report.payments_document.pk} " \
                       f'AND payment_status = "SUCCESSFUL"' \
                       f"GROUP BY payment_type;"

    conn = sqlite3.connect(DATABASES.get('default').get('NAME'))
    cursor = conn.execute(select_statement)

    report_files_path = os.path.join(MEDIA_ROOT, report.name)
    os.makedirs(report_files_path, exist_ok=True)
    payment_type_report_document_path = os.path.join(report_files_path, 'payment_type_report.csv')
    with open(payment_type_report_document_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['payment_type', 'total_amount']),
        for record in cursor:
            writer.writerow([record[0], record[1]])
    conn.close()
    return payment_type_report_document_path


class ReportTypes:
    days_from_suspension_report = 'days_from_suspension_report'
    agent_collection_report = 'agent_collection_report'
    days_from_suspension_report_per_agent = 'days_from_suspension_report_per_agent'
    payment_type_report = 'payment_type_report'
    all_reports = 'all_reports'


class ConstantStrings:
    strftime_format = "%d%m%Y%H%M%S"