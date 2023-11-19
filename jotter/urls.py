from django.urls import path
from . import views

urlpatterns = [
    path('users/<int:group_id>/create/', views.CreateUser.as_view()),
    path('users/all/', views.ListUsers.as_view()),
    path('users/<int:pk>', views.EditUser.as_view()),

    path('contexts/', views.ListContexts.as_view()),
    path('contexts/create/', views.CreateContext.as_view()),
    path('contexts/<int:pk>/', views.ContextDetail.as_view()),
    path('contexts/<int:context_id>/assign/<int:class_id>/', views.assoc_class_add),
    path('contexts/<int:context_id>/unassign/<int:class_id>/', views.assoc_class_remove),

    path('word/<int:pk>/', views.SingleWord.as_view()),
    path('wordbank/<int:pk>/', views.WordBank.as_view()),

    path('class/create/', views.CreatePupilClass.as_view()),
    path('class/<int:pk>', views.SingleClass.as_view()),
    path('class/join/', views.join_class),
    path('class/<int:class_id>/remove/<int:pupil_id>/', views.remove_from_class)
]