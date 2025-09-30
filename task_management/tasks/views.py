import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer

logger = logging.getLogger(__name__)

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = request.user.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
        previous_status = task.status
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            new_status = serializer.validated_data.get('status', previous_status)
            if new_status == 'Completed':
                completion_report = request.data.get('completion_report')
                worked_hours = request.data.get('worked_hours')
                if previous_status != 'Completed':
                    if not completion_report or not worked_hours:
                        return Response({"error": "Completion report and worked hours are required when marking as completed"}, status=http_status.HTTP_400_BAD_REQUEST)
                if completion_report:
                    task.completion_report = completion_report
                if worked_hours:
                    try:
                        task.worked_hours = float(worked_hours)
                    except ValueError:
                        return Response({"error": "Worked hours must be a number"}, status=http_status.HTTP_400_BAD_REQUEST)
            serializer.save()
            logger.info(f"Task {task.id} status updated to {new_status} by {request.user.username}")
            return Response(serializer.data)
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

class TaskReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.status != 'Completed':
            return Response({"error": "Task is not completed"}, status=http_status.HTTP_400_BAD_REQUEST)
        user = request.user
        if user.role == 'superadmin':
            pass
        elif user.role == 'admin':
            if task.assigned_to.assigned_to != user:
                return Response({"error": "Not authorized to view this report"}, status=http_status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Not authorized"}, status=http_status.HTTP_403_FORBIDDEN)
        data = {
            'completion_report': task.completion_report,
            'worked_hours': task.worked_hours
        }
        logger.info(f"Task {task.id} report viewed by {request.user.username}")
        return Response(data)