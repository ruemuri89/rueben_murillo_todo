from django.test import TestCase
from django.urls import reverse
from .models import ToDo

# Create your tests here.
class TaskCreationTest(TestCase):
    """
    Given a valid task title, description, and due date,
    Whwen the user submits the create task form
    THEN a new Task should be saved in the database
    AND the user should be redirected to the task list
    """
    def test_create_new_task(self):
        data = {
            "name": "Write unit tests",
            "description": "Add tests for the create_task view",
            "due_date": "2024-12-31",
            "completed": False
        }
        
        response = self.client.post(reverse("create_task"), data)
        
        task = ToDo.objects.first()

        self.assertEqual(response.status_code, 302)  # Redirect to task list
        self.assertRedirects(response, reverse("task_list"))
        self.assertEqual(ToDo.objects.count(), 1)
        self.assertEqual(task.name, "Write unit tests")
        self.assertFalse(task.completed)
        self.assertEqual(str(task.due_date), "2024-12-31")