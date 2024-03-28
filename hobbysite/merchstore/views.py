from django.views.generic import ListView, DetailView
from .models import Product, ProductType

class MerchListView(ListView):
    model = ProductType
    template_name = 'merch_list.html'
    context_object_name = 'product_types'

class MerchDetailView(DetailView):
    model = Product
    template_name = 'merch_detail.html'
    context_object_name = 'product'