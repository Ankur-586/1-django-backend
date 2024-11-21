from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator

class Category(models.Model):
    category_image  = models.ImageField(upload_to='category')
    category_name = models.CharField(max_length=50, unique=True, db_index=True, 
                                     validators=[RegexValidator(r'^[a-zA-Z ]+$', 'Category name must only contain alphabetic characters')])
    category_slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description     = models.TextField(null=False, blank=False, default='')
    is_active       = models.BooleanField(default=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        # Automatically generate a slug based on the category_name if not provided
        if not self.category_slug:
            self.category_slug = slugify(self.category_name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['parent_category__id']
        
    def hide_all_subcategories(self) -> None:
        """
        -----
        Docs:
        -----
        Purpose: Recursively hides all subcategories of the current category.
        Process: Iterates through each subcategory, sets its hidden status to True, saves the subcategory, 
                 and then calls itself to handle further subcategories.
        """
        for subcategory in self.subcategories.all():
            subcategory.is_active = False
            subcategory.save()
            subcategory.hide_all_subcategories()  # Recursively hide subcategories
            
    def unhide_all_subcategories(self) -> None:
        """
        -----
        Docs:
        -----
        Purpose: Recursively unhides all subcategories of the current category.
        Process: Iterates through each subcategory, sets its hidden status to False, saves the subcategory, 
                 and then calls itself to handle further subcategories.
        """
        for subcategory in self.subcategories.all():
            subcategory.is_active = True
            subcategory.save()
            subcategory.unhide_all_subcategories()  # Recursively unhide subcategories
        
