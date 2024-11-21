from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction

from category.models import Category
from product.models import Product, ProductVariants

"""
Signal handler for updating the 'is_active' status of a Category instance.
"""
@receiver(pre_save, sender=Category)
def update_is_active_status(sender, instance, **kwargs):
    '''
    This function listens for pre-save signals from the Category model. If the 
    'is_active' status of an existing category is changed, it either deactivates 
    or activates the category, along with its associated products and product 
    variants. It also manages the visibility of all subcategories.
    '''
    if instance.pk:
        try:
            old_instance = Category.objects.get(pk=instance.pk)
        except Category.DoesNotExist:
            return  # Optionally log this

        if old_instance.is_active != instance.is_active:
            with transaction.atomic():
                if not instance.is_active:
                    deactivate_category(instance)
                else:
                    activate_category(instance)

def deactivate_category(instance):
    ''' 
    Hides subcategories and marks products and product variants as inactive. 
    '''
    instance.hide_all_subcategories()  # Hide all subcategories
    # Bulk update products and their variants
    Product.objects.filter(category=instance).update(is_active=False)
    ProductVariants.objects.filter(product__category=instance).update(is_active=False)

def activate_category(instance):
    '''
    Unhides subcategories and marks products and product variants as active.
    '''
    instance.unhide_all_subcategories()  # Unhide all subcategories
    # Bulk update products and their variants
    Product.objects.filter(category=instance).update(is_active=True)
    ProductVariants.objects.filter(product__category=instance).update(is_active=True)
