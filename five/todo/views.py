from django.shortcuts import render,redirect, get_object_or_404
from .models import ToDo
from .forms import ToDoForm

# Create your views here.
def task_list(request):
    tasks = ToDo.objects.all().order_by("due_date")
    return render(request, "todo/task_list.html", {"tasks": tasks})

def task_create(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = ToDoForm()
    return render(request, "todo/task_form.html", {"form": form})