from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Card


@login_required
def dashboard(request):

    cards = Card.objects.filter(
        user=request.user
    )

    data_de = request.GET.get("de")
    data_ate = request.GET.get("ate")

    if data_de:
        cards = cards.filter(criado_em__date__gte=data_de)

    if data_ate:
        cards = cards.filter(criado_em__date__lte=data_ate)

    cards = cards.order_by("ordem", "id")

    contador_colunas = {
        "AF": cards.filter(coluna="AF").count(),
        "PE": cards.filter(coluna="PE").count(),
        "CA": cards.filter(coluna="CA").count(),
        "FF": cards.filter(coluna="FF").count(),
        "EP": cards.filter(coluna="EP").count(),
        "CO": cards.filter(coluna="CO").count(),
    }

    return render(request, 'core/dashboard.html', {
        "cards": cards,
        "contador_colunas": contador_colunas
    })