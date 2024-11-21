from rest_framework import serializers
from .models import *
from category.serializers import CategorySerializer

class TagSerializer(serializers.ModelSerializer):
    # collect_tags = 
    class Meta:
        model = Tag
        fields = ['name']

class MetaSerializer(serializers.ModelSerializer):
    metadata = serializers.JSONField()
    class Meta:
        model = Meta
        fields = ['metadata']
        
class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['name','rate']

class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImages
        fields = ['image', 'alt_text', 'order']

class ProductVariantSerializer(serializers.ModelSerializer):
    variant_images = ProductVariantImageSerializer(source='images', many=True, read_only=True)  # Change `images` to `variant_images`
    meta = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariants
        fields = ['id', 'variant_name', 'sku', 'price', 'weight', 'stock', 
                  'proudct_variant_stock', 'variant_images','meta']
        
    def get_meta(self, obj):
        return obj.meta_data.get_metadata() if obj.meta_data else {}

class ProductSerializer(serializers.ModelSerializer):
    
    category = serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True, read_only=True)
    variant_images  = ProductVariantImageSerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True)
    meta = serializers.SerializerMethodField()
    tax = TaxSerializer()
    
    def get_category(self, obj):
        return {
            'id': obj.category.id,
            'category_name': obj.category.category_name,
            'category_slug': obj.category.category_slug,
            'category_image': obj.category.category_image.url if obj.category.category_image.url else None
        }

    def get_meta(self, obj):
        return obj.meta_data.get_metadata() if obj.meta_data else {}
    
    class Meta:
        model = Product
        fields = [
            'id','product_name', 'product_slug', 'created_at', 'updated_at', 'thumbnail', 
            'description', 'tax', 'variant_images', 'category', 'variants', 'tags', 
            'product_stock', 'meta', 'minimum_order_quantity', 'maximum_order_quantity'
        ]
    
    
