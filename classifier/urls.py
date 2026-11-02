from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('classify/', views.classify_view, name='classify'),
    path('record/<int:record_id>/', views.record_detail, name='record_detail'),
    path('record/<int:record_id>/delete/', views.delete_record, name='delete_record'),
    path('categories/', views.categories_view, name='categories'),
    path('cnn-explorer/', views.cnn_explorer_view, name='cnn_explorer'),
    path('history/', views.history_view, name='history'),
    path('history/clear/', views.clear_history, name='clear_history'),
    path('about/', views.about_view, name='about'),
    path('api-docs/', views.api_docs_view, name='api_docs'),
    path('api/classify/', views.api_classify, name='api_classify'),
]
