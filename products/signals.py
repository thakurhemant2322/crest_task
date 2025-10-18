from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Product, ProductLog

def dict_diff(old, new):
    changes = {}
    for k in set(old) | set(new):
        if old.get(k) != new.get(k):
            changes[k] = {'old': old.get(k), 'new': new.get(k)}
    return changes

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            instance._prechange = {
                'title': old.title,
                'description': old.description,
                'price': str(old.price),
                'discount': str(old.discount),
                'image': old.image,
                'ssn': old.ssn,
                'is_active': old.is_active,
            }
        except sender.DoesNotExist:
            instance._prechange = {}

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if created:
        ProductLog.objects.create(product=instance, action='created', changes={})
    else:
        before = getattr(instance, '_prechange', {})
        after = {
            'title': instance.title,
            'description': instance.description,
            'price': str(instance.price),
            'discount': str(instance.discount),
            'image': instance.image,
            'ssn': instance.ssn,
            'is_active': instance.is_active,
        }
        ProductLog.objects.create(product=instance, action='updated', changes=dict_diff(before, after))
