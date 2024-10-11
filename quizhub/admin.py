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
    list_display = ('question_text', 'get_tags', 'correct_option') 
    search_fields = ['question_text', 'tags__tag_name'] 
    list_filter = ['tags']  

    def get_tags(self, obj):
        return ", ".join([tag.tag_name for tag in obj.tags.all()]) 

    get_tags.short_description = 'Tags'  


admin.site.register(Question, QuestionAdmin)

@admin.register(FavoriteQuestion)
class FavoriteQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_favorite')  
    list_filter = ('is_favorite',)  
    search_fields = ('user__email', 'question__title') 

@admin.register(ReadQuestion)
class ReadQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_read')  
    list_filter = ('is_read',)  
    search_fields = ('user__email', 'question__title') 