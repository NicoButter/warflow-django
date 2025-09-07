from django.shortcuts import render, redirect
from .models import Project, ProjectMembership
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    memberships = ProjectMembership.objects.filter(user=request.user)
    return render(request, 'projects/dashboard.html', {'memberships': memberships})

@login_required
def create_project(request):
    if request.method == "POST":
        name = request.POST.get('name')
        project = Project.objects.create(name=name)
        ProjectMembership.objects.create(user=request.user, project=project, role='admin')
        return redirect('projects:dashboard')
    return render(request, 'projects/create_project.html')
