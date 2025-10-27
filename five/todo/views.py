# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import ToDo
from .forms import ToDoForm

@login_required
def todo_list(request):
    """Display all todos for the logged-in user"""
    todos = ToDo.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'todos': todos})

@login_required
def todo_create(request):
    """Create a new todo"""
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('todo_list')
    else:
        form = ToDoForm()
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def todo_edit(request, pk):
    """Edit an existing todo"""
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo_list')
    else:
        form = ToDoForm(instance=todo)
    
    return render(request, 'todo/todo_form.html', {
        'form': form,
        'todo': todo,
        'action': 'Edit'
    })

@login_required
def todo_delete(request, pk):
    """Delete a todo"""
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('todo_list')
    
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

@login_required
def todo_toggle_complete(request, pk):
    """Toggle todo completion status"""
    todo = get_object_or_404(ToDo, pk=pk, user=request.user)
    
    if todo.completed:
        todo.mark_incomplete()
        status = 'incomplete'
    else:
        todo.mark_complete()
        status = 'complete'
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': status,
            'completed': todo.completed
        })
    
    messages.success(request, f'Todo marked as {status}!')
    return redirect('todo_list')