from django.urls import path
from .views import MerchListView, MerchDetailView, MerchCreateView, MerchUpdateView, CartView, TransactionListView, CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('items/', MerchListView.as_view(), name='merch_list'),
    path('item/<int:pk>/', MerchDetailView.as_view(), name='merch_detail'),
    path('item/add/', MerchCreateView.as_view(), name='product_create'),
    path('item/<int:pk>/edit/', MerchUpdateView.as_view(), name='product_update'),
    path('cart/', CartView.as_view(), name='cart'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
]

app_name = 'merchstore'
