from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

User = get_user_model()

def validate_image(image):
    max_size = 2 * 1024 * 1024  # 2MB
    allowed_formats = ['JPEG', 'JPG', 'PNG']

    if image.size > max_size:
        raise ValidationError("Image file too large ( > 2MB ).")

    try:
        img = Image.open(image)
        if img.format.upper() not in allowed_formats:
            raise ValidationError("Unsupported image format. Use JPEG or PNG.")
    except Exception:
        raise ValidationError("Invalid image file.")

def compress_image(image):
    img = Image.open(image)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.thumbnail((600, 600))  # Resize
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=80)
    file_name = image.name.rsplit('.', 1)[0] + "_compressed.jpg"
    return ContentFile(buffer.getvalue(), name=file_name)


class Profile(models.Model):
    BRANCH_CHOICES = [
        ('Pimpalgaon', 'Pimpalgaon'),
        ('Ghatsila', 'Ghatsila'),
        ('Vidur', 'Vidur'),
        ('Vidhata', 'Vidhata'),
    ]

    GENDER_CHOICES = [('Groom', 'Groom'), ('Bride', 'Bride')]

    COMPLEXION_CHOICES = [
        ('Fair', 'Fair'),
        ('Wheatish', 'Wheatish'),
        ('Dark', 'Dark'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    RELIGION_CHOICES = [
        ('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'),
        ('Buddhist', 'Buddhist'), ('Jain', 'Jain'), ('Other', 'Other'),
    ]

    MARRIAGE_TYPE_CHOICES = [
        ('Mutual', 'Mutual understanding'),
        ('Registered', 'Registered'),
        ('Vedic', 'Traditional/Vedic'),
    ]

    MANGLIK_CHOICES = [('Yes', 'Yes'), ('No', 'No'), ('Mild', 'Mild')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    form_no = models.CharField(max_length=20, editable=False, unique=True)
    date_filled = models.DateField(auto_now_add=True)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    full_name = models.CharField(max_length=100)

    # Personal Details
    caste = models.CharField(max_length=100)
    dob = models.DateField()
    birth_place = models.CharField(max_length=100)
    birth_time = models.TimeField()
    birth_day = models.CharField(max_length=20, blank=True)
    nakshatra = models.CharField(max_length=100, blank=True)
    height_ft = models.IntegerField()
    height_in = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50, choices=COMPLEXION_CHOICES, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)

    mother_tongue = models.CharField(max_length=50)
    taluka = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    religion = models.CharField(max_length=50, choices=RELIGION_CHOICES)
    gotra = models.CharField(max_length=50, blank=True)
    kuldaivat = models.CharField(max_length=50, blank=True)
    deity = models.CharField(max_length=50, blank=True)
    subcaste = models.CharField(max_length=50, blank=True)

    education = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    monthly_income = models.PositiveIntegerField()
    job_address = models.TextField(blank=True)

    # Contact
    whatsapp_number = models.CharField(max_length=15)
    phone_number_1 = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15, blank=True)
    phone_number_3 = models.CharField(max_length=15, blank=True)
    phone_number_4 = models.CharField(max_length=15, blank=True)

    # Family
    father_name = models.CharField(max_length=100)
    father_alive = models.BooleanField(default=True)
    mother_name = models.CharField(max_length=100)
    mother_alive = models.BooleanField(default=True)
    mother_maiden_name = models.CharField(max_length=100, blank=True)
    mother_maiden_village = models.CharField(max_length=100, blank=True)
    brothers = models.PositiveIntegerField(default=0)
    brothers_married = models.PositiveIntegerField(default=0)
    sisters = models.PositiveIntegerField(default=0)
    sisters_married = models.PositiveIntegerField(default=0)

    # Horoscope
    horoscope_file = models.FileField(upload_to='horoscopes/', blank=True, null=True)
    raasi = models.CharField(max_length=100, blank=True)
    horoscope_nakshatra = models.CharField(max_length=100, blank=True)
    gan = models.CharField(max_length=100, blank=True)
    nadi = models.CharField(max_length=100, blank=True)
    charan = models.CharField(max_length=100, blank=True)
    horoscope_seen = models.BooleanField(default=False)
    manglik_status = models.CharField(max_length=20, choices=MANGLIK_CHOICES, blank=True)

    preferred_marriage_type = models.CharField(max_length=20, choices=MARRIAGE_TYPE_CHOICES)
    residential_address = models.TextField()
    other_info = models.TextField(blank=True)

    # Declaration
    declaration = models.BooleanField(default=False)
    declaration_name = models.CharField(max_length=100)
    declaration_phone = models.CharField(max_length=15)
    declaration_date = models.DateField(default=timezone.now)

    # ✅ Image Fields
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, validators=[validate_image])
    aadhar_image = models.ImageField(upload_to='documents/', blank=True, null=True, validators=[validate_image])
    supporting_document = models.ImageField(upload_to='documents/', blank=True, null=True, validators=[validate_image])

    def __str__(self):
        return f"{self.full_name} ({self.form_no})"

    @property
    def height(self):
        return f"{self.height_ft}'{self.height_in}\""

    def get_main_image_url(self):
        return self.profile_image.url if self.profile_image else "/static/images/default.jpg"

    def save(self, *args, **kwargs):
        # Generate form number if not set
        if not self.form_no:
            self.form_no = f"FORM-{uuid.uuid4().hex[:8].upper()}"

        self.full_clean()

        # Compress and save images
        if self.profile_image and not isinstance(self.profile_image.file, BytesIO):
            compressed = compress_image(self.profile_image)
            self.profile_image.save(compressed.name, compressed, save=False)

        if self.aadhar_image and not isinstance(self.aadhar_image.file, BytesIO):
            compressed = compress_image(self.aadhar_image)
            self.aadhar_image.save(compressed.name, compressed, save=False)

        if self.supporting_document and not isinstance(self.supporting_document.file, BytesIO):
            compressed = compress_image(self.supporting_document)
            self.supporting_document.save(compressed.name, compressed, save=False)

        super().save(*args, **kwargs)
