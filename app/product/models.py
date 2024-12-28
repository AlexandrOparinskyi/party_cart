from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from app.common.models import BaseModel


class Category(BaseModel):
    """
    Category model for products

    Fields:
        name (str): Category name
        description (str): Category description
        slug (str): Category URL-address

    Methods:
        get_short_description(): Returned short category description
        __str__(): Returned category name
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def get_short_description(self):
        if self.description[50] in ['.', '!', '?']:
            return self.description[:51]
        if self.description[50] == ' ':
            return f'{self.description[:50]}...'
        return f'{self.description[:51]}...'

    def __str__(self):
        return self.name


class Product(BaseModel):
    """
    Products models

    Fields:
        name (str): Product name
        slug (str): Product URL-address
        price (DecimalField): Product price
        sale (int): Product sale
        image1, image2, image3 (ImageField): Product images

    Methods:
        get_price_result(): Returns the final price of the product taking
                            into account the discount, if any
        __str__(): Returned product name
    """
    name = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from='name', unique=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_DEFAULT,
                                 default='Products',
                                 related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.IntegerField(validators=[MaxValueValidator(100),
                                           MinValueValidator(0)],
                               default=0)
    image1 = models.ImageField(upload_to='products_image')
    image2 = models.ImageField(upload_to='products_image', null=True)
    image3 = models.ImageField(upload_to='products_image', null=True)

    def get_price_result(self):
        if self.sale:
            return round(self.price - (self.price / 100 * self.sale), 2)
        return self.price

    def __str__(self):
        return self.name
