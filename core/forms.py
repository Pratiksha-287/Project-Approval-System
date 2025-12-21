from django import forms
from core.models import Project, Review, User

class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "file", "guide"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # filter so only guides appear
        self.fields["guide"].queryset = User.objects.filter(role="guide")

class GuideApprovalForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["incharge"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["incharge"].queryset = User.objects.filter(role="incharge")
        self.fields["incharge"].required = False 

class InchargeApprovalForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["hod"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hod"].queryset = User.objects.filter(role="hod")
        self.fields["hod"].required = False 


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["feedback", "status_change"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Pass request.user from view
        super().__init__(*args, **kwargs)

        #status choices based on role
        if user.role == "guide":
            self.fields["status_change"].choices = [
                ("under_review", "Under Review"),
                ("needs_revision", "Needs Revision"),
                ("guide_approved", "Guide Approved"),
            ]
        elif user.role == "incharge":
            self.fields["status_change"].choices = [
                ("under_review", "Under Review"),
                ("needs_revision", "Needs Revision"),
                ("incharge_approved", "Incharge Approved"),
            ]
        elif user.role == "hod":
            self.fields["status_change"].choices = [
                ("final_approved", "Final Approved"),
                ("final_rejected", "Final Rejected"),
            ]



