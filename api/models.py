from django.db import models

class Todo(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'todos'

    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(blank=False)
    completed = models.BooleanField(default=False)