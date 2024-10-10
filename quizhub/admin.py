from django.contrib import admin
from .models import Tag, Question

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

    list_display = ('question_text', 'tag', 'correct_option') 
    search_fields = ['question_text', 'tag']
    list_filter = ['tag']  

admin.site.register(Question, QuestionAdmin)
