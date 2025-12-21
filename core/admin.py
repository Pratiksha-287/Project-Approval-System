from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from core.models import User, Project, Review

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "status", "submitted_at", "plagiarism_score")
    list_filter = ("status",)
    search_fields = ("title", "student__username")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("project", "reviewer", "status_change", "reviewed_at")
    search_fields = ("project__title", "reviewer__username")

