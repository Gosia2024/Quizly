from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Quiz
from .serializers import QuizSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    url = request.data.get("url")

    if not url:
        return Response(
            {"detail": "URL is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if "youtube.com" not in url and "youtu.be" not in url:
        return Response(
            {"detail": "Invalid YouTube URL"},
            status=status.HTTP_400_BAD_REQUEST
        )

    quiz = Quiz.objects.create(
        title="Generated Quiz",
        description="Quiz generated from YouTube video",
        video_url=url,
        owner=request.user
    )

    serializer = QuizSerializer(quiz)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_quizzes(request):
    quizzes = Quiz.objects.filter(owner=request.user)
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Sprawdzenie właściciela
    if quiz.owner != request.user:
        return Response(
            {"detail": "Access denied - quiz does not belong to user"},
            status=status.HTTP_403_FORBIDDEN
        )

    # ---------- GET ----------
    if request.method == 'GET':
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ---------- PATCH ----------
    if request.method == 'PATCH':
        serializer = QuizSerializer(
            quiz,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
