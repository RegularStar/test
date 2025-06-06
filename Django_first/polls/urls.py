from django.urls import path
from . import views

app_name = "polls"


urlpatterns = [
    #     path("", views.index, name="index"),
    #     path("/<int:question_id>/", views.detail, name="detail"),
    #     path("/<int:question_id>/results/", views.results, name="results"),
    #     path("/<int:question_id>/vote/", views.vote, name="vote"),
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("create/", views.QuestionCreateView.as_view(), name="question_create"),
    path(
        "<int:pk>/update/", views.QuestionUpdateView.as_view(), name="question_update"
    ),
    path(
        "<int:pk>/delete/", views.QuestionDeleteView.as_view(), name="question_delete"
    ),
]
