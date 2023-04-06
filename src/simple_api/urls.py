from django.urls import path
from .views import *


urlpatterns = [
    # use Django's HTTP request
    path('acticle/', acticle_list),
    path('acticle/detail/<int:id>/', acticle_detail),
    # use REST Framework Request instance
    path('acticleApi/', acticleAPIView.as_view()),
    path('acticleApi/<int:id>/', acticleDetails.as_view()),
    # use Generic view API
    path('acticleGeneric/', GenericApiView.as_view()),
    path('acticleGeneric/<int:id>/', GenericApiView.as_view())
]