from .models import Basket


def basket(request):
    """context_processor to show basket without get_context_data()"""

    user = request.user
    return {'basket': Basket.objects.filter(user=user) if user.is_authenticated else []}