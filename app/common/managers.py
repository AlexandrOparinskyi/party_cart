from django.db import models


class IsActiveQuerySet(models.QuerySet):
    """
    Custom QuerySet which, when deleted, changes the field is_active=False.
    If you pass the hard_delete key to the delete method, the entry will
    be completely deleted
    """

    def delete(self, hard_delete=False):
        if hard_delete:
            super().delete()
        else:
            return self.update(is_active=False)


class IsActiveManager(models.Manager):
    """
    Custom manager for receiving records with the is_active=True field
    """

    def get_queryset(self):
        return IsActiveQuerySet(self.model).filter(is_active=True)

    def unfiltered(self):
        return IsActiveQuerySet(self.model)

    def hard_delete(self):
        """
        Completely deleting a record from the database
        """
        return self.unfiltered().delete(hard_delete=True)

