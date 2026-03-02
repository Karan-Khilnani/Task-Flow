from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import RegisterForm


# ─── REGISTER ───────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username} 🎉')
            return redirect('tasks')
        else:
            # Show each form error as a message
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    return render(request, 'register.html', {'form': form})


# ─── LOGIN ───────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! 👋')
            return redirect('tasks')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# ─── LOGOUT ──────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# ─── TASK LIST + ADD TASK ────────────────────────────────────
@login_required(login_url='login')
def tasks_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Task.objects.create(user=request.user, title=title)
            messages.success(request, 'Task added ✅')
        else:
            messages.error(request, 'Task cannot be empty.')
        return redirect('tasks')

    tasks = Task.objects.filter(user=request.user)

    # Counts for stats bar
    total     = tasks.count()
    completed = tasks.filter(completed=True).count()
    remaining = total - completed

    context = {
        'tasks'    : tasks,
        'total'    : total,
        'completed': completed,
        'remaining': remaining,
    }
    return render(request, 'tasks.html', context)


# ─── COMPLETE TASK ───────────────────────────────────────────
@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed   # toggle on/off
    task.save()
    return redirect('tasks')


# ─── DELETE TASK ─────────────────────────────────────────────
@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted.')
    return redirect('tasks')