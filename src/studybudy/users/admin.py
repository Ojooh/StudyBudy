from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import *


User = get_user_model()
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'user_id', 'first_name','email', 'user_type', 'staff', 'admin', 'active', 'date_created')
    list_filter = ('admin', 'staff', 'active', 'email', 'user_id')
    fieldsets = (
        (None, {'fields': ('email', 'user_id', 'username', 'password')}),
        ('personnal Details', {'fields': ( 'first_name', 'last_name', 'sex', 'dob', 'age', 'country', 'state', 'shared_with_me')}),
        ('academic deatails', {'fields': ('user_type', 'los', 'los_class', 'school')}),
        ('Social Profile', {'fields': ('telephone', 'facebook', 'twitter', 'instagram', 'profile_photo')}),
        ('Date info', {'fields': ('last_login', 'last_editted')}),
        ('Permissions', {'fields': ('staff','admin', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username', 'user_id')
    ordering = ('id','email', 'user_id')
    filter_horizontal = ()

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserState)
admin.site.register(Notifications)
admin.site.unregister(Group)

