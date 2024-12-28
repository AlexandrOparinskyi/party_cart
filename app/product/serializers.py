from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_null=True,
                                        source='get_short_description')
    slug = serializers.SlugField(read_only=True)


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    slug = serializers.SlugField(read_only=True)
    category_slug = serializers.CharField(write_only=True)
    category = CategorySerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    sale = serializers.IntegerField(validators=[MaxValueValidator(100),
                                                MinValueValidator(0)],
                                    default=0)
    image1 = serializers.ImageField()
    image2 = serializers.ImageField(allow_null=True)
    image3 = serializers.ImageField(allow_null=True)
    result_price = serializers.CharField(read_only=True,
                                         source='get_price_result')
