import json
from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# from .models import User

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'sex', 'dob', 'active', 'staff', 'admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class DateInput(forms.DateInput):
    input_type = "date"



class ProfileForm(forms.ModelForm):
    
    
    CATEGORY_CHOICES = [
        ('', 'Select'),
        ("Teacher", 'Teacher'),
        ("Student", 'Student'),
    ]

    LOS_CHOICES = [
        ('', 'Select'),
        ("Primary", 'Primary'),
        ("Secondary", 'Secondary'),
        ("Tertiary", 'Tertiary'),
    ]

    CLASS_CHOICES = [
        ('', 'Select'),
        ("1st Grade", '1st Grade'),
        ("2nd Grade", '2nd Grade'),
        ("3rd Grade", '3rd Grade'),
        ("4th Grade", '4th Grade'),
        ("5th Grade", '5th Grade'),
        ("6th Grade", '6th Grade'),
        ("7th Grade (jss1)", '7th Grade (jss1)'),
        ("8th Grade (jss2)", '8th Grade (jss2)'),
        ("9th Grade (jss3)", '9th Grade (jss3)'),
        ("10th Grade (ss1)", '10th Grade (ss1)'),
        ("11th Grade (ss2)", '11th Grade (ss2)'),
        ("12th Grade (ss3)", '12th Grade (ss3)'),
        ("1st Year", '1st Year'),
        ("2nd Year", '2nd Year'),
        ("3rd Year", '3rd Year'),
        ("4th Year", '4th Year'),
        ("5th Year", '5th Year'),
        ("6th Year", '6th Year'),
        ("7th Year", '7th Year'),
        ("Matsers/PHD", 'Matsers/PHD'),
    ]

    SEX_CHOICES = [
        ('', 'Select'),
        ("Male", 'Male'),
        ("Female", 'Female'),
    ]

    user_type = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(
            attrs={
                "col": 4,
                "placeholder" : "Select Your Category",
                "class" : "form-control", 
                "id" : "user_type",
            }
        )
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter first name",
                "class" : "form-control", 
                "id" : "first_name",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter last name",
                "class" : "form-control", 
                "id" : "last_name",
            }
        )
    )

    dob = forms.DateField(
        # input_formats=['%Y/%m/%d'],
        widget=DateInput(
            format="%Y-%m-%d",
            attrs={
            "col" : 4,
            "class": "form-control",
            "id" : "dob"
            }
        )
    )

    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        widget=forms.Select(
            attrs={
                "col": 4,
                "placeholder" : "Select Your Sex",
                "class" : "form-control", 
                "id" : "sex",
            }
        )
    )


    age = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Age",
                "class" : "form-control", 
                "id" : "age",
                "readonly" : True
            }
        )
    )

    countrys = forms.ChoiceField(
        required=False,
        choices= [('', 'Select')],
        widget=forms.Select(
            attrs={
                "col": 6,
                "placeholder" : "Select Your Country of Residence",
                "class" : "form-control", 
                "id" : "country",
            }
        )
    )

    

    los = forms.ChoiceField(
        choices=LOS_CHOICES,
        widget=forms.Select(
            attrs={
                "col": 4,
                "placeholder" : "Select Your Level of Study",
                "class" : "form-control", 
                "id" : "los",
            }
        )
    )

    los_class = forms.ChoiceField(
        choices=CLASS_CHOICES,
        widget=forms.Select(
            attrs={
                "col": 4,
                "placeholder" : "Select Your Class",
                "class" : "form-control", 
                "id" : "class",
            }
        )
    )

    school = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter School Name",
                "class" : "form-control", 
                "id" : "school",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Email",
                "class" : "form-control", 
                "id" : "email",
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Username",
                "class" : "form-control", 
                "id" : "Username",
                "readonly" : True
            }
        )
    )

    telephone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Telephone",
                "class" : "form-control", 
                "id" : "telephone",
            }
        )
    )

    facebook = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Facebook",
                "class" : "form-control", 
                "id" : "Facebook",
            }
        )
    )

    twitter = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Twitter",
                "class" : "form-control", 
                "id" : "Twitter",
            }
        )
    )

    instagram = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Instagram",
                "class" : "form-control", 
                "id" : "Instagram",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "col": 6,
                "class" : "form-control", 
                "id" : "form_password"
            }
        )
    )

    password2 = forms.CharField(
        label ="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "col": 6,
                "class" : "form-control", 
                "id" : "form_password2"
            }
        )
    )

    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "col": 6,
                "class" : "form-control", 
                "id" : "profile_photo"
            }
        )
    )

    country = forms.CharField(
        required=False,
        label ="",
        widget=forms.HiddenInput(
            attrs={
                "col": 12,
                "placeholder" : "Select Your Country of Residence",
                "class" : "form-control", 
                "id" : "country-val",
            }
        )
    )

    state = forms.CharField(
        required=False,
        label ="",
        widget=forms.HiddenInput(
            attrs={
                "col": 12,
                "placeholder" : "Select Your state",
                "class" : "form-control", 
                "id" : "state-val",
            }
        )
    )



    class Meta:
        model = User
        fields = ('user_type', 'first_name', 'last_name', 'sex', 'dob', 'age', 'countrys', 'los', 'los_class', 'school', 'email',  'username', 'telephone', 'facebook', 'twitter', 'instagram', 'password', 'password2', 'profile_photo', 'country','state',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.frip = instance
        if instance and instance.pk:
            # print(self.fields['state'].choices)
            # self.fields['country'].choices[1][1] = county
            self.fields['password'].required = False
            self.fields['password2'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists() and self.instance.pk is None:
            raise forms.ValidationError("Email is taken")
        return email
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        ctry    = country.split("-")
        return ctry[0]

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.capitalize()

    def clean(self):
        data = self.cleaned_data
        print(data)
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("passwords must match. ")
        return data

    

    

    