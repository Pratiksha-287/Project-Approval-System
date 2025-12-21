from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Project, Review, User
from core.forms import ReviewForm, GuideApprovalForm


@login_required
def dashboard(request):
    if request.user.role != "guide":
        return render(request, "403.html", status=403)
    
    projects = Project.objects.filter(
        guide=request.user,
        status__in=["uploaded", "under_review"],
        ).order_by("-submitted_at")
    return render(request, "guide/dashboard.html", {"projects": projects})

@login_required
def review_project(request, project_id):
    if request.user.role != "guide":
        return render(request, "403.html", status=403)
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        # form = ReviewForm(request.POST)
        form = ReviewForm(request.POST, user=request.user) 
        approval_form = GuideApprovalForm(request.POST, instance=project)
        
        if form.is_valid() and approval_form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.project = project
            review.save()
            # update project status from form.status_change
            project.status = review.status_change
            project.save()

             #email
            subject = f"Feedback from {request.user.role} on your project: {project.title}"
            message = (
                f"Hello {project.student.username},\n\n"
                f"You have received new feedback from {request.user.username}.\n\n"
                f"Feedback: {review.feedback}\n"
                f"New Status: {review.status_change}\n\n"
                "Please log in to your dashboard for more details."
            )

            send_mail(
                subject,
                message,
                None,
                [project.student.email],
                fail_silently=False,
            )
            return redirect("guide_dashboard")
    else:
        form = ReviewForm(user=request.user)
        approval_form = GuideApprovalForm(instance=project)

    return render(request, "guide/review_project.html", {"project": project, "form": form,"approval_form": approval_form })
