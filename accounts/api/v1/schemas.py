"""
OpenAPI schemas for accounts API endpoints using drf-spectacular
"""
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
    inline_serializer
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


# Register User Schema
register_user_schema = extend_schema(
    summary="Register a new user",
    description="Send registration data and receive OTP code via email for verification",
    request=inline_serializer(
        name='RegisterRequest',
        fields={
            'email': serializers.EmailField(help_text='Your email address for registration'),
            'username': serializers.CharField(help_text='Choose a unique username (3-35 characters)'),
            'password': serializers.CharField(help_text='Create a strong password (min 8 characters)', style={'input_type': 'password'}),
            'first_name': serializers.CharField(help_text='Your first name'),
            'last_name': serializers.CharField(help_text='Your last name'),
            'birth_date': serializers.DateField(help_text='Your birth date (YYYY-MM-DD format)'),
            'phone_number': serializers.CharField(required=False, help_text='Your phone number (optional)'),
        }
    ),
    responses={
        200: {
            'description': 'OTP sent successfully',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'OTP sent to your email.',
                        'email': 'user@example.com'
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - validation errors',
            'content': {
                'application/json': {
                    'example': {
                        'email': ['This field is required.'],
                        'username': ['A user with that username already exists.']
                    }
                }
            }
        }
    },
    tags=['Authentication']
)


# Verify OTP Schema
verify_otp_schema = extend_schema(
    summary="Verify OTP and complete registration",
    description="Verify the OTP code sent to email, create user account, and return JWT tokens for authentication.",
    responses={
        201: {
            'description': 'Registration completed successfully with JWT tokens',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'Registration successful.',
                        'user': {
                            'id': 1,
                            'email': 'user@example.com',
                            'username': 'johndoe',
                            'first_name': 'John',
                            'last_name': 'Doe',
                            'birth_date': '1990-01-01',
                            'phone_number': '+1234567890'
                        },
                        'tokens': {
                            'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                            'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Invalid or expired OTP, or registration session expired',
            'content': {
                'application/json': {
                    'examples': {
                        'invalid_otp': {
                            'value': {'error': 'Invalid or expired OTP.'}
                        },
                        'session_expired': {
                            'value': {'error': 'Registration session expired. Please register again.'}
                        },
                        'user_exists': {
                            'value': {'error': 'User with this email already exists.'}
                        }
                    }
                }
            }
        }
    },
    tags=['Authentication']
)


# Profile View Schema
profile_view_schema = extend_schema(
    summary="Get authenticated user's profile",
    description="Retrieve profile information for the currently authenticated user (automatically determined from JWT token). Includes user's posts with full details.",
    responses={
        200: {
            'description': 'Profile retrieved successfully',
            'content': {
                'application/json': {
                    'example': {
                        'id': 1,
                        'user': 'johndoe',
                        'website': 'https://example.com',
                        'bio': 'Hello, I am John!',
                        'profile_picture': '/media/profile_pictures/john.jpg',
                        'location': 'New York',
                        'is_private': False,
                        'posts': [
                            {
                                'id': 1,
                                'user': 'johndoe',
                                'caption': 'My first post',
                                'images': [
                                    {'id': 1, 'image': '/media/posts/image1.jpg', 'image_type': 'post'}
                                ],
                                'like_count': 10,
                                'is_liked': False,
                                'created_at': '2025-10-11T08:00:00Z'
                            }
                        ]
                    }
                }
            }
        },
        404: {
            'description': 'Profile not found',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Profile not found.'
                    }
                }
            }
        },
        401: {
            'description': 'Authentication credentials were not provided'
        }
    },
    tags=['Profile']
)


