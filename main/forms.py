from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm, LoginForm
from .models import Word, UserProfile


class WordLookupForm(forms.Form):
    """Form for looking up a word."""
    word = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter a French or English word...',
            'autofocus': True
        }),
        label='Word',
        help_text='Enter a word in French or English'
    )


class WordForm(forms.ModelForm):
    """Form for editing word details."""
    class Meta:
        model = Word
        fields = ['cefr_level']  # Only CEFR level is editable
        widgets = {
            'cefr_level': forms.Select(attrs={'class': 'form-select'}),
        }


class CustomSignupForm(SignupForm):
    """Custom signup form with nickname and language preferences."""
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('zh', 'Chinese (Mandarin)'),
        ('ja', 'Japanese'),
        ('fr', 'French'),
    ]
    
    nickname = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your nickname',
        }),
        label='Nickname',
        help_text='Choose a nickname to display on your profile'
    )
    
    native_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=True,
        initial='en',
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Native Language',
        help_text='Your native language (used for explanations)'
    )
    
    target_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=True,
        initial='fr',
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Learning Language',
        help_text='Language you want to learn'
    )
    
    def save(self, request):
        """Save the user and create their profile with nickname and language preferences."""
        user = super().save(request)
        
        # Create or update user profile with nickname and language preferences
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'nickname': self.cleaned_data['nickname'],
                'native_language': self.cleaned_data['native_language'],
                'target_language': self.cleaned_data['target_language'],
            }
        )
        if not created:
            profile.nickname = self.cleaned_data['nickname']
            profile.native_language = self.cleaned_data['native_language']
            profile.target_language = self.cleaned_data['target_language']
            profile.save()
        
        return user


class CustomLoginForm(LoginForm):
    """Custom login form that uses nickname instead of email."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change the login field label and placeholder
        self.fields['login'].label = 'Nickname'
        self.fields['login'].widget.attrs.update({
            'placeholder': 'Enter your nickname',
            'autofocus': True
        })
        # Remove help text that mentions email
        self.fields['login'].help_text = ''
    
    def clean_login(self):
        """Override to look up user by nickname instead of email."""
        nickname = self.cleaned_data.get('login')
        
        if nickname:
            # Try to find user by nickname through UserProfile
            try:
                profile = UserProfile.objects.get(nickname__iexact=nickname)
                # Return the associated user's email for allauth authentication
                return profile.user.email
            except UserProfile.DoesNotExist:
                # If nickname not found, try as email for backward compatibility
                # or raise validation error
                try:
                    User.objects.get(email__iexact=nickname)
                    return nickname  # It's an email, use it directly
                except User.DoesNotExist:
                    raise forms.ValidationError(
                        "No account found with this nickname."
                    )
        
        return nickname


class ProfileSettingsForm(forms.ModelForm):
    """Form for editing user profile settings."""
    
    class Meta:
        model = UserProfile
        fields = ['nickname', 'avatar', 'native_language', 'target_language']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your nickname',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'native_language': forms.Select(attrs={
                'class': 'form-select',
            }),
            'target_language': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].label = 'Nickname'
        self.fields['avatar'].label = 'Profile Picture'
        self.fields['native_language'].label = 'Native Language'
        self.fields['target_language'].label = 'Learning Language'
