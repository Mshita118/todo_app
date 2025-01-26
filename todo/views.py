from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Category, Priority, Comment
from .forms import TaskForm, CategoryForm, CommentForm, SortForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def custom_logout(request):
    logout(request)
    return redirect('logged_out')


@login_required
def task_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'created_at')
    show_completed = request.GET.get('show_completed', 'true')

    tasks = Task.objects.all()

    if show_completed == 'false':
        tasks = tasks.filter(completed=False)

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
        )

    if sort_by == 'category':
        tasks = tasks.order_by('category__name', 'title')
    elif sort_by == 'priority':
        tasks = tasks.order_by('priority__level', 'title')
    else:
        tasks = tasks.order_by(sort_by)

    deadline_soon = datetime.now().date() + timedelta(days=7)

    for task in tasks:
        task.is_deadline_soon = task.deadline and task.deadline <= deadline_soon

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = SortForm(initial={'sort_by': sort_by})

    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'sort_by': sort_by,
        'show_completed': show_completed,
        'query': query,
        'page_obj': page_obj,
        'form': form,
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
    comments = task.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = CommentForm()

    return render(request, 'todo/task_detail.html', {'task': task, 'comments': comments, 'form': form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'todo/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'todo/category_form.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'todo/category_form.html', {'form': form, 'category': category})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'todo/category_confirm_delete.html', {'category': category})
