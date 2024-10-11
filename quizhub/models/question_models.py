from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Question(models.Model):
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    tags = models.ManyToManyField('quizhub.Tag', related_name='questions')


    def __str__(self):
        return self.question_text

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question_text[:50]


class FavoriteQuestion(models.Model):
    user = models.ForeignKey(User, related_name='favorite_questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='favorites', on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'question')
        indexes = [
            models.Index(fields=['user', 'question']),
        ]


class ReadQuestion(models.Model):
    user = models.ForeignKey(User, related_name='read_questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='read', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'question')
        indexes = [
            models.Index(fields=['user', 'question']),
        ]