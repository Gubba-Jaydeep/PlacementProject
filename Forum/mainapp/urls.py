from django.urls import path,re_path

from . import views

app_name="mainapp"
urlpatterns=[
    path("",views.index,name="index"),
    path("askQuestion", views.askQuestion, name="askQuestion"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("r_validate", views.r_validate, name="r_validate"),
    path("logout", views.logout, name="logout"),
    path("postAnswer", views.postAnswer, name="postAnswer"),
    path("incQuestionVote", views.incQuestionVote, name="incQuestionVote"),
    path("decQuestionVote", views.decQuestionVote, name="decQuestionVote"),
    re_path(r'^(?P<qID>[0-9]+)/$', views.getQuestionDetails, name="getQuestionDetails"),
    path("<int:aID>/ok",views.incAnswerVote,name="incAnswerVote"),
    path("<int:aID>/notok",views.decAnswerVote,name="decAnswerVote"),
    path("profile", views.profile, name="profile"),
    path("info",views.info, name="info"),
    path("addData",views.addData,name="addData"),
]