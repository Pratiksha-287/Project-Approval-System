from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Project, Review
from core.forms import ProjectUploadForm

@login_required
def dashboard(request):
    if request.user.role != "student":
        return render(request, "403.html", status=403)
    # projects = request.user.projects.all().order_by("-submitted_at")
    projects = Project.objects.filter(student=request.user).order_by("-submitted_at")
    # Fetch related reviews for each project
    projects_with_reviews = []
    for p in projects:
        reviews = Review.objects.filter(project=p)
        projects_with_reviews.append({"project": p, "reviews": reviews})

    return render(request, "student/dashboard.html", {"projects_with_reviews": projects_with_reviews})
    # return render(request, "student/dashboard.html", {"projects": projects})

@login_required
def upload_project(request):
    if request.user.role != "student":
        return render(request, "403.html", status=403)
    if request.method == "POST":
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.student = request.user
            p.status = "uploaded"
            p.save()
            return redirect("student_dashboard")
    else:
        form = ProjectUploadForm()
    return render(request, "student/upload_project.html", {"form": form})
