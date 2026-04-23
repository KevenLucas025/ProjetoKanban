from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 Django auth (reset de senha, login default etc)
    path('accounts/', include('django.contrib.auth.urls')),

    # 📦 apps
    path('', include('accounts.urls')),
    path('', include('core.urls')),
]