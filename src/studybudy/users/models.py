import random, os
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from studybudy.settings import BASE_DIR

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_photo_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile-photos/{final_filename}".format(final_filename=final_filename)



# Create your models here.
class User(AbstractBaseUser):
    TYPE_CHOICES = [
        ('Admin IT', 'Admin IT'),
        ('Admin Editor', 'Admin Editor'),
        ('Student', 'Student'), 
        ('Teacher', 'Teacher'),
        
    ]

    user_id                     = models.CharField(max_length=50, unique=True, default="")
    first_name                  = models.CharField(max_length=300)
    last_name                   = models.CharField(max_length=300)
    dob                         = models.DateField(null=True)
    age                         = models.IntegerField(default=0)
    sex                         = models.CharField(max_length=10)
    country                     = models.CharField(max_length=50, blank=True)
    state                       = models.CharField(max_length=50, blank=True)
    los                         = models.CharField(max_length=50, blank=True)
    los_class                   = models.CharField(max_length=50, blank=True)
    school                      = models.CharField(max_length=200, blank=True)
    email                       = models.EmailField(max_length=255, unique=True)
    username                    = models.CharField(max_length=255, unique=True)
    telephone                   = models.CharField(max_length=50, default=0, blank=True)
    facebook                    = models.CharField(max_length=50, blank=True)
    twitter                     = models.CharField(max_length=50, blank=True)
    instagram                   = models.CharField(max_length=50, blank=True)
    user_type                   = models.CharField(max_length=50, choices=TYPE_CHOICES,)
    shared_with_me              = models.CharField(max_length=50, blank=True, null=True,)
    profile_photo               = models.ImageField(upload_to=upload_photo_path, null=True, blank=True)
    active                      = models.BooleanField(default=True)# can login
    admin                       = models.BooleanField(default=False)# staff user non superuser
    staff                       = models.BooleanField(default=False)# supersuser
    date_created                = models.DateTimeField(auto_now_add=True)
    last_editted                = models.DateTimeField(blank=True, null=True)
    last_login                  = models.DateTimeField(blank=True, null=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'dob','sex', 'user_type']


    #User Class Properties
    def __str__(self):
        return self.email


    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        short_name = full_name = '%s' % (self.first_name)
        return short_name.strip()

    def get_country_state(self):
        '''
        Returns the country and state for the user.
        '''
        country_state = '%s %s' % (self.country, self.state)
        return country_state.strip()


    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active



class UserState(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False, unique=True)
    mode                = models.CharField(max_length=100, default="light")
    folder_order        = models.CharField(max_length=100, default="ASC")
    file_order          = models.CharField(max_length=100, default="ASC")
    file_filters        = models.CharField(max_length=100, default="Name")
    folder_filters      = models.CharField(max_length=100, default="Name")
    view                = models.CharField(max_length=100, default="grid")
    total_storage       = models.BigIntegerField(default=0)

    def user_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.user.email


class Notifications(models.Model):
    usey                = models.ForeignKey(User, related_name="notifications_user", on_delete=models.CASCADE, blank=True, null=True,)
    task_id             = models.BigIntegerField(default=0)
    notify              = models.CharField(max_length=200,)
    seen                = models.BooleanField(default=False)

    def __str__(self):
        return self.usey.email