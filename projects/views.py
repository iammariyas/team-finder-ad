from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from users.constants import PROJECT_STATUS_OPEN, PROJECT_STATUS_CLOSED
from users.pagination import paginate
from .forms import ProjectForm
from .models import Project


def project_list(request):
    qs = (
        Project.objects.select_related('owner')
        .prefetch_related('participants')
    )
    page_obj = paginate(request, qs)
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
        and project.status == PROJECT_STATUS_OPEN
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
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect('project_detail', project_id=project.pk)
    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': False},
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('project_detail', project_id=project.pk)
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
    if is_favorited := user.favorites.filter(pk=project.pk).exists():
        user.favorites.remove(project)
    else:
        user.favorites.add(project)
    return JsonResponse({'status': 'ok', 'favorited': not is_favorited})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id:
        return JsonResponse(
            {'status': 'error', 'message': 'Только автор проекта может его завершить'},
            status=HttpResponseForbidden.status_code,
        )
    if project.status != PROJECT_STATUS_OPEN:
        return JsonResponse(
            {'status': 'error', 'message': 'Завершить можно только открытый проект'},
            status=HttpResponseForbidden.status_code,
        )
    project.status = PROJECT_STATUS_CLOSED
    project.save(update_fields=['status'])
    return JsonResponse({'status': 'ok', 'project_status': project.status})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if project.owner == user:
        return JsonResponse(
            {'status': 'error', 'message': 'Автор проекта не может присоединиться как участник'},
            status=HttpResponseBadRequest.status_code,
        )
    if project.status != PROJECT_STATUS_OPEN:
        return JsonResponse(
            {'status': 'error', 'message': 'К проекту нельзя присоединиться: набор закрыт'},
            status=HttpResponseBadRequest.status_code,
        )
    if is_participant := project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({'status': 'ok', 'participant': not is_participant})
