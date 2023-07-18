from django.urls import path
from .views import todos, toggleCompleted

urlpatterns = [
    path("todos/", todos),
    path("todos/<int:id>/", todos),
    path("todos/<int:id>/toggle", toggleCompleted),
]
 