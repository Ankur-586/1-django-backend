from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name','category_slug','category_image','description','parent_category','is_active') 
    list_editable = ('is_active',)
    search_fields = ('category_name', 'slug')
    prepopulated_fields = {'category_slug':('category_name',)}
    ordering = ('parent_category',)
