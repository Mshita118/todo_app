from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Category
from .forms import TaskForm
from django.db.models import Q
from django.core.paginator import Paginator


def task_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'created_at')
    show_completed = request.GET.get('show_completed', 'true')

    tasks = Task.objects.all()

    if show_completed == 'false':
        tasks = tasks.filter(completed=False)

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if sort_by == 'category':
        tasks = tasks.order_by('category__name', 'title')
    else:
        tasks = tasks.order_by(sort_by)

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'sort_by': sort_by,
        'show_completed': show_completed,
        'query': query,
        'page_obj': page_obj,
    })


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'todo/task_detail.html', {'task': task})
