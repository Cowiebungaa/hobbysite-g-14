from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product, Transaction
from .forms import TransactionForm
from user_management.models import Profile


class MerchListView(ListView):
    model = Product
    template_name = 'merch_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        all_products = super().get_queryset()

        if self.request.user.is_authenticated:
            user_products = all_products.filter(owner=self.request.user.profile)
            other_products = all_products.exclude(owner=self.request.user.profile)
        else:
            other_products = None
            user_products = None

        return other_products 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_products'] = self.request.user.profile.product_set.all()
            context['other_products'] = Product.objects.exclude(owner=self.request.user.profile)
            context['create_product_url'] = reverse_lazy('merchstore:product_create')
        context['all_products'] = Product.objects.all()
        return context
    
class MerchDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'merch_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        if product.stock == 0:
            context['disable_buy_button'] = True
            context['out_of_stock'] = True
        else:
            context['disable_buy_button'] = False
            context['out_of_stock'] = False
        if product.owner == self.request.user.profile:
            context['editable'] = True
            context['disable_buy_button'] = True
        else:
            context['editable'] = False
        context['form'] = TransactionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = self.get_object()
            transaction.buyer = request.user.profile
            transaction.save()
            product = self.get_object()
            product.stock -= transaction.amount
            product.save()
            if self.request.user.is_authenticated:
                return HttpResponseRedirect(reverse_lazy('merchstore:cart'))
            else:
                return HttpResponseRedirect(reverse_lazy('login'))
        return self.get(request, *args, **kwargs)

    
class MerchCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'product_type', 'description', 'price', 'stock', 'status']
    template_name = 'merch_create.html'
    success_url = reverse_lazy('merchstore:merch_list')
    
    def form_valid(self, form):
        if hasattr(self.request.user, 'profile'):
            form.instance.owner = self.request.user.profile
            return super().form_valid(form)
        else:
            profile = Profile.objects.create(user=self.request.user)
            form.instance.owner = profile
            return super().form_valid(form)
    
class MerchUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'product_type', 'description', 'price', 'stock', 'status']
    template_name = 'merch_update.html'
    success_url = reverse_lazy('merchstore:merch_list')
    
    def form_valid(self, form):
        product = form.save(commit=False)
        if product.stock == 0:
            product.status = 'Out of stock'
        else:
            product.status = 'Available'
        return super().form_valid(form)
    
class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'cart.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(buyer=self.request.user.profile)
    
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(product__owner=self.request.user.profile)