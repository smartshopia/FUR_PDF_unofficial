from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, CustomUser, PDF

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'gender']

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['title', 'file']

class CustomSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class UploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.pdf', '.jpg', '.png')):
            raise forms.ValidationError("Only PDF, JPG, and PNG files are allowed.")
        return file
