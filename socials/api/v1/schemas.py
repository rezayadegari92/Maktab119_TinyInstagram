"""
OpenAPI schemas for socials API endpoints using drf-spectacular
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


# Post List Schema
post_list_schema = extend_schema(
    summary="List all posts",
    description="Get a list of all posts. Can be filtered by tags and location. Only shows posts from public profiles or followed private profiles.",
    parameters=[
        OpenApiParameter(
            name='tags',
            description='Filter posts by tag name',
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name='location',
            description='Filter posts by location (partial match)',
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY
        )
    ],
    responses={
        200: {
            'description': 'List of posts',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': 1,
                            'user': 'johndoe',
                            'images': [
                                {
                                    'id': 1,
                                    'image': '/media/posts/image1.jpg',
                                    'image_type': 'post',
                                    'created_at': '2023-01-01T12:00:00Z'
                                }
                            ],
                            'caption': 'Beautiful sunset!',
                            'is_liked': True,
                            'comments': [],
                            'likes': [],
                            'like_count': 5,
                            'created_at': '2023-01-01T12:00:00Z'
                        }
                    ]
                }
            }
        }
    },
    tags=['Posts']
)


# Post Create Schema
post_create_schema = extend_schema(
    summary="Create a new post",
    description="Create a new post with images and caption. Upload images using the image_files field.",
    responses={
        201: {
            'description': 'Post created successfully',
            'content': {
                'application/json': {
                    'example': {
                        'id': 1,
                        'user': 'johndoe',
                        'images': [],
                        'caption': 'Beautiful sunset!',
                        'is_liked': False,
                        'comments': [],
                        'likes': [],
                        'like_count': 0,
                        'created_at': '2023-01-01T12:00:00Z'
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - validation errors'
        }
    },
    tags=['Posts']
)


# Post Detail Schema
post_detail_schema = extend_schema(
    summary="Get post details",
    description="Retrieve detailed information about a specific post",
    responses={
        200: {
            'description': 'Post details',
            'content': {
                'application/json': {
                    'example': {
                        'id': 1,
                        'user': 'johndoe',
                        'images': [
                            {
                                'id': 1,
                                'image': '/media/posts/image1.jpg',
                                'image_type': 'post',
                                'created_at': '2023-01-01T12:00:00Z'
                            }
                        ],
                        'caption': 'Beautiful sunset!',
                        'is_liked': True,
                        'comments': [],
                        'likes': [],
                        'like_count': 5,
                        'created_at': '2023-01-01T12:00:00Z'
                    }
                }
            }
        },
        404: {
            'description': 'Post not found'
        }
    },
    tags=['Posts']
)


# Post Update Schema
post_update_schema = extend_schema(
    summary="Update a post",
    description="Update caption, location, or replace images of your own post. If new images are provided, old images will be deleted and replaced with new ones. Supports multipart/form-data for image uploads. Both PUT and PATCH methods supported. Only the post owner can update.",
    responses={
        200: {
            'description': 'Post updated successfully',
            'content': {
                'application/json': {
                    'example': {
                        'id': 1,
                        'user': 'johndoe',
                        'images': [
                            {
                                'id': 1,
                                'image': '/media/posts/image1.jpg',
                                'image_type': 'post',
                                'created_at': '2023-01-01T12:00:00Z'
                            }
                        ],
                        'caption': 'Updated caption!',
                        'location': 'New York',
                        'is_liked': False,
                        'comments': [],
                        'likes': [],
                        'like_count': 5,
                        'created_at': '2023-01-01T12:00:00Z'
                    }
                }
            }
        },
        403: {
            'description': 'Permission denied - not the post owner'
        },
        404: {
            'description': 'Post not found'
        }
    },
    tags=['Posts']
)


# Post Delete Schema
post_delete_schema = extend_schema(
    summary="Delete a post",
    description="Delete your own post. Only the post owner can delete.",
    responses={
        204: {
            'description': 'Post deleted successfully'
        },
        403: {
            'description': 'Permission denied - not the post owner'
        },
        404: {
            'description': 'Post not found'
        }
    },
    tags=['Posts']
)


# Like Post Schema
like_post_schema = extend_schema(
    summary="Like a post",
    description="Like a post. Can only like posts from public profiles or followed private profiles.",
    responses={
        201: {
            'description': 'Post liked successfully',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'post liked :)'
                    }
                }
            }
        },
        200: {
            'description': 'Already liked',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'you already like this :)'
                    }
                }
            }
        },
        404: {
            'description': 'Post not found'
        }
    },
    tags=['Posts']
)


# Unlike Post Schema
unlike_post_schema = extend_schema(
    summary="Unlike a post",
    description="Remove your like from a post",
    responses={
        200: {
            'description': 'Like removed successfully',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'like removed :)'
                    }
                }
            }
        },
        404: {
            'description': 'Post not found or like not found'
        }
    },
    tags=['Posts']
)


# Comment Create Schema
comment_create_schema = extend_schema(
    summary="Add a comment to a post",
    description="Add a comment to a post. Can only comment on posts from public profiles or followed private profiles.",
    responses={
        201: {
            'description': 'Comment created successfully',
            'content': {
                'application/json': {
                    'example': {
                        'id': 1,
                        'user': 'johndoe',
                        'text': 'Great post!',
                        'like_count': 0,
                        'is_liked': False,
                        'created_at': '2023-01-01T12:00:00Z'
                    }
                }
            }
        },
        400: {
            'description': 'Bad request - validation errors'
        },
        404: {
            'description': 'Post not found'
        }
    },
    tags=['Comments']
)


# Comment Delete Schema
comment_delete_schema = extend_schema(
    summary="Delete a comment",
    description="Delete your own comment. Only the comment owner can delete.",
    responses={
        200: {
            'description': 'Comment deleted successfully',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'comment deleted :)'
                    }
                }
            }
        },
        403: {
            'description': 'Permission denied - not the comment owner'
        },
        404: {
            'description': 'Comment not found'
        }
    },
    tags=['Comments']
)


# Follow User Schema
follow_user_schema = extend_schema(
    summary="Follow a user",
    description="Follow another user to see their posts even if their profile is private",
    responses={
        201: {
            'description': 'User followed successfully',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'user followed successfully'
                    }
                }
            }
        },
        200: {
            'description': 'Already following',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'you already follow this user'
                    }
                }
            }
        },
        400: {
            'description': 'Cannot follow yourself'
        },
        404: {
            'description': 'User not found'
        }
    },
    tags=['Follow']
)


# Unfollow User Schema
unfollow_user_schema = extend_schema(
    summary="Unfollow a user",
    description="Unfollow a user you are currently following",
    responses={
        200: {
            'description': 'User unfollowed successfully',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'user unfollowed successfully'
                    }
                }
            }
        },
        404: {
            'description': 'User not found or not following'
        }
    },
    tags=['Follow']
)


# Followers List Schema
followers_list_schema = extend_schema(
    summary="Get user's followers",
    description="Get a list of users who follow the specified user",
    responses={
        200: {
            'description': 'List of followers',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': 1,
                            'username': 'follower1',
                            'email': 'follower1@example.com'
                        }
                    ]
                }
            }
        },
        404: {
            'description': 'User not found'
        }
    },
    tags=['Follow']
)


# Following List Schema
following_list_schema = extend_schema(
    summary="Get user's following",
    description="Get a list of users that the specified user is following",
    responses={
        200: {
            'description': 'List of following',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': 1,
                            'username': 'following1',
                            'email': 'following1@example.com'
                        }
                    ]
                }
            }
        },
        404: {
            'description': 'User not found'
        }
    },
    tags=['Follow']
)

