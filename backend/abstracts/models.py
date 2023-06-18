# Django
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

# Python
import datetime
import typing as t


class AbstractManager(models.Manager):
    """Abstract manager for all models."""

    def get_not_deleted(self) -> QuerySet[t.Any] | None:
        """
        Get all models, where datetime_deleted is None.
        """
        queryset: QuerySet[t.Any] = \
            self.filter(datetime_deleted__isnull=True)

        return queryset

    def get_deleted(self) -> QuerySet[t.Any] | None:
        """
        Get all models, where datetine_deleted is not None.
        """
        queryset: QuerySet[t.Any] = \
            self.filter(datetime_deleted__isnull=False)

        return queryset

    def get_object_or_none(self, **filter: t.Any) -> t.Any:
        """
        Get user or None by field.
        """
        # Try to get object by filter
        try:
            obj: t.Any = self.get(**filter)

        # Set obj to None, if there is no such object
        except Exception as e:
            print(e)
            obj = None

        finally:
            return obj


class AbstractModel(models.Model):
    """Abstract model for all other models."""

    # Datetime when model was created
    datetime_created: datetime.datetime = models.DateTimeField(
        verbose_name='время создания',
        default=timezone.now,
        null=True,
        blank=True
    )
    # Datetime when model was updated
    datetime_updated: datetime.datetime = models.DateTimeField(
        verbose_name='время обновления',
        auto_now=True,
        null=True,
        blank=True
    )
    # Datetime when model was deleted
    datetime_deleted: datetime.datetime = models.DateTimeField(
        verbose_name='время удаления',
        null=True,
        blank=True
    )
    objects: AbstractManager = AbstractManager()

    class Meta:
        abstract: bool = True
