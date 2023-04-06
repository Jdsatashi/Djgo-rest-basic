from django.urls import path
from .views import *


urlpatterns = [
    path('acticle/', acticle_list),
    path('acticle/detail/<int:id>/', acticle_detail)
]