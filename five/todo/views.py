# views.py - UPDATE function names
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import ToDo
from .forms import ToDoForm

@login_required
def task_list(request):  # Renamed from todo_list
    """Display all todos for the logged-in user"""
    todos = ToDo.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'todos': todos})

@login_required
def task_create(request):  # Renamed from todo_create
    """Create a new todo"""
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = ToDoForm()
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def task_edit(request, pk):  # Renamed from todo_edit
    """Edit an existing todo"""
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = ToDoForm(instance=todo)
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'todo': todo,
        'action': 'Edit'
    })

@login_required
def task_delete(request, pk):  # Renamed from todo_delete
    """Delete a todo"""
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

@login_required
def task_toggle_complete(request, pk):  # Renamed from todo_toggle_complete
    """Toggle todo completion status"""
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if todo.completed:
        todo.mark_incomplete()
        status = 'incomplete'
    else:
        todo.mark_complete()
        status = 'complete'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': status,
            'completed': todo.completed
        })
    
    messages.success(request, f'Task marked as {status}!')
    return redirect('task_list')