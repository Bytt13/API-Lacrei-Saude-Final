from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfissionalViewSet, ConsultaViewSet

router = DefaultRouter()
router.register(r"profissionais", ProfissionalViewSet)
router.register(r"consultas", ConsultaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
