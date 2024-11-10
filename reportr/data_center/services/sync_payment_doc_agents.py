import csv

from data_center.models import PaymentDocument, Agent


def sync_payment_doc_agents(document_id):
    payments_document = PaymentDocument.objects.get(pk=document_id)
    document_path = payments_document.file.path
    processed_count = 0
    exist_count = 0
    with open(document_path, newline='', encoding="utf8") as inputfile:
        for idx, row in enumerate(csv.reader(inputfile, delimiter=",")):
            if idx > 1:
                agent, created = Agent.objects.get_or_create(
                    agent_id=row[8],
                    name=row[8],
                )
                if created:
                    processed_count = processed_count + 1
                else:
                    exist_count = exist_count + 1
    print(exist_count, " records exists")
    print(processed_count, " records created")
    return processed_count
