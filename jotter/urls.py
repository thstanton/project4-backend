from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.CreateUser.as_view()),
    path('users/all', views.ListUsers.as_view()),
    path('contexts/', views.ListContexts.as_view()),
    path('contexts/create', views.CreateContext.as_view()),
    path('contexts/<int:pk>', views.ContextDetail.as_view()),
    path('contexts/<int:pk>/update', views.UpdateContext.as_view()),
    path('wordbanks/<int:pk>', views.WordBank.as_view())
]