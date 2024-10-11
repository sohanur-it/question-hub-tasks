from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from quizhub.models.question_models import Question

@receiver(m2m_changed, sender=Question.tags.through)
def update_question_tag_ancestors(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add' and not reverse:
        current_tags = instance.tags.all()

        for tag in current_tags:
            ancestors = tag.get_all_ancestor_tags() 
            for ancestor in ancestors:
                if not instance.tags.filter(pk=ancestor.pk).exists():
                    instance.tags.add(ancestor)