from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):

    # Use forms.EmailField for automatic email validation tihs is inbuilt django validator
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password does not match")
        

    class Meta:
        model = User
        fields = ['email','first_name','last_name']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter your first name"    
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter your last name"
        self.fields['email'].widget.attrs['placeholder'] = "Enter your email"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'