from django.contrib import admin
from .models import *

class ProductVariantInline(admin.TabularInline):
    model = ProductVariants
    extra = 1

class VariantImageInline(admin.TabularInline):
    model = VariantImages
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    prepopulated_fields = {'product_slug': ('product_name',)} #need to define slug inside producty field
    list_display = ('product_name', 'price', 'tax', 'category','is_active','product_stock')
    list_editable = ('is_active',)
    list_filter = ('available_on', 'updated_at', 'category', 'tags')
    search_fields = ('product_name', 'description', 'category__name', 'tags__name')
    ordering = ('-updated_at',)

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product_class', 'display', 'name')
    search_fields = ('display', 'name')

@admin.register(ProductVariants)
class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [VariantImageInline]
    list_display = ('id', 'product', 'variant_name', 'sku', 'price',
                    'stock', 'proudct_variant_stock', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('product__name', 'variant_name')

@admin.register(VariantImages)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'image', 'alt_text', 'order')
    search_fields = ('product__name','product_variant')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ('metadata', 'created_at', 'updated_at')
    search_fields = ('metadata',)


# suppose i want to create a django project which has a role and user model. what all fields should be there. 
# Role should be not in a drop down but as a fk

