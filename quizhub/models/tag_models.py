from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    level = models.PositiveIntegerField(default=0, editable=False)


    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super(Tag, self).save(*args, **kwargs)

    def get_parent_hierarchy(self):
        if self.parent:
            return f"{self.parent.get_parent_hierarchy()} --> {self.tag_name}"
        return self.tag_name
    
    def get_all_ancestor_tags(self):
        ancestors = [self]
        parent = self.parent
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors
    
    def get_all_child_tags(self):
        children = list(self.children.all())  # Get the immediate children
        for child in children:
            children.extend(child.get_all_child_tags())  # Recursively get children of each child
        return children
    

    def get_question_count(self):
        # Count questions directly linked to this tag
        count = self.questions.count()

        # Add counts from all ancestor tags
        for ancestor in self.get_all_ancestor_tags():
            count += ancestor.questions.count()

        return count
    
    def __str__(self):
        return self.get_parent_hierarchy()