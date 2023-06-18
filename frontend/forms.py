from django import forms


class RegistrationForm(forms.Form):
    """
    Form for registration.
    """

    GENDERS: tuple = (
        (1, 'male'),
        (2, 'female')
    )

    first_name: str = forms.CharField()
    last_name: str = forms.CharField()
    email: str = forms.CharField()
    password: str = forms.CharField()
    password2: str = forms.CharField()
    gender: int = forms.ChoiceField(choices=GENDERS)


class LoginForm(forms.Form):
    """
    Form for logging in.
    """

    email: str = forms.CharField()
    password: str = forms.CharField()


class ActivateAccountForm(forms.Form):
    """
    Form for account activation.
    """

    email: str = forms.CharField()
    code: str = forms.CharField()


class SendPasswordCodeForm(forms.Form):
    """
    Form for sending restore password code.
    """

    email: str = forms.CharField()


class ForgetPasswordForm(forms.Form):
    """
    Form for password restore.
    """

    email: str = forms.CharField()
    code: str = forms.CharField()
    password: str = forms.CharField()
    password2: str = forms.CharField()


class ChangePasswordForm(forms.Form):
    """
    Form for password change.
    """

    password: str = forms.CharField(label='New password')
    password2: str = forms.CharField(label='Repeat new password')
