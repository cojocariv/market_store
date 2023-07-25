from django.shortcuts import render
from http import HTTPStatus
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from orders.forms import OrderForm
from django.urls import reverse, reverse_lazy
from common.views import TitleMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from orders.models import Order
from django.views.generic.detail import DetailView
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NWJOoGAcI2m7FYu0EBQUFUk',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    @csrf_exempt
    def stripe_webhook_view(request):
        payload = request.body

        # For now, you only need to print out the webhook payload so you can see
        # the structure.
        print(payload)

        return HttpResponse(status=200)
