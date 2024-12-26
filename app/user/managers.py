from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager

    Methods:
        create_user(): Create a user
        create_superuser(): Create a superuser
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and eturned a user
        """
        if not email:
            return ValueError('Email is a required field')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        """
        Create and returned a superuser. Fields is_staff, is_admin
        and is_active become True
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            return ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_admin') is not True:
            return ValueError('Superuser must have is_admin=True')

        return self.create_user(email, password, **extra_fields)
