from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class ToDo(models.Model):
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['due_date']
        verbose_name = 'To-Do'
        verbose_name_plural = 'To-Dos'
        
    def mark_complete(self):
        "Mark todo as complete"
        self_completed = True
        self.save()
    
    def mark_incomplete(self):
        "Mark todo as incomplete"
        self.completed = False
        self.save()
    
    def is_overdue(self):
        "Check if todo is overdue"
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False