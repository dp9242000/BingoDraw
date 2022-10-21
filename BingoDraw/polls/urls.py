from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote', views.vote, name='vote'),
    # ex: /polls/new/
    path('new/', views.QuestionCreateView.as_view(), name='question-create'),
    # ex: /polls/5/update/
    path('<int:pk>/update/', views.QuestionUpdateView.as_view(), name='update'),
    # ex: /polls/5/delete/
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    # ex: /polls/user
    path('<str:username>', views.UserPollListView.as_view(), name='user-polls'),
]
