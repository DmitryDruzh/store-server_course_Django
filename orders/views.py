from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket

from .forms import OrderForm
from .models import Order

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = ' Store | Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        basket = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=basket.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse("order_success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse("order_canceled")}',
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

class OrderSuccessView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store | Заказ оформлен'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'
    title = 'Store | Ошибка оплаты'


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

     # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


class OrderListView(TitleMixin, ListView):
    title = 'Store | Заказы'
    template_name = 'orders/orders.html'
    queryset = Order.objects.all()
    context_object_name = 'orders'
    ordering = ('id')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store | Заказ № {self.object.id}'
        return context
