from django.shortcuts import render,redirect, get_object_or_404
from .models import ToDo
from .forms import ToDoForm

# Create your views here.
def task_list(request):
    tasks = ToDo.objects.all().order_by("due_date")
    return render(request, "todo/task_list.html", {"tasks": tasks})

def create_task(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = ToDoForm()
    return render(request, "todo/task_form.html", {"form": form})

def edit_task(request, pk):
    task = get_object_or_404(ToDo, pk=pk)
    if request.method == 'POST':
        form = ToDoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = ToDoForm(instance=task)
    return render(request, "todo/task_form.html", {"form": form})

def delete_task(request, pk):
    task = get_object_or_404(ToDo, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect("task_list")
    return render(request, "todo/task_confirm_delete.html", {"task": task})

def toggle_task(request, pk):
    task = get_object_or_404(ToDo, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect("task_list")
