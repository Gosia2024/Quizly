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
def quiz_detail(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id, owner=request.user)
    except Quiz.DoesNotExist:
        return Response(
            {"detail": "Quiz not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = QuizSerializer(quiz)
    return Response(serializer.data)