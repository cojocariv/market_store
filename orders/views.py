from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from orders.forms import OrderForm
from django.urls import reverse_lazy
from common.views import TitleMixin
from django.views.generic.list import ListView
from orders.models import Order
from django.views.generic.detail import DetailView


class SuccesTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Multumim pentru comanda!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Comenzi'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - comanda Nr. {{ self.object.id }}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Perfectarea comenzii'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
