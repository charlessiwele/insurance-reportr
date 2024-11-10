from datetime import datetime
from django.contrib import admin
from data_center import models
from data_center.models import DocumentStatus
from data_center.services.report_services import ConstantStrings


# Register your models here.
@admin.register(models.DocumentStatus)
class DocumentStatusAdmin(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.
@admin.register(models.PaymentDocument)
class PaymentDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'file',
        'process_status',
    ]
    change_form_template = 'admin/payment_document_change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        form = super(PaymentDocumentAdmin, self).get_form(request, obj, **kwargs)
        datetime_now = datetime.now().strftime("%d%m%Y%H%M%S")
        if not obj:
            form.base_fields['process_status'].initial = DocumentStatus.objects.get(name='UNPROCESSED')
            form.base_fields['name'].initial = datetime_now
        return form

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        name = form.cleaned_data.get('file').name
        form.instance.name = name
        return super(PaymentDocumentAdmin, self).save_form(request, form, change)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj and obj.pk:
            context['pk'] = obj.pk
        return super(PaymentDocumentAdmin, self).render_change_form(
            request, context, add=add, change=change, form_url=form_url, obj=obj
        )


# Register your models here.
@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'device_id',
        'payment_id',
        'payment_type',
        'payment_amount',
        'payment_created',
        'payment_status',
        'agent_id',
        'payments_document'
    ]

    readonly_fields = [
        'device_id',
        'payment_id',
        'payment_type',
        'payment_amount',
        'payment_created',
        'payment_status',
        'agent_id',
        'payments_document'
    ]

    @staticmethod
    def payments_document(obj):
        return obj.payments_document.name

    change_form_template = 'admin/change_form.html'


@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'agent_id',
        'name'
    ]
    change_form_template = 'admin/change_form.html'


class GeneratedReportTabularInline(admin.TabularInline):
    model = models.GeneratedReport
    readonly_fields = ('name', 'file', 'report', 'created_at', 'updated_at')


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'report_type',
        'payments_document'
    ]

    @staticmethod
    def report_type(obj):
        return obj.report_type.name

    @staticmethod
    def payments_document(obj):
        return obj.payments_document.name

    def get_form(self, request, obj=None, **kwargs):
        form = super(ReportAdmin, self).get_form(request, obj, **kwargs)
        datetime_now = datetime.now().strftime(ConstantStrings.strftime_format)
        if not obj:
            form.base_fields['name'].initial = datetime_now
        return form

    change_form_template = 'admin/reports_change_form.html'

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj and obj.pk:
            context['pk'] = obj.pk
        return super(ReportAdmin, self).render_change_form(
            request, context, add=add, change=change, form_url=form_url, obj=obj
        )

    inlines = [GeneratedReportTabularInline]
