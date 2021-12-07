from django.urls import path
from .views import *
app_name = 'timeline'
urlpatterns = [
    path('', index, name='timelines'),
    path('<str:slug>/', Posts_in_TitleView)
    # path("", Posts_in_TitleView),
]
