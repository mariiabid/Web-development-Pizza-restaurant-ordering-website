from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, University

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    university = forms.ModelChoiceField(
        queryset=University.objects.filter(is_active=True), 
        required=False,
        empty_label=" --Select University (optional) --"

    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'university', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        university = self.cleaned_data.get('university')
        if university:
            user.university = university
            email_domain = self.cleaned_data['email'].split('@')[-1]
            if email_domain == university.email_domain:
                user.is_verified_student = True
        
        if commit:
            user.save()
        return user