from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.index,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "prediction/",
        views.prediction,
        name="prediction"
    ),

    path(
        "history/",
        views.history,
        name="history"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "download-report/<int:prediction_id>/",
        views.download_report,
        name="download_report"
    ),

]