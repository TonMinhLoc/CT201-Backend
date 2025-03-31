from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'competition', views.CompetitionView)


urlpatterns = [
    path('viewset/', include(router.urls)),
]
