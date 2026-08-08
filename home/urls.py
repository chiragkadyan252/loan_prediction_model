from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        "",
        views.index,
        name="home"
    ),


    # =========================
    # ABOUT
    # =========================

    path(
        "about/",
        views.about,
        name="about"
    ),


    # =========================
    # CONTACT
    # =========================

    path(
        "contact/",
        views.contact,
        name="contact"
    ),


    # =========================
    # LOGIN
    # =========================

    path(
        "login/",
        views.user_login,
        name="login"
    ),


    # =========================
    # SIGN UP
    # =========================

    path(
        "signup/",
        views.signup,
        name="signup"
    ),


    # =========================
    # LOGOUT
    # =========================

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),


    # =========================
    # DASHBOARD
    # =========================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # =========================
    # PREDICTION
    # =========================

    path(
        "prediction/",
        views.prediction,
        name="prediction"
    ),


    # =========================
    # HISTORY
    # =========================

    path(
        "history/",
        views.history,
        name="history"
    ),


    # =========================
    # PDF REPORT
    # =========================

    path(
        "download-report/<int:prediction_id>/",
        views.download_report,
        name="download_report"
    ),

]