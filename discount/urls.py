from django.urls import path

from .views import DiscountView, ReportView

app_name = 'discount'

urlpatterns = [
    path('discount', DiscountView.as_view(), name='discount'),
    path('report', ReportView.as_view(), name='report')
]
