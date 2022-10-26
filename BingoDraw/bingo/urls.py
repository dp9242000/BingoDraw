from django.urls import path

from . import views

app_name = 'bingo'
urlpatterns = [
    # ex: /bingo/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /bingo/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
