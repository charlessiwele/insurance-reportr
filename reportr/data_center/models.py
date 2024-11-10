from django.db import models


class DocumentStatus(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Documents Statuses"

    def __str__(self):
        return self.name


class PaymentDocument(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(upload_to='documents', blank=True, null=True)
    process_status = models.ForeignKey(DocumentStatus, on_delete=models.DO_NOTHING, max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Payment Documents"

    def __str__(self):
        return self.name


class Agent(models.Model):
    agent_id = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Agents"

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_id = models.CharField(max_length=500, blank=True, null=True)
    payment_type = models.CharField(max_length=500, blank=True, null=True)
    payment_amount = models.CharField(max_length=500, blank=True, null=True)
    payment_signature_image = models.CharField(max_length=500, blank=True, null=True)
    payment_photo = models.CharField(max_length=500, blank=True, null=True)
    payment_created = models.CharField(max_length=500, blank=True, null=True)
    payment_status = models.CharField(max_length=500, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    agent_id = models.CharField(max_length=500, blank=True, null=True)
    device_id = models.CharField(max_length=500, blank=True, null=True)
    payments_document = models.ForeignKey(PaymentDocument, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Payments"

    def __str__(self):
        return f'Payment ID: {self.payment_id}'


class ReportType(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Report Types"

    def __str__(self):
        return self.name


class Report(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    report_type = models.ForeignKey(ReportType, on_delete=models.DO_NOTHING, blank=True, null=True)
    payments_document = models.ForeignKey(PaymentDocument, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Reports"

    def __str__(self):
        return self.name


class GeneratedReport(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    report = models.ForeignKey(
        Report,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Generated Report Documents"

    def __str__(self):
        return self.name
