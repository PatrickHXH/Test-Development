from django.urls import path
from  . import views


urlpatterns = [
    path('', views.IndexView.as_view(),name="index"),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),     #<int:question_id>类似与正则表达式用外键id表示
    # ex: /polls/5/results/
    path('<int:pk>', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]