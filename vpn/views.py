from django.views.generic import TemplateView
from .models import Tariff


class TariffsView(TemplateView):
    template_name = 'vpn/tariffs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tariffs'] = Tariff.objects.all()
        
        return context