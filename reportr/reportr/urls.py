from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from data_center.views import SyncDocumentPaymentsView, SyncDocumentAgentsView, GenerateReportsView
from reportr import settings

urlpatterns = [
    path('', admin.site.urls),
    path('mail/sync_document_payments/<document_id>', SyncDocumentPaymentsView.as_view(),
         name='sync_document_payments'),
    path('mail/sync_document_agents/<document_id>', SyncDocumentAgentsView.as_view(),
         name='sync_document_agents'),
    path('mail/generate_reports/<report_id>', GenerateReportsView.as_view(),
         name='generate_reports'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
