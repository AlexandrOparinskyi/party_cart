from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from app.common.utils import update_model
from app.product.models import Category, Product
from app.product.serializers import CategorySerializer, ProductSerializer

category_tags = ['Category']
products_tags = ['Products']


class CategoryAPIView(APIView):
    """
    Views to get al create a categories
    """
    serializer_class = CategorySerializer

    @extend_schema(
        summary='Get categories',
        description='View to get all categories',
        tags=category_tags
    )
    def get(self, request):
        categories = Category.objects.all()

        if not categories:
            return Response({'message': 'Categories not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create a new categories',
        description='View to create a new categories',
        tags=category_tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = Category.objects.create(**serializer.validated_data)
            serializer = self.serializer_class(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class CategoryBySlugAPIView(APIView):
    """
    Views to get, update or delete a category
    """
    serializer_class = CategorySerializer

    def get_object(self, category_slug):
        try:
            category = Category.objects.get(slug=category_slug)
            self.check_object_permissions(self.request, category)
            return category
        except Category.DoesNotExist:
            return None

    @extend_schema(
        summary='Get a category',
        description='View to get category by slug',
        tags=category_tags,
        operation_id='get_category'
    )
    def get(self, request, *args, **kwargs):
        category_slug = kwargs.get('slug')
        category = self.get_object(category_slug)

        if not category:
            return Response({'message': f'Category with slug '
                                             f'{category_slug} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Update a category',
        description='View to update a category by slug',
        tags=category_tags,
        operation_id='update_category'
    )
    def put(self, request, *args, **kwargs):
        category_slug = kwargs.get('slug')
        category = self.get_object(category_slug)

        if not category:
            return Response({'message': f'Category with slug '
                                             f'{category_slug} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = update_model(category, serializer.validated_data)
            category.save()
            serializer = self.serializer_class(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Delete a category',
        description='View to delete a category by slug',
        tags=category_tags,
        operation_id='delete_category'
    )
    def delete(self, request, *args, **kwargs):
        category_slug = kwargs.get('slug')
        category = self.get_object(category_slug)

        if not category:
            return Response({'message': f'Category with slug '
                                             f'{category_slug} not found'},
                            status=status.HTTP_404_NOT_FOUND)

        category.is_active = False
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ProductsAPIView(APIView):
    """
    Views to get and create a products
    """
    serializer_class = ProductSerializer

    @extend_schema(
        summary='Get products',
        description='View to get all products',
        tags=products_tags
    )
    def get(self, request):
        products = Product.objects.select_related('category').all()

        if not products:
            return Response({'message': 'Products not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create a new products',
        description='View to create a new products',
        tags=products_tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            category_slug = data.pop('category_slug')
            category = Category.objects.get(slug=category_slug)
            product = Product.objects.create(category=category, **data)
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ProductBySlugAPIView(APIView):
    """
    Views to get, update and delete product by slug
    """
    serializer_class = ProductSerializer

    def get_object(self, product_slug):
        try:
            product = Product.objects.get(slug=product_slug)
            self.check_object_permissions(self.request, product)
            return product
        except Product.DoesNotExist:
            return None

    @extend_schema(
        summary='Get product',
        description='View to get products by slug',
        tags=products_tags,
        operation_id='get_product'
    )
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = self.get_object(product_slug)

        if not product:
            return Response({'message': f'Product with slug {product_slug}'
                                        f' not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Update product',
        description='View to update products by slug',
        tags=products_tags,
        operation_id='update_product'
    )
    def put(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = self.get_object(product_slug)

        if not product:
            return Response({'message': f'Product with slug {product_slug}'
                                        f' not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = update_model(product, serializer.validated_data)
            product.save()
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Update product',
        description='View to update products by slug',
        tags=products_tags,
        operation_id='delete_product'
    )
    def delete(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = self.get_object(product_slug)

        if not product:
            return Response({'message': f'Product with slug {product_slug}'
                                        f' not found'},
                            status=status.HTTP_404_NOT_FOUND)

        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ProductByCategoryAPIView(APIView):
    """
    View to get all products by category
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary='Get products by category',
        description='View to get all products by category slug',
        tags=products_tags
    )
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get('category_slug'))
        products = Product.objects.filter(category=category)

        if not products.exists():
            return Response({'message': f'Products with category slug '
                                        f'{category} not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
