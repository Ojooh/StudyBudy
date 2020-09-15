import random, os
from django.db import models
from users.models import User

# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "Notes/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class FileSystem(models.Model):
    name            = models.CharField(max_length=200)
    folder          = models.BigIntegerField(default=0)
    file_type       = models.CharField(max_length=50, blank=True, null=True,)
    size            = models.BigIntegerField(default=0)
    owner           = models.ForeignKey(User, related_name="Owner", on_delete=models.CASCADE, blank=True, null=True,)
    location        = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    starred         = models.BooleanField(default=False)
    public          = models.BooleanField(default=False)
    sharable        = models.BooleanField(default=False)
    shared_with     = models.CharField(max_length=50, blank=True, null=True,)
    words           = models.CharField(max_length=500, blank=True, null=True,)
    time_taken      = models.BigIntegerField(default=0)
    description     = models.TextField(blank=True, null=True,)
    quized          = models.BooleanField(default=False)
    quized_saved    = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    last_editted_by = models.ForeignKey(User, related_name="editted_by", on_delete=models.CASCADE, blank=True, null=True,)
    last_editted    = models.DateTimeField(blank=True, null=True)
    last_opened     = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


    def get_owner_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.owner.first_name, self.owner.last_name)
        return full_name

    def get_owner_short_name(self):
        '''
        Returns the short name for the user.
        '''
        short_name = full_name = '%s' % (self.owner.first_name)
        return short_name.strip()

