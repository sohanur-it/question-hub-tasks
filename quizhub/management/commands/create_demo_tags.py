from django.core.management.base import BaseCommand
from quizhub.models import Tag

class Command(BaseCommand):
    help = 'Create tags based on the English Language hierarchy.'

    def handle(self, *args, **kwargs):
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
        def create_tags(parent_name, sub_tags):
            if isinstance(sub_tags, dict):
                for tag, children in sub_tags.items():
                    parent_tag, _ = Tag.objects.get_or_create(tag_name=tag, parent=parent_name)
                    create_tags(parent_tag, children)
            else:
                for sub_tag in sub_tags:
                    Tag.objects.get_or_create(tag_name=sub_tag, parent=parent_name)

        # Loop through the hierarchy and create tags
        for main_tag, sub_tags in hierarchy.items():
            main_tag_obj, _ = Tag.objects.get_or_create(tag_name=main_tag)
            create_tags(main_tag_obj, sub_tags)

        self.stdout.write(self.style.SUCCESS('Successfully created tags based on the hierarchy.'))
