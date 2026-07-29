from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # read_only = ['created_at']
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class MinimalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
        
class ProductSerializer(serializers.ModelSerializer):
    # category_obj = MinimalCategorySerializer(read_only=True, source='category')
    # image = serializers.SerializerMethodField(read_only=True)
    # category_obj = serializers.SerializerMethodField(read_only=True)  
    
    # def get_category_obj(self, obj):
    #     return {
    #         "id": obj.category.id,
    #         "name": obj.category.name,
    #     }
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            image_url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(image_url)
            return image_url
        return None
    
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] =  MinimalCategorySerializer(instance.category).data
        representation['image'] = self.get_image(instance)
        return representation
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'quantity', 'category', 'image']