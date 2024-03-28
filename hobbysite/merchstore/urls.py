from django.urls import path
from .views import MerchDetailView, MerchListView

urlpatterns = [
    path('items/', MerchListView.as_view(), name='merch_list'),
    path('item/<int:pk>/', MerchDetailView.as_view(), name='merch_detail'),
]