import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quizhub.models.question_models import Question
from quizhub.models.tag_models import Tag

class Command(BaseCommand):
    help = 'Create tags, 1000 demo questions, and a superuser for testing.'

    def handle(self, *args, **kwargs):
        # Define the tag hierarchy
        hierarchy = {
            'Parts of Speech': {
                'Noun': ['Proper Noun', 'Common Noun'],
                'Verb': ['Action Verb', 'Linking Verb'],
                'Adjective': ['Comparative', 'Superlative'],
            },
            'Tenses': {
                'Past': ['Simple Past', 'Past Continuous'],
                'Present': ['Simple Present', 'Present Continuous'],
                'Future': ['Simple Future', 'Future Continuous'],
            },
            'Vocabulary': ['Synonyms', 'Antonyms'],
            'Grammar': ['Sentence Structure', 'Punctuation'],
            'Syntax': {
                'Word Order': [],
                'Sentence Types': [],
            }
        }

        # Function to recursively create tags
        def create_tags(parent_tag, sub_tags):
            if isinstance(sub_tags, dict):
                for tag, children in sub_tags.items():
                    parent_tag_obj, _ = Tag.objects.get_or_create(tag_name=tag, parent=parent_tag)
                    create_tags(parent_tag_obj, children)
            else:
                for sub_tag in sub_tags:
                    Tag.objects.get_or_create(tag_name=sub_tag, parent=parent_tag)

        # Loop through the hierarchy and create tags
        for main_tag, sub_tags in hierarchy.items():
            main_tag_obj, _ = Tag.objects.get_or_create(tag_name=main_tag)
            create_tags(main_tag_obj, sub_tags)

        self.stdout.write(self.style.SUCCESS('Successfully created tags based on the hierarchy.'))

        # Retrieve all existing tags from the database
        tag_objects = list(Tag.objects.all())

        # Check if there are any tags available
        if not tag_objects:
            self.stdout.write(self.style.ERROR('No tags found in the database. Please create some tags first.'))
            return

        # Generate 1000 demo questions
        for i in range(1, 1001):
            question_text = f"Sample Question {i}?"
            options = [f"Option {j}" for j in range(1, 5)]  # Create 4 options

            # Randomly select the correct option as an integer
            correct_option = random.randint(1, 4)  # Randomly select an option number between 1 and 4

            # Create a new question
            question = Question.objects.create(
                question_text=question_text,
                option1=options[0],
                option2=options[1],
                option3=options[2],
                option4=options[3],
                correct_option=correct_option  # Assign the integer value for the correct option
            )

            # Assign a random tag to the question
            question.tags.add(random.choice(tag_objects))

        self.stdout.write(self.style.SUCCESS('Successfully created 1000 demo questions.'))

        # Create a superuser if it does not exist
        self.create_superuser()

    def create_superuser(self):
        User = get_user_model()

        # Check if a superuser with the provided email already exists
        if not User.objects.filter(email='admin@admin.com').exists():
            self.stdout.write(self.style.WARNING('No superuser found, creating superuser.'))
            User.objects.create_superuser(
                email='admin@admin.com',
                password='admin321'
            )
            self.stdout.write(self.style.SUCCESS('Superuser "admin@admin.com" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists, skipping superuser creation.'))
