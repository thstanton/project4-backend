from django.urls import path
from . import views

urlpatterns = [
    # User Endpoints
    path('users/<int:group_id>/create/', views.CreateUser.as_view()),
    path('users/all/', views.ListUsers.as_view()),
    path('users/<int:pk>', views.EditUser.as_view()),
    path('users/self/', views.SelfUser.as_view()),
    # Context Endpoints
    path('contexts/', views.ListContexts.as_view()),
    path('contexts/create/', views.CreateContext.as_view()),
    path('contexts/<int:pk>/', views.ContextDetail.as_view()),
    path('contexts/<int:context_id>/assign/<int:class_id>/', views.assoc_class_add),
    path('contexts/<int:context_id>/unassign/<int:class_id>/', views.assoc_class_remove),
    path('contexts/word/<int:pk>/', views.SingleWord.as_view()),
    path('contexts/wordbank/<int:pk>/', views.WordBank.as_view()),
    path('contexts/image/<int:pk>/', views.SingleImage.as_view()),
    # Class Endpoints
    path('class/create/', views.CreatePupilClass.as_view()),
    path('class/<int:pk>/', views.SingleClass.as_view()),
    path('class/join/', views.join_class),
    path('class/<int:class_id>/remove/<int:pupil_id>/', views.remove_from_class),
    path('class/pupil/', views.AssignedContextsView.as_view()),
    # Jotter Endpoints
    path('jotter/create/', views.CreateJotter.as_view()),
    path('jotter/<int:pk>/', views.SingleJotter.as_view()),
    path('jotter/incomplete/', views.ListOwnIncompleteJotters.as_view()),
    path('jotter/complete/', views.ListOwnCompleteJotters.as_view()),
    path('jotter/pupil/<int:pupil_id>/', views.ListPupilJotters.as_view()),
    path('jotter/context/<int:context_id>/class/<int:class_id>/', views.ListContextJotters.as_view())
]