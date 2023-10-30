from django import forms
from user.models import MyUser as User


class RegisterForm(forms.ModelForm):

    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': "Re-enter password"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Username"}),
            'email': forms.EmailInput(attrs={'placeholder': "Email"}),
            'first_name': forms.TextInput(attrs={'placeholder': "First name"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Last name"}),
            'password': forms.PasswordInput(attrs={'placeholder': "Password"}),
        }
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get('password')

    #     if len(password) < 8:
    #         raise forms.ValidationError('Parol 8 simvoldan az olmamalidir!')
    #     else:
    #         return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': "Username"}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': "Password"}))