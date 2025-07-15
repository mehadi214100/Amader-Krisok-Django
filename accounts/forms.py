from django import forms
from .models import User,UserProfile
from django.core.exceptions import ValidationError
from officers.models import Officer

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields = ['first_name','phone_number','email','password1','password2']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email already exists")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password does not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"]) 
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ['user']

        widgets = {
            "date_of_birth" : forms.DateInput(attrs={"type":'date',"class":"form-control"}),
            "gender":forms.Select(attrs={"class":"form-control"}),
            "city":forms.TextInput(attrs={"class":"form-control"}),
            "address":forms.Textarea(attrs={"class":"form-control"})
        }

class OfficerProfileForm(forms.ModelForm):
    class Meta:
        model = Officer
        fields = [
            'nid_number', 'date_of_birth', 'education', 'institution',
            'graduation_year', 'specialization', 'experience', 'workplace',
            'designation', 'joining_date', 'days_available',
            'time_available', 'bio', 'profile_picture','is_available'
        ]
        widgets = {
            'nid_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'education': forms.Select(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'days_available': forms.Select(attrs={'class': 'form-control'}),
            'time_available': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }