# Python
import re
import typing as t

# Local
from .models import (
    AccountCode,
    TokenWhiteList,
)

# Django
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model


User: AbstractBaseUser = get_user_model()


def email_validation_error(email: str, find_user: bool = False,
                           allowed_domains: list = settings.ALLOWED_DOMAINS,
                           raise_exception: bool = False
                           ) -> dict | None:
    """
    Return errors if user's email is match next criteria :

    * Email must starts with a letter
    * Email must include at least 2 characters in main part
    * Email domain part must be in allowed_domains list

>>> allowed_domains = ['inbox.ru', 'mail.ru', 'list.ru', 'gmail.com']

    * If there is user not found and `find_user = True`, raise an error.

    Return dict of errors or None.
    """
    pattern: str = r'^[^\d\s]\w+@(\w+.\w+$)'
    # Create pattern: starts with letter, has at least
    # 2 characters in main part and domain in
    # settings ALLOWED_DOMAINS
    validation: list = re.findall(pattern=pattern, string=email)
    error: dict = {'email': []}

    # If email doesn't match pattern
    if not validation:
        err: str = ('Email must starts with a letter and include'
                    ' at least two characters in main part.')
        error['email'].append(err)
    # If email's domain not allowed
    elif validation[0] not in allowed_domains:
        err: str = 'Domain %s is not allowed.' % validation[0]
        error['email'].append(err)
    # If find_user flag is on, check if there user with such email
    if find_user is True:
        user: User | None = User.objects.get_object_or_none(email=email)
        if user is None:
            error = {'email': ['User with such email was not found.']}
        elif user.is_active is False:
            error = {'email': ['User is not active.']}

    # If there any errors and flag raise_exception is on, raise exception
    if error.get('email') and raise_exception is True:
        raise ValidationError(error)

    # Return errors or None
    return error if error.get('email') else None


def password_validation_error(password1: str,
                              password2: str = None,
                              user: User = None,
                              raise_exception: bool = False
                              ) -> dict | None:
    """
    Return errors if passwords are not match criteria :

    * password doesn't match user's old password
    * passwords length is greater than 6
    * passwords contain letters AND numbers
    * password1 is equal to password2

    Return dict of errors or None.
    """
    error: dict = {'password': []}

    # If the new password is the same as it was before
    if isinstance(user, AbstractBaseUser):
        if user.check_password(password1):
            err: str = 'The password cannot match the old one.'
            error['password'].append(err)
    # If password length less than 7 (minimal length - 7)
    if len(password1) < 7:
        err: str = 'Password length must be greater or equal to 7.'
        error['password'].append(err)
    # If password contains only numbers or letters
    if password1.isalpha() or password1.isdigit():
        err: str = 'Password must contain both numbers and letters.'
        error['password'].append(err)
    # If password1 doesn't match password2
    if password2 and password1 != password2:
        err: str = 'Password mismatch.'
        error['password'].append(err)
        error.update({'password2': ['Password mismatch.']})

    # If there any errors and flag raise_exception is on, raise exception
    if error.get('password') and raise_exception is True:
        raise ValidationError(error)

    # Return errors or None
    return error if error.get('password') else None


def login_data_validation_error(email: str, password: str, user: User,
                                raise_exception: bool = False
                                ) -> dict | None:
    """
    Return errors if login data is invalid. Check if email,

    password are not empty and user is authenicated.
    """
    error: dict = {}
    is_admin: bool = False

    # If user was found
    if user:

        # Define if user is admin
        is_admin = user.is_admin

        # Create suberrors dict
        suberror: dict = {'email': []}

        # If user is not admin and is_admin flag is on
        if not user.is_admin and is_admin is True:
            err: str = 'Admin panel is for admins only.'
            suberror['email'].append(err)

        # If user is not active
        if user.is_active is False:
            err: str = 'You must activate your account first.'
            suberror['email'].append(err)

        # If there are suberrors, add it in main errors dict
        if suberror.get('email'):
            error.update(suberror)

    # If email is empty
    if not email:
        error.update({'email': ['This field is required.']})

    # If password is empty
    if not password:
        error.update({'password': ['This field is required.']})

    # If user was not found
    if user is None and email and password:
        error.update({'email': 'User was not found.'})
        error.update({'password': 'User was not found.'})

    # If there any errors and flag raise_exception is on, raise exception
    if error and raise_exception is True:
        raise ValidationError(error)

    # Return errors or None
    return error if error else None


def is_email_confirmed(email: str, raise_exception: bool = False
                       ) -> dict | User | t.Literal['update', 'create']:
    """
    Check if user's email confirmation is still

    in progress or new authhroization is available.

    ---
    * if active user is found

    Return dict of errors.

    ---
    * If raise_exceptions is True

    Raise errors.

    ---
    * If not active user is found

    Return update.

    ---
    * If user is not found, return `create`

    Return create.
    """
    error: dict = {}

    user: User | None
    if user := User.objects.get_object_or_none(email=email):

        # If user is already confirmed
        if user.is_active:
            error: dict = {'email': ['User with this email already exists.']}

        # Define that we should update user
        else:
            return 'update'

    # Define that we should create user
    else:
        return 'create'

    # If there any errors and flag raise_exception is on, raise exception
    if raise_exception is True:
        if error:
            raise ValidationError(error)
        return user

    # Return errors
    return error


def user_code_validation(user: User, code: str, code_type: int,
                         raise_exception: bool = False) -> dict | None:
    """
    Find user and check if it has not expired code.

    User with this email must be not active, code

    must be not expired and be owned by user.

    Return doct of errors or None.
    """
    error: dict = {}

    # Looks for code with a valid lifetime and that matches the user
    activation_code: QuerySet[AccountCode] =\
        AccountCode.objects.extended_filter(user=user, expired=False,
                                            code=code, code_type=code_type)
    # Check if there such codes
    if activation_code.exists() is False:
        error.update({'code': ['This code is invalid.']})

    # If user is None, should only raise an error about a user not found
    if user is None:
        error = {'email': ['User with this email wasn\'t found.']}

    # If user is active, should only raise an error
    # about user is already confirmed
    elif user.is_active and code_type == AccountCode.ACCOUNT_ACTIVATION:
        error = {'email': ['User with this email is already confirmed.']}

    # If there any errors and flag raise_exception is on, raise exception
    if raise_exception is True:
        if error:
            raise ValidationError(error)
        return activation_code.last()

    # Return errors or None
    return error if error else None


def refresh_token_validation_error(token: str, ip: str, fingerprint: str,
                                   raise_exception: bool = False
                                   ) -> dict | None:
    """
    Validate refresh token.
    """
    error: dict = {}

    # Check if refresh token is valid
    is_valid: bool = \
        TokenWhiteList.objects.find_valid(token=token, ip=ip,
                                          fingerprint=fingerprint).exists()

    # If not valid and function should raise exception
    if not is_valid and raise_exception is True:
        error: dict = {
            'refresh': ['Refresh token is not valid.']
        }
        raise ValidationError(error)

    return error if error else None


def gender_validation_error(gender: str, raise_exception: bool = False
                            ) -> dict | None:
    """
    Check if user gender is valid.
    """
    error: dict = {}

    # Check if there any gender
    if not gender:
        error['gender'] = ['This field may not be blank.']

    # Check if gender is not valid
    elif gender not in (1, 2):
        error['gender'] = ['Gender is not allowed.']

    # If not valid and function should raise exception
    if error and raise_exception is True:
        raise ValidationError(error)

    return error if error else None
