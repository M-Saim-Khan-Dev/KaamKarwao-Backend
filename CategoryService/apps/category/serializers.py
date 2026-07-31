from .models import  Category,SubCategory
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','color','image']

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(), source='category', write_only= True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name','color','image','category','category_id','base_price']