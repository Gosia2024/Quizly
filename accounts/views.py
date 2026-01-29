from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    confirmed_password = request.data.get('confirmed_password')
    email = request.data.get('email')

    # 1. Validate input data
    if not username or not password or not confirmed_password or not email:
        return Response(
            {"detail": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. Check if passwords match
    if password != confirmed_password:
        return Response(
            {"detail": "Passwords do not match"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 3. Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # 4. Check if email already exists
    if User.objects.filter(email=email).exists():
        return Response(
            {"detail": "Email already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 5. Create User
    User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    # 6. Return success response
    return Response(
        {"detail": "User created successfully!"},
        status=status.HTTP_201_CREATED
    )






@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  
def login_user(request):
    print("LOGIN VIEW CALLED")

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"detail": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    response = Response(
           {
            "detail": "Login successfully!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        },
        status=status.HTTP_200_OK
    )
    

    response.set_cookie(
        key='access_token',
        value=str(access),
        httponly=True,
        secure=False,   # Prduction True
        samesite='Lax'
    )

    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite='Lax'
    )


    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_user(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {"detail": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response(
            {
              "detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
            },
            status=status.HTTP_200_OK
        )

        # Usuń cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

    except Exception:
        return Response(
            {"detail": "Invalid token"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response(
            {"detail": "Refresh token missing"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        token = RefreshToken(refresh_token)
        new_access = token.access_token

        response = Response(
            {
                "detail": "Token refreshed",
                "access": str(new_access)
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key='access_token',
            value=str(new_access),
            httponly=True,
            secure=False,   # production -> True
            samesite='Lax'
        )

        return response

    except Exception:
        return Response(
            {"detail": "Refresh token invalid"},
            status=status.HTTP_401_UNAUTHORIZED
        )
