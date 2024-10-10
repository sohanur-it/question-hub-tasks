from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# models.py

from django.db import models

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
    
    def __str__(self):
        return self.get_parent_hierarchy()



class Question(models.Model):
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['created_at']),
    #     ]
    
    def __str__(self):
        return self.question_text[:50]


class FavoriteQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')
        indexes = [
            models.Index(fields=['user', 'question']),
        ]


class ReadQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'question')
        indexes = [
            models.Index(fields=['user', 'question']),
        ]
