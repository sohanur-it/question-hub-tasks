from django.urls import path
from .views import (
    ParentTagsAPIView,
    TagsWithQuestionCountAPIView,
    TagsWithQuestionView,
    QuestionsUnderTagView,
    TagsWithUserQuestionStatsAPIView,
    TagsWithNestedCountsView,
)

urlpatterns = [
    # API endpoint to display all parent tags
    path('parents/', ParentTagsAPIView.as_view(), name='parent-tags'),

    # API endpoint to show all tags with their respective question with nested tags
    #filter with  <?is_read=true & is_favorite=true>
    path('nested-with-questions/', TagsWithQuestionView.as_view(), name='tags-with-products'),

    # API endpoint to retrieve questions under a specific tag by tag ID
    path('<int:tag_id>/with-questions/', QuestionsUnderTagView.as_view(), name='questions-under-tag'),

    # Show the nested counts for child, grandchild, and great-grandchild tags
    path('child-tag-lists/', TagsWithNestedCountsView.as_view(), name='tags-nested-counts'),

    # API endpoint to get the count of questions for each tag
    path('with-questions-count/', TagsWithQuestionCountAPIView.as_view(), name='tags-with-questions-count'),

    # API endpoint to retrieve user-specific question statistics for all tags
    path('user-question-stats/', TagsWithUserQuestionStatsAPIView.as_view(), name='user-question-stats'),
]


