from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from users.pagination import paginate

from .forms import ProjectForm
from .models import Project

PAGE_SIZE = 12


def project_list(request):
    qs = (
        Project.objects.select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    page_obj = paginate(request, qs, PAGE_SIZE)
    return render(
        request,
        'projects/project_list.html',
        {'projects': qs, 'page_obj': page_obj, 'query_prefix': ''},
    )


@login_required
def favorite_projects(request):
    qs = (
        request.user.favorites.select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    return render(request, 'projects/favorite_projects.html', {'projects': qs})


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=project_id,
    )
    owner = project.owner
    participant_rows = [owner] + list(project.participants.exclude(pk=owner.pk))
    can_join = (
        request.user.is_authenticated
        and request.user.pk != owner.pk
        and project.status == 'open'
    )
    return render(
        request,
        'projects/project-details.html',
        {
            'project': project,
            'participant_rows': participant_rows,
            'can_join': can_join,
        },
    )


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_detail', project_id=project.pk)
    else:
        form = ProjectForm()
    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': False},
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': True},
    )


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if user.favorites.filter(pk=project.pk).exists():
        user.favorites.remove(project)
        favorited = False
    else:
        user.favorites.add(project)
        favorited = True
    return JsonResponse({'status': 'ok', 'favorited': favorited})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id or project.status != 'open':
        return JsonResponse(
            {'status': 'error', 'message': 'Недостаточно прав для этого действия'},
            status=403,
        )
    project.status = 'closed'
    project.save(update_fields=['status'])
    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if project.owner_id == user.pk:
        return JsonResponse(
            {'status': 'error', 'message': 'Автор проекта не может присоединиться как участник'},
            status=400,
        )
    if project.status != 'open':
        return JsonResponse(
            {'status': 'error', 'message': 'К проекту нельзя присоединиться: набор закрыт'},
            status=400,
        )
    if project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
        participant = False
    else:
        project.participants.add(user)
        participant = True
    return JsonResponse({'status': 'ok', 'participant': participant})
