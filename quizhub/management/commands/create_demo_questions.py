import random
from django.core.management.base import BaseCommand
from quizhub.models import Question, Tag  # Replace 'your_app' with the actual app name

class Command(BaseCommand):
    help = 'Create 1000 demo questions for testing.'

    def handle(self, *args, **kwargs):
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
