from django.urls import path
from . import views

urlpatterns = [
    path("task/", views.task_list, name="task_list"),
    path("task/create/", views.create_task, name="task_create"),
    path("task/<int:pk>/edit/", views.edit_task, name="task_edit"),
    path("task/<int:pk>/delete/", views.delete_task, name="task_delete"),
    path("task/<int:pk>/toggle/", views.toggle_task, name="task_toggle"),
]