# Update Profile Schema
update_profile_schema = extend_schema(
    summary="Update authenticated user's profile",
    description="Update profile information for the currently authenticated user (automatically determined from JWT token). Supports both POST and PATCH methods.",
    request=inline_serializer(
        name='UpdateProfileRequest',
        fields={
            'website': serializers.URLField(required=False, help_text='Your website URL'),
            'bio': serializers.CharField(required=False, help_text='Tell us about yourself'),
            'location': serializers.CharField(required=False, help_text='Your location'),
            'is_private': serializers.BooleanField(required=False, help_text='Make profile private'),
            'profile_picture': serializers.ImageField(required=False, help_text='Upload profile picture'),
        }
    ),
    responses={
        200: {
            'description': 'Profile updated successfully',
            'content': {
                'application/json': {
                    'example': {
                        'message': 'Profile updated successfully.',
                        'profile': {
                            'id': 1,
                            'user': 'johndoe',
                            'website': 'https://example.com',
                            'bio': 'Updated bio',
                            'location': 'New York',
                            'is_private': False
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Profile not found',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Profile not found.'
                    }
                }
            }
        },
        401: {
            'description': 'Authentication credentials were not provided'
        }
    },
    tags=['Profile']
)


# Profile List Schema
profile_list_schema = extend_schema(
    summary="List all profiles",
    description="Get a list of all user profiles with search capability by username. Posts data is excluded for better performance.",
    parameters=[
        OpenApiParameter(
            name='search',
            description='Search profiles by username',
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY
        )
    ],
    responses={
        200: {
            'description': 'List of profiles without posts data',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': 1,
                            'user': 'johndoe',
                            'website': 'https://example.com',
                            'bio': 'Hello!',
                            'profile_picture': '/media/profile_pictures/john.jpg',
                            'location': 'New York',
                            'is_private': False
                        },
                        {
                            'id': 2,
                            'user': 'janedoe',
                            'website': 'https://jane.com',
                            'bio': 'Photography enthusiast',
                            'profile_picture': '/media/profile_pictures/jane.jpg',
                            'location': 'Los Angeles',
                            'is_private': True
                        }
                    ]
                }
            }
        }
    },
    tags=['Profile']
)


# Profile Detail Schema
profile_detail_schema = extend_schema(
    summary="Get profile details by ID",
    description="Retrieve detailed profile information for a specific profile ID. Includes posts data.",
    responses={
        200: {
            'description': 'Profile details with posts',
            'content': {
                'application/json': {
                    'example': {
                        'id': 1,
                        'user': 'johndoe',
                        'website': 'https://example.com',
                        'bio': 'Hello, I am John!',
                        'profile_picture': '/media/profile_pictures/john.jpg',
                        'location': 'New York',
                        'is_private': False,
                        'posts': [
                            {
                                'id': 1,
                                'user': 'johndoe',
                                'caption': 'Beautiful sunset',
                                'images': [],
                                'like_count': 10,
                                'is_liked': False
                            }
                        ]
                    }
                }
            }
        },
        404: {
            'description': 'Profile not found'
        }
    },
    tags=['Profile']
)


# Login Schema
login_schema = extend_schema(
    summary="User login",
    description="Authenticate user with email and password. Returns only JWT access and refresh tokens.",
    request=inline_serializer(
        name='LoginRequest',
        fields={
            'email': serializers.EmailField(help_text='Your registered email address'),
            'password': serializers.CharField(help_text='Your account password', style={'input_type': 'password'}),
        }
    ),
    responses={
        200: {
            'description': 'Login successful - returns JWT tokens only',
            'content': {
                'application/json': {
                    'example': {
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid credentials',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Invalid email or password'
                    }
                }
            }
        }
    },
    tags=['Authentication']
)


# Token Refresh Schema
token_refresh_schema = extend_schema(
    summary="Refresh access token",
    description="Use refresh token to get a new access token. Access tokens expire after 1 day.",
    responses={
        200: {
            'description': 'New access token generated',
            'content': {
                'application/json': {
                    'example': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                }
            }
        },
        401: {
            'description': 'Invalid or expired refresh token',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Token is invalid or expired'
                    }
                }
            }
        }
    },
    tags=['Authentication']
)



