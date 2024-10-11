from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from quizhub.models.question_models import Question

@receiver(m2m_changed, sender=Question.tags.through)
def update_question_tag_ancestors(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and not reverse:
        # Get the tags directly associated with the question
        current_tags = instance.tags.all()

        # For each tag, get its ancestors and associate them with the question
        for tag in current_tags:
            ancestors = tag.get_all_ancestor_tags()  # Assuming this method returns all ancestors of the tag
            for ancestor in ancestors:
                # Check if the ancestor is not already associated with the question
                if not instance.tags.filter(pk=ancestor.pk).exists():
                    instance.tags.add(ancestor)