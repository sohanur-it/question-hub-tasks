from rest_framework import serializers
from quizhub.models.question_models import Question
from quizhub.models.tag_models import Tag
from rest_framework import serializers

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'question_text',
            'option1',
            'option2',
            'option3',
            'option4',
            'correct_option'
        ]

class TagWithQuestionsSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    question_lists = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Tag
        fields = [
            'id',
            'tag_name',
            'question_count',
            'question_lists'
        ]

    def get_question_lists(self, obj):
        request = self.context.get('request')
        page_size = int(request.query_params.get('page_size', 10)) 
        page = int(request.query_params.get('page', 1))

        questions = obj.questions.all().order_by('id')

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_questions = questions[start_index:end_index]
        return QuestionSerializer(paginated_questions, many=True).data
    
    def get_question_count(self, instance):
        count = instance.questions.count()
        return count



class TagSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    # favorite_count = serializers.SerializerMethodField()
    # read_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'tag_name', 'parent', 'level', 'question_count']

    def get_question_count(self, instance):
        # Get all ancestor tags including the current tag
        count = instance.questions.count()
        return count
    


class UserTagSerializer(serializers.ModelSerializer):
    favorite_question_count = serializers.IntegerField(read_only=True)
    read_question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = [
            'id',
            'tag_name',
            'favorite_question_count',
            'read_question_count'
        ]




