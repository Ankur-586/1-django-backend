from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    # subcategories = serializers.ListField(child=serializers.CharField(), source='subcategories.all', read_only=True)
    category_slug = serializers.SlugField(required=False)
    
    class Meta:
        model = Category
        fields = ('id', 'category_image', 'category_name', 'category_slug', 'description','subcategories')

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True, context=self.context).data

    def create(self, validated_data):
        """
        Override the default create method to handle category creation,
        including setting the parent_category if provided.
        """
        # Extract parent category (if present) and other fields
        parent_category_data = validated_data.pop('parent_category', None)

        # Create the category instance with validated data
        category = Category.objects.create(**validated_data)

        # If a parent category is provided, link it to the new category
        if parent_category_data:
            try:
                parent_category = Category.objects.get(id=parent_category_data.id)
                category.parent_category = parent_category
                category.save()
            except Category.DoesNotExist:
                raise serializers.ValidationError(f"Parent category with ID {parent_category_data.id} does not exist.")
        
        return category
'''     
i want a end point suppose if i hit subcategories i get all the sub categories 
and i hit category i get all category and sub category. if i hit the sub 
category and pass category id then i should get category 
'''