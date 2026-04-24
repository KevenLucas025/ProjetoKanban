from django.urls import path
from .views import login_view, register_view,upload_foto,remover_foto

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('upload-foto/',upload_foto,name='upload_foto'),
    path('remover-foto/',remover_foto,name='remover_foto'),
]