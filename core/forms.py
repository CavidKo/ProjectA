from core.models import Contact
from django import forms


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('email', 'message')
        widgets = {
            'email': forms.EmailInput(attrs={'class': "stext-111 cl2 plh3 size-116 p-l-28 p-r-25", 'type': "text", 'name': "email", 'placeholder': "Your Email Address"}),
            'message': forms.Textarea(attrs={'class':"stext-111 cl2 plh3 size-120 p-lr-28 p-tb-25", 'name': "msg", 'placeholder': "How Can We Help?"})
        }