from django import forms 
from .models import Posts
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['text','image']

class UserRegistrationForm(UserCreationForm):
    input_class = 'w-full rounded-lg border border-[#343a43] bg-[#090b0e] p-3 focus:outline-none focus:ring-2 focus:ring-[#c6ff24]'
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': input_class,
            'placeholder': 'you@example.com',
            'autocomplete': 'email',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': self.input_class,
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': self.input_class,
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': self.input_class,
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        })

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')