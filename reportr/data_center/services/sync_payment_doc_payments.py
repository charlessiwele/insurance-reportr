import csv

from data_center.models import Payment, PaymentDocument


def sync_payment_doc_payments(document_id):
    payments_document = PaymentDocument.objects.get(pk=document_id)
    document_path = payments_document.file.path
    processed_count = 0
    exist_count = 0
    with open(document_path, newline='', encoding="utf8") as inputfile:
        for idx, row in enumerate(csv.reader(inputfile, delimiter=",")):
            if idx > 1:
                payment, created = Payment.objects.get_or_create(
                    payment_id=row[0],
                    payment_type=row[1],
                    payment_amount=row[2],
                    payment_signature_image=row[3],
                    payment_photo=row[4],
                    payment_created=row[5],
                    payment_status=row[6],
                    notes=row[7],
                    agent_id=row[8],
                    device_id=row[9],
                    payments_document=payments_document,
                )
                if created:
                    processed_count = processed_count + 1
                else:
                    exist_count = exist_count + 1
    print(exist_count, " records exists")
    print(processed_count, " records created")
    return processed_count
