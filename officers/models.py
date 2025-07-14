from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class Officer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='আইডি')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='officer_profile',
        verbose_name=_('User')
    )

    class Education(models.TextChoices):
        BSC = 'BSC', _('B.Sc in Agriculture')
        MSC = 'MSC', _('M.Sc in Agriculture')
        PHD = 'PHD', _('PhD inploma in Agricu Agriculture')
        DIPLOMA = 'DIP', _('Dilture')
        OTHER = 'OTH', _('Other')

   
    class Specialization(models.TextChoices):
        CROP = 'CR', _('Crop Disease Management')
        IRRIGATION = 'IR', _('Irrigation Technology')
        ORGANIC = 'OR', _('Organic Farming')
        SEED = 'SD', _('Seed Technology')
        PESTICIDE = 'PE', _('Pesticide Management')
        CLIMATE = 'CL', _('Climate Adaptation')
        MACHINERY = 'MA', _('Agricultural Machinery')

    
    class AvailableDays(models.TextChoices):
        SAT_TO_WED = 'SW', _('Saturday-Wednesday')
        SUN_TO_THU = 'ST', _('Sunday-Thursday')
        MON_TO_FRI = 'MF', _('Monday-Friday')
        FLEXIBLE = 'FL', _('Flexible')

   
    nid_number = models.CharField(
        max_length=17,
        verbose_name=_('National ID Number'),
        blank=True,
        null=True
    )
    
    date_of_birth = models.DateField(
        verbose_name=_('Date of Birth'),
        blank=True,
        null=True
    )

   
    education = models.CharField(
        max_length=3,
        choices=Education.choices,
        verbose_name=_('Education Qualification'),
        blank=True,
        null=True
    )

    institution = models.CharField(
        max_length=100,
        verbose_name=_('Educational Institution'),
        blank=True,
        null=True
    )

    graduation_year = models.PositiveIntegerField(
        verbose_name=_('Graduation Year'),
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        blank=True,
        null=True
    )

    specialization = models.CharField(
        max_length=2,
        choices=Specialization.choices,
        default=Specialization.CROP,
        verbose_name=_('Specialization')
    )

    experience = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name=_('Experience (Years)'),
        blank=True,
        null=True
    )

    # Workplace Information
    workplace = models.CharField(
        max_length=100,
        verbose_name=_('Workplace'),
        help_text=_('District/Upazila Agriculture Office, Research Institute etc.')
    )

    designation = models.CharField(
        max_length=100,
        verbose_name=_('Designation'),
        blank=True,
        null=True
    )

    joining_date = models.DateField(
        verbose_name=_('Joining Date'),
        blank=True,
        null=True
    )

   
    days_available = models.CharField(
        max_length=2,
        choices=AvailableDays.choices,
        default=AvailableDays.SAT_TO_WED,
        verbose_name=_('Available Days')
    )

    time_available = models.CharField(
        max_length=100,
        default='9:00 AM - 4:00 PM',
        verbose_name=_('Available Time')
    )

  
    total_meetings = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Meetings Conducted')
    )

    average_rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_('Average Rating')
    )

   
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Bio')
    )

    profile_picture = models.ImageField(
        upload_to='officers/profile_pictures/',
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Verified Officer')
    )

    class Meta:
        verbose_name = _('Agriculture Officer')
        verbose_name_plural = _('Agriculture Officers')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation} ({self.workplace})"

    def get_education_info(self):
        return f"{self.get_education_display()} ({self.graduation_year}) from {self.institution}"

    def get_availability(self):
        return f"{self.get_days_available_display()}, {self.time_available}"

    def get_experience_level(self):
        if self.experience >= 10:
            return _('Senior')
        elif self.experience >= 5:
            return _('Mid-level')
        return _('Junior')