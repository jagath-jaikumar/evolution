from datetime import datetime

from django.contrib.auth.models import User
from django.db import connections
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


def root(request):
    return JsonResponse({"message": f"Evolution Server running {datetime.now()}"})


def liveness_check(request):
    return HttpResponse("OK")


def readiness_check(request):
    for connection in connections.all():
        try:
            connection.cursor()
        except Exception as e:
            return HttpResponse(f"Database connection failed: {e}", status=500)
    return HttpResponse("OK")


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response(
        {"message": "User created successfully.", "user_id": user.id},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_id_from_username(request):
    username = request.data.get("username")
    user = User.objects.get(username=username)
    return Response({"user_id": user.id}, status=status.HTTP_200_OK)
