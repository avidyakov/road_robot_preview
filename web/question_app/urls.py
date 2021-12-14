from django.urls import path

from question_app import views


app_name = 'question_app'

urlpatterns = [
    path('', views.QuestionSearch.as_view())
]
