# Django
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib import admin
from django.contrib.auth import get_user_model


User: AbstractBaseUser = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin class for user model.
    """

    all_user_fields: tuple = ('email', 'first_name', 'last_name',
                              'is_active', 'is_staff', 'is_superuser')

    # 'email', 'first_name', 'last_name',
    # 'is_active', 'is_staff', 'is_superuser'
    fields = all_user_fields

    # 'email', 'first_name', 'last_name',
    # 'is_active', 'is_staff', 'is_superuser'
    list_display = all_user_fields

    # 'is_active', 'is_staff', 'is_superuser'
    list_filter = all_user_fields[3:6]

    # 'email', 'first_name', 'last_name',
    # 'is_active', 'is_staff', 'is_superuser'
    readonly_fields = all_user_fields
