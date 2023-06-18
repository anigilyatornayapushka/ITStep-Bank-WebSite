# Django
from django.contrib import admin

# Local
from .models import (
    Transaction,
    Card,
)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin model for transaction.
    """

    # All fields
    fields = ('card_sender', 'card_receiver', 'currency')

    # Fields to display in table
    list_display = fields

    # Unchangable fields
    readonly_fields = fields


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """
    Admin model for card.
    """

    # All fields
    fields = ('number', 'user')

    # Fields to display in table
    list_display = fields

    # Unchangable fields
    readonly_fields = fields
