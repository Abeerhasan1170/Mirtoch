from django.urls import path
from . import views

app_name = 'mirtoch'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    #path('user/<str:name>/', views.userProfile, name="profiles"),
    path('search/', views.query_user, name="search"),
    path('user/', views.profileView, name="profileView"),
    path('about/', views.about, name="about"),
    path('publications/', views.publications, name="publications"),
    path('publications/<str:slug>/',
         views.single_publication, name='single-publication'),
    path('register/', views.register, name='register'),
    path('sendmessage/', views.sendmessage, name="sendmessage"),
    path('terms/', views.terms, name="terms"),
    path('sentiment/<str:name>/', views.sentiment, name="sentiment"),
    path('category/<str:catname>/', views.get_category, name="category"),
    path('change_country/', views.change_default_country, name="change_category"),
    path('verify/<token>/', views.verify_email, name='verify_email'),
    path('add-comment/', views.add_comment, name='add_comment'),
]
