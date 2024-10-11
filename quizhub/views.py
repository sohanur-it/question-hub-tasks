from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import TagSerializer, QuestionSerializer, UserTagSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from quizhub.models.question_models import Question
from quizhub.models.tag_models import Tag

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 
    max_page_size = 100


class QuestionsUnderTagView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


    @swagger_auto_schema(
        security=[{'BearerAuth': []}]  # This line is important for Swagger to recognize the security
    )
    def get(self, request, tag_id):
        user = request.user
        
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            raise NotFound('Tag not found')

        tags = Tag.objects.annotate(
            favorite_question_count=Count(
                'questions__favorites',
                filter=Q(questions__favorites__user=user, questions__favorites__is_favorite=True)
            ),
            read_question_count=Count(
                'questions__read',
                filter=Q(questions__read__user=user, questions__read__is_read=True)
            )
        ).order_by('id')

        questions = tag.questions.all()
        total_questions_count = questions.count()

        # Apply read filter
        is_read = request.query_params.get('is_read')
        if is_read is not None:
            if is_read.lower() == 'true':
                questions = questions.filter(read__is_read=True, read__user=user)
            elif is_read.lower() == 'false':
                questions = questions.exclude(read__is_read=True, read__user=user)

        # Apply favorite filter
        is_favorite = request.query_params.get('is_favorite')
        if is_favorite is not None:
            if is_favorite.lower() == 'true':
                questions = questions.filter(favorites__is_favorite=True, favorites__user=user)
            elif is_favorite.lower() == 'false':
                questions = questions.exclude(favorites__is_favorite=True, favorites__user=user)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_questions = paginator.paginate_queryset(questions, request)

        # Serialize the paginated questions
        serializer = QuestionSerializer(paginated_questions, many=True)
        
        # Prepare the response data
        response_data = {
            'tag_id': tag.id,
            'tag_name': tag.tag_name,
            'total_questions_count': total_questions_count,
            'favorite_question_count': tags.get(pk=tag_id).favorite_question_count,
            'read_question_count': tags.get(pk=tag_id).read_question_count,
            'questions': serializer.data,
        }

        return paginator.get_paginated_response(response_data)


class TagsWithQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'is_read',
                openapi.IN_QUERY,
                description="Filter questions based on read status. Use 'true' or 'false'.",
                type=openapi.TYPE_BOOLEAN,
                required=False
            ),
            openapi.Parameter(
                'is_favorite',
                openapi.IN_QUERY,
                description="Filter questions based on favorite status. Use 'true' or 'false'.",
                type=openapi.TYPE_BOOLEAN,
                required=False
            ),
        ]
    )

    def get(self, request):
        user = request.user
        
        is_read = request.query_params.get('is_read')
        is_favorite = request.query_params.get('is_favorite')

        parent_tags = Tag.objects.filter(parent__isnull=True).prefetch_related('children').annotate(
            favorite_question_count=Count(
                'questions__favorites',
                filter=Q(questions__favorites__user=user, questions__favorites__is_favorite=True)
            ),
            read_question_count=Count(
                'questions__read',
                filter=Q(questions__read__user=user, questions__read__is_read=True)
            )
        ).order_by('id')

        response_data = []

        def build_tag_data(tag):
            questions = tag.questions.all()

            # Apply read filter
            if is_read is not None:
                if is_read.lower() == 'true':
                    questions = questions.filter(read__is_read=True, read__user=user)
                elif is_read.lower() == 'false':
                    questions = questions.exclude(read__is_read=True, read__user=user)

            # Apply favorite filter
            if is_favorite is not None:
                if is_favorite.lower() == 'true':
                    questions = questions.filter(favorites__is_favorite=True, favorites__user=user)
                elif is_favorite.lower() == 'false':
                    questions = questions.exclude(favorites__is_favorite=True, favorites__user=user)

            # Paginate the questions
            paginator = self.pagination_class()
            paginated_questions = paginator.paginate_queryset(questions, request)

            # Serialize the paginated questions
            question_serializer = QuestionSerializer(paginated_questions, many=True)

            tag_data = {
                'tag_id': tag.id,
                'tag_name': tag.tag_name,
                'favorite_question_count': tag.favorite_question_count,
                'read_question_count': tag.read_question_count,
                'total_questions_count': questions.count(),
                'questions': question_serializer.data,
                'children': []
            }

            child_tags = tag.children.all().annotate(
                favorite_question_count=Count(
                    'questions__favorites',
                    filter=Q(questions__favorites__user=user, questions__favorites__is_favorite=True)
                ),
                read_question_count=Count(
                    'questions__read',
                    filter=Q(questions__read__user=user, questions__read__is_read=True)
                )
            )

            for child_tag in child_tags:
                tag_data['children'].append(build_tag_data(child_tag))

            return tag_data

        for tag in parent_tags:
            response_data.append(build_tag_data(tag))

        return Response(response_data, status=200)


class ParentTagsAPIView(APIView):
    def get(self, request):
        parent_tags = Tag.objects.filter(parent__isnull=True)
        serializer = TagSerializer(parent_tags, many=True)
        return Response(serializer.data)


class TagsWithQuestionCountAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all().annotate(question_count=Count('questions')).order_by('id')
        serializer = TagSerializer(tags, many=True, context={'include_question_count': True})
        return Response(serializer.data)


class TagsWithUserQuestionStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        tags = Tag.objects.all().annotate(
            favorite_question_count=Count(
                'questions__favorites',
                filter=Q(questions__favorites__user=user, questions__favorites__is_favorite=True)
            ),
            read_question_count=Count(
                'questions__read',
                filter=Q(questions__read__user=user, questions__read__is_read=True)
            )
        ).order_by('id')

        serializer = UserTagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagsWithNestedCountsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get nested tag counts",
        responses={
            200: openapi.Response(
                description="A list of parent tags with their children and question counts",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'tag_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'tag_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'favorite_question_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'read_question_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'total_questions_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'children': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        user = request.user

        # Get parent tags and their counts
        parent_tags = Tag.objects.filter(parent__isnull=True).prefetch_related('children').annotate(
            favorite_question_count=Count(
                'questions__favorites',
                filter=Q(questions__favorites__user=user, questions__favorites__is_favorite=True)
            ),
            read_question_count=Count(
                'questions__read',
                filter=Q(questions__read__user=user, questions__read__is_read=True)
            )
        ).order_by('id')

        response_data = []

        def build_tag_data(tag):
            # Create tag data without including questions
            tag_data = {
                'tag_id': tag.id,
                'tag_name': tag.tag_name,
                'favorite_question_count': tag.favorite_question_count,
                'read_question_count': tag.read_question_count,
                'total_questions_count': tag.questions.count(),  # Total questions count
                'children': []
            }

            # Get child tags and their counts
            child_tags = tag.children.annotate(
                favorite_question_count=Count(
                    'questions__favorites',
                    filter=Q(questions__favorites__user=user, questions__favorites__is_favorite=True)
                ),
                read_question_count=Count(
                    'questions__read',
                    filter=Q(questions__read__user=user, questions__read__is_read=True)
                )
            )

            for child_tag in child_tags:
                tag_data['children'].append(build_tag_data(child_tag))

            return tag_data

        for tag in parent_tags:
            response_data.append(build_tag_data(tag))

        return Response(response_data, status=200)
