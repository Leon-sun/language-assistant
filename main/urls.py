from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('lookup/', views.word_lookup, name='word_lookup'),
    path('words/', views.word_list, name='word_list'),
    path('words/<int:word_id>/', views.word_detail, name='word_detail'),
    path('words/<int:word_id>/delete/', views.word_delete, name='word_delete'),
    path('stories/', views.stories, name='stories'),
    path('profile/', views.profile_settings, name='profile_settings'),
]
