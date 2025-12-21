from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        # simple role-based redirect
        role = getattr(request.user, "role", None)
        if role == "student":
            return redirect("student_dashboard")
        if role == "guide":
            return redirect("guide_dashboard")
        if role == "incharge":
            return redirect("incharge_dashboard")
        if role == "hod":
            return redirect("hod_dashboard")
    return render(request, "home.html")
