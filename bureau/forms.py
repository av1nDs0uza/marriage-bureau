from django import forms
from .models import Profile

BOOLEAN_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)

class Step1Form(forms.ModelForm):  # Form Meta & Personal Info
    class Meta:
        model = Profile
        fields = ['full_name', 'branch', 'gender', 'caste', 'dob']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'branch': forms.Select(),
            'gender': forms.Select(),
            'caste': forms.TextInput(),
        }

class Step2Form(forms.ModelForm):  # Birth, Physical, Cultural, Education
    class Meta:
        model = Profile
        fields = [
            'birth_place', 'birth_time', 'birth_day', 'nakshatra',
            'height_ft', 'height_in', 'weight', 'color', 'blood_group',
            'mother_tongue', 'taluka', 'district', 'religion', 'gotra',
            'kuldaivat', 'deity', 'subcaste', 'education', 'profession',
            'monthly_income', 'job_address'
        ]
        widgets = {
            'birth_place': forms.TextInput(),
            'birth_time': forms.TimeInput(attrs={'type': 'time'}),
            'birth_day': forms.TextInput(),
            'nakshatra': forms.TextInput(),
            'height_ft': forms.NumberInput(),
            'height_in': forms.NumberInput(),
            'weight': forms.NumberInput(),
            'color': forms.Select(),
            'blood_group': forms.Select(),
            'mother_tongue': forms.TextInput(),
            'taluka': forms.TextInput(),
            'district': forms.TextInput(),
            'religion': forms.Select(),
            'gotra': forms.TextInput(),
            'kuldaivat': forms.TextInput(),
            'deity': forms.TextInput(),
            'subcaste': forms.TextInput(),
            'education': forms.TextInput(),
            'profession': forms.TextInput(),
            'monthly_income': forms.NumberInput(),
            'job_address': forms.Textarea(attrs={'rows': 2}),
        }

class Step3Form(forms.ModelForm):  # Contact & Family Info
    class Meta:
        model = Profile
        fields = [
            'whatsapp_number',
            'phone_number_1', 'phone_number_2', 'phone_number_3', 'phone_number_4',
            'father_name', 'father_alive',
            'mother_name', 'mother_alive',
            'mother_maiden_name', 'mother_maiden_village',
            'brothers', 'brothers_married', 'sisters', 'sisters_married',
        ]
        widgets = {
            'whatsapp_number': forms.TextInput(attrs={'type': 'tel', 'required': True}),
            'phone_number_1': forms.TextInput(attrs={'type': 'tel', 'required': True}),
            'phone_number_2': forms.TextInput(attrs={'type': 'tel'}),
            'phone_number_3': forms.TextInput(attrs={'type': 'tel'}),
            'phone_number_4': forms.TextInput(attrs={'type': 'tel'}),
            'father_name': forms.TextInput(attrs={'required': True}),
            'father_alive': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'mother_name': forms.TextInput(attrs={'required': True}),
            'mother_alive': forms.RadioSelect(choices=BOOLEAN_CHOICES),
            'mother_maiden_name': forms.TextInput(),
            'mother_maiden_village': forms.TextInput(),
            'brothers': forms.NumberInput(),
            'brothers_married': forms.NumberInput(),
            'sisters': forms.NumberInput(),
            'sisters_married': forms.NumberInput(),
        }


class Step4Form(forms.ModelForm):  # Horoscope & Marriage Preference
    class Meta:
        model = Profile
        fields = [
            'raasi', 'horoscope_nakshatra', 'gan', 'nadi', 'charan',
            'horoscope_seen', 'manglik_status', 'preferred_marriage_type'
        ]
        widgets = {
            'raasi': forms.TextInput(),
            'horoscope_nakshatra': forms.TextInput(),
            'gan': forms.TextInput(),
            'nadi': forms.TextInput(),
            'charan': forms.TextInput(),
            'horoscope_seen': forms.CheckboxInput(),
            'manglik_status': forms.RadioSelect(),
            'preferred_marriage_type': forms.Select(),
        }

class Step5Form(forms.ModelForm):  # Declaration, Address, Images
    declaration = forms.BooleanField(
        required=True,
        label="I confirm that all provided information is true."
    )
    declaration_name = forms.CharField(
        required=True,
        label="Full Name"
    )
    declaration_phone = forms.CharField(
        required=True,
        label="Phone",
        widget=forms.TextInput(attrs={'type': 'tel'})
    )
    declaration_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Profile
        fields = [
            'residential_address', 'other_info',
            'profile_image', 'aadhar_image', 'supporting_document',
            'declaration', 'declaration_name', 'declaration_phone', 'declaration_date'
        ]
        widgets = {
            'residential_address': forms.Textarea(attrs={'rows': 3}),
            'other_info': forms.Textarea(attrs={'rows': 2}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': '.jpg,.jpeg,.png'}),
            'aadhar_image': forms.ClearableFileInput(attrs={'accept': '.jpg,.jpeg,.png'}),
            'supporting_document': forms.ClearableFileInput(attrs={'accept': '.jpg,.jpeg,.png'}),
            'declaration_date': forms.DateInput(attrs={'type': 'date'}),
        }

class Step6Form(forms.Form):
    accept = forms.BooleanField(
        required=True,
        label="I have read and agree to the Terms and Conditions."
    )
