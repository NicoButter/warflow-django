from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from accounts.models import CustomUser
from projects.models import Project, ProjectMembership

# --- Helpers ---
def is_admin(user):
    return user.role == 'admin'  # o user.is_staff si quieres seguir usando staff

# --- Dashboards ---
@login_required
def dashboard_welcome(request):
    """
    Dashboard inicial para usuarios nuevos.
    Solo pueden crear un proyecto nuevo.
    """
    if request.method == 'POST':
        name = request.POST.get('project_name')
        if name:
            project = Project.objects.create(name=name)
            ProjectMembership.objects.create(user=request.user, project=project, role='admin')
            return redirect('dashboards:dashboard_user')
    return render(request, 'dashboards/dashboard_welcome.html')

@login_required
def dashboard_user(request):
    """
    Dashboard para usuarios que ya tienen proyectos.
    Muestra todos los proyectos donde participa.
    """
    memberships = ProjectMembership.objects.filter(user=request.user)
    return render(request, 'dashboards/dashboard_user.html', {'memberships': memberships})

@login_required
@user_passes_test(is_admin)
def dashboard_admin(request):
    """
    Dashboard global de administradores del sistema (opcional)
    """
    users = CustomUser.objects.all()
    return render(request, 'dashboards/dashboard_admin.html', {'users': users})

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
