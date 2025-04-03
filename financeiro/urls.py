from django.contrib import admin
from django.urls import path, include
from core.views import TransacaoViewSet, dashboard
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('transacoes', TransacaoViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('dashboard/', dashboard, name='dashboard')
]