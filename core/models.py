from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("guide", "Guide"),
        ("incharge", "In-charge"),
        ("hod", "HOD"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.username} ({self.role})"


class Project(models.Model):
    STATUS_CHOICES = [
        ("uploaded", "Uploaded"),
        ("under_review", "Under Review"),
        ("needs_revision", "Needs Revision"),
        ("guide_approved", "Guide Approved"),
        ("incharge_approved", "In-charge Approved"),
        ("final_approved", "Final Approved"),
        ("final_rejected", "Final Rejected"),
        
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="projects/", blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="uploaded")
    plagiarism_score = models.FloatField(default=0.0)
    # repo_link = models.URLField(blank=True, null=True) 
    submitted_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    guide = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="guided_projects")
    incharge = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="incharge_projects")
    hod = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="hod_projects")


    def __str__(self):
        return f"{self.title} - {self.student.username} ({self.status})"
    


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True, null=True)  
    status_change = models.CharField(max_length=30, choices=Project.STATUS_CHOICES)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} on {self.project.title}"

