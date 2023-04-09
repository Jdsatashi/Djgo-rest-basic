from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('viewset', ActicleViewSet, basename='acticle')
router.register('genericview', GenericViewActicle, basename='acticles')

urlpatterns = [
    # use Django's HTTP request
    path('acticle/', acticle_list),
    path('acticle/detail/<int:id>/', acticle_detail),
    # use REST Framework Request instance
    path('acticleApi/', acticleAPIView.as_view()),
    path('acticleApi/<int:id>/', acticleDetails.as_view()),
    # use Generic view API
    path('acticleGeneric/', GenericApiView.as_view()),
    path('acticleGeneric/<int:id>/', GenericApiView.as_view()),
    # Use View Set
    path('acticles/', include(router.urls)),
]
