from django.urls import path
from . import views
from .feeds import LatestTasksFeed

app_name = 'todo'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    
    path('tag/<str:tag_slug>/', views.TaskListView.as_view(), name='task_list_by_tag'),
    
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.task_detail, name='task_detail'),
    path('buy/<int:pk>/', views.buy_skin, name='buy_skin'),
    path('<int:task_id>/share/', views.task_share, name='task_share'),
    path('feed/', LatestTasksFeed(), name='task_feed'),
]