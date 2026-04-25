from django.urls import path
from .views import (login_view, register_view,upload_foto,remover_foto,logout_view,criar_card,renomear_card,excluir_card)

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('upload-foto/',upload_foto,name='upload_foto'),
    path('remover-foto/',remover_foto,name='remover_foto'),
    path('logout/',logout_view, name='logout'),
    path("card/criar/", criar_card, name="criar_card"),
    path("card/renomear/<int:id>/", renomear_card, name="renomear_card"),
    path("card/excluir/<int:id>/", excluir_card, name="excluir_card"),
]