from django.urls import path
from core.views import home, student, guide, incharge, hod, auth_views

urlpatterns = [
    path("", home.home, name="home"),
    path("accounts/login/", auth_views.login_view, name="login"),
    path("accounts/logout/", auth_views.logout_view, name="logout"),

    path("student/dashboard/", student.dashboard, name="student_dashboard"),
    path("student/upload/", student.upload_project, name="upload_project"),

    path("guide/dashboard/", guide.dashboard, name="guide_dashboard"),
    path("guide/review/<int:project_id>/", guide.review_project, name="guide_review"),

    path("incharge/dashboard/", incharge.dashboard, name="incharge_dashboard"),
    path("incharge/review/<int:project_id>/", incharge.review_project, name="incharge_review"),

    path("hod/dashboard/", hod.dashboard, name="hod_dashboard"),
    path("hod/review/<int:project_id>/", hod.review_project, name="hod_review"),
]