import os

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['text', 'image']

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        if not text:
            raise ValidationError('Post text cannot be empty.')
        if len(text) > 250:
            raise ValidationError('Posts must be 250 characters or fewer.')
        return text

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        extension = os.path.splitext(image.name)[1].lower()
        if extension not in allowed_extensions:
            raise ValidationError('Only JPG, PNG, GIF, and WEBP images are allowed.')

        if image.size > 5 * 1024 * 1024:
            raise ValidationError('Image uploads must be 5MB or smaller.')

        return image


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