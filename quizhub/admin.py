from django.contrib import admin
from quizhub.models.question_models import Question, ReadQuestion, FavoriteQuestion
from quizhub.models.tag_models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'parent', 'level')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Tag.objects.all().order_by('level', 'tag_name')
            form_field = super().formfield_for_foreignkey(db_field, request, **kwargs)
            form_field.label_from_instance = lambda obj: obj.get_parent_hierarchy()
            return form_field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Tag, TagAdmin)



class QuestionAdmin(admin.ModelAdmin):
    # Display the question text, tags (as a list), and correct option
    list_display = ('question_text', 'get_tags', 'correct_option') 
    search_fields = ['question_text', 'tags__tag_name']  # Search by question text or tag name
    list_filter = ['tags']  # Filter by tags

    # Method to display tags in list_display
    def get_tags(self, obj):
        return ", ".join([tag.tag_name for tag in obj.tags.all()])  # Join the tag names as a string

    get_tags.short_description = 'Tags'  # Column name in the admin list view

# Register the Question model with the updated QuestionAdmin
admin.site.register(Question, QuestionAdmin)

@admin.register(FavoriteQuestion)
class FavoriteQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_favorite')  # Customize display fields
    list_filter = ('is_favorite',)  # Add filter based on favorite status
    search_fields = ('user__email', 'question__title')  # Add search functionality for user and question

@admin.register(ReadQuestion)
class ReadQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_read')  # Customize display fields
    list_filter = ('is_read',)  # Add filter based on read status
    search_fields = ('user__email', 'question__title')  # Add search functionality for user and question