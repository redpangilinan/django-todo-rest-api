from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status

# CRUD functionality for Todo
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def todos(request, id=None):
    if request.method == 'GET':
        if id is not None:
            try:
                todo = Todo.objects.get(pk=id)
                serializer = TodoSerializer(todo)
                return Response(serializer.data)
            except Todo.DoesNotExist:
                return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            completed_param = request.query_params.get('completed', None)

            if completed_param is None:
                todos = Todo.objects.all()
            elif completed_param.lower() == 'true':
                todos = Todo.objects.filter(completed=True)
            elif completed_param.lower() == 'false':
                todos = Todo.objects.filter(completed=False)
            else:
                return Response({"error": "Invalid parameter"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            todo = Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            todo = Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Toggles the Todo status to either complete or incomplete
@api_view(['PUT'])
def toggleCompleted(request, id):
    try:
        todo = Todo.objects.get(pk=id)
    except Todo.DoesNotExist:
        return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

    todo.completed = not todo.completed
    todo.save()

    serializer = TodoSerializer(todo)
    return Response(serializer.data)