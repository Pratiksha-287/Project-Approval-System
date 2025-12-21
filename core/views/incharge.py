from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Project, Review, User
from core.forms import ReviewForm,  InchargeApprovalForm
from django.core.mail import send_mail

@login_required
def dashboard(request):
    if request.user.role != "incharge":
        return render(request, "403.html", status=403)
    projects = Project.objects.filter(status="guide_approved").order_by("-submitted_at")
    return render(request, "incharge/dashboard.html", {"projects": projects})

@login_required
def review_project(request, project_id):
    if request.user.role != "incharge":
        return render(request, "403.html", status=403)
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, user=request.user) 
        # form = ReviewForm(request.POST)
        approval_form = InchargeApprovalForm(request.POST, instance=project)
        if form.is_valid() and approval_form.is_valid():
            rv = form.save(commit=False)
            rv.reviewer = request.user
            rv.project = project
            rv.save()
            project.status = rv.status_change
            project.save()

             #email
            subject = f"Feedback from {request.user.role} on your project: {project.title}"
            message = (
                f"Hello {project.student.username},\n\n"
                f"You have received new feedback from {request.user.username}.\n\n"
                f"Feedback: {rv.feedback}\n"
                f"New Status: {rv.status_change}\n\n"
                "Please log in to your dashboard for more details."
            )

            send_mail(
                subject,
                message,
                None,
                [project.student.email],
                fail_silently=False,
            )
            return redirect("incharge_dashboard")
    else:
        form = ReviewForm(user=request.user)
        approval_form = InchargeApprovalForm(request.POST, instance=project)
    return render(request, "incharge/review_project.html", {"project": project, "form": form,"approval_form": approval_form })
