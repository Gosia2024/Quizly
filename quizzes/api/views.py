"""
API Views for the Quizzes application.
Handles the logic for creating, listing, and managing quizzes, 
integrating the AI processing pipeline with the Django database.
"""
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Quiz

from .serializers import QuizSerializer
from ..utils import (
    normalize_youtube_url,
    download_audio,
    transcribe_audio,
    build_prompt,
    generate_quiz_json
)
from ..models import Quiz, Question, QuestionOption
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    """
    Main endpoint to generate a quiz from a YouTube URL.
    
    Pipeline:
    1. Validates and normalizes the YouTube URL.
    2. Downloads audio and transcribes it.
    3. Requests a JSON-structured quiz.
    4. Saves the quiz, questions, and options in a single atomic transaction.
    """
    url = request.data.get("url")

    if not url:
        return Response({"detail": "URL required"}, status=400)

    # normalize URL
    try:
        clean_url = normalize_youtube_url(url)
    except ValueError:
        return Response({"detail": "Invalid YouTube URL"}, status=400)

    # AI FLOW
    audio_path = download_audio(clean_url)
    transcript = transcribe_audio(audio_path)
    prompt = build_prompt(transcript)
    quiz_data = generate_quiz_json(prompt)

    # SAVE
    with transaction.atomic():
        quiz = Quiz.objects.create(
            title=quiz_data["title"],
            description=quiz_data["description"],
            video_url=clean_url,
            owner=request.user
        )

        for q in quiz_data["questions"]:
            question = Question.objects.create(
                quiz=quiz,
                question_title=q["question_title"],
                answer=q["answer"]
            )

            for opt in q["question_options"]:
                QuestionOption.objects.create(
                    question=question,
                    option_text=opt
                )

    serializer = QuizSerializer(quiz)
    return Response(serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_quizzes(request):
    """
    Returns a list of all quizzes owned by the currently authenticated user.
    """
    quizzes = Quiz.objects.filter(owner=request.user)
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, quiz_id):
    """
    Retrieve, update, or delete a specific quiz.
    Includes ownership verification (403 Forbidden if accessing someone else's quiz).
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)
# Ownership check
    if quiz.owner != request.user:
        return Response(
            {"detail": "Access denied - quiz does not belong to user"},
            status=status.HTTP_403_FORBIDDEN
        )

# GET: Return full quiz details including questions
    if request.method == 'GET':
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
 # PATCH: Partial update of quiz fields (title, description, etc.)
    if request.method == 'PATCH':
        serializer = QuizSerializer(quiz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# DELETE: Permanently remove the quiz from the database
    if request.method == 'DELETE':
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)