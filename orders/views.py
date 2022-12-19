from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from common.views import TitleMixin
from .forms import OrderForm

# Create your views here.


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = ' Store | Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('order_success')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

class OrderSuccessView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store | Заказ оформлен'
