from rest_framework.routers import DefaultRouter
from contracts import views

router = DefaultRouter()

router.register(r'contracts', views.ContractViewSet)
router.register(r'energy-bills', views.EnergyBillViewSet)
