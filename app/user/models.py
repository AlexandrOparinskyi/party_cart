from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import validate_email
from django.db import models

from app.common.models import BaseModel
from app.user.managers import CustomUserManager


class User(AbstractBaseUser, BaseModel):
    """
    Custom user model

    Fields:
        name (str): User`s name
        surname (str): User`s surname
        email (str): User`s email
        phone (str): User`s phone
        address (ForeignKey): User`s address
        created_at (DateTimeField): Account creation date
        is_admin (bool): User is admin
        is_staff (bool): User is staff

    Methods:
        get_full_name(): Returned user`s full name
        __str__(): Returned user`s full name
    """

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[validate_email])
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    def get_full_name(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return self.get_full_name()


class Address(BaseModel):
    """
    Address model for user

    Fields:
        user (ForeignKey): Owner of address
        city (str): User`s city
        street (str): User`s street
        house (str): Users`s house
        apartment (str): User`s apartment
        description (str): Additional description for the address

    Methods:
        get_full_address(): Obtaining address information
        __str__(): Returns the user's address
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='address')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=20)
    apartment = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True)

    def get_full_address(self):
        return f'{self.city}, {self.street}, {self.house}, {self.apartment}'

    def __str__(self):
        return f'Address by {self.user}'
