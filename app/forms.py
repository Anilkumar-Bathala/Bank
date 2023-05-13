from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class WithdrawForm(forms.Form):
    account_number = forms.CharField(label='Account Number')
    amount = forms.DecimalField(label='Amount')


class DepositForm(forms.Form):
    account_number = forms.CharField(label='Account Number')
    amount = forms.DecimalField(label='Amount')


class TransferForm(forms.Form):
    from_account_number = forms.CharField(label='From Account Number')
    to_account_number = forms.CharField(label='To Account Number')
    amount = forms.DecimalField(label='Amount')
