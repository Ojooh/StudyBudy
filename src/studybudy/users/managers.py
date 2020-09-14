import time, os
from django.db import models
from django.conf import settings
from datetime import date
from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


    def generate_username(self, email):
        marray = email.split("@")
        return "@" + marray[0]

    def generate_userID(self, user_type, user_id):
        year = time.strftime("%y", time.localtime())
        num = str(user_id).zfill(4)

        if user_type == "Student":
            ID = "STD" + "-" + year + num
        elif user_type == "Admin IT" or user_type == "Admin Editor":
            ID = "ADM" + "-" + year + num
        return ID

    def create_user(self, email, first_name, last_name, sex, dob, user_type, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('User must have a password')
        email = self.normalize_email(email)
        user_obj = self.model(email=email, **extra_fields)
        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.sex = sex
        user_obj.dob = dob
        user_obj.user_type  = user_type
        user_obj.save(using=self._db)
        if dob != "" and dob is not None:
            user_obj.age            = self.calculate_age(user_obj.dob)

        user_obj.username       = self.generate_username(user_obj.email)
        user_obj.user_id    = self.generate_userID(user_obj.user_type, user_obj.id)  
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self, email, first_name, last_name, sex, dob, user_type, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user_obj = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            dob=dob,
            user_type= user_type,
            password=password,
        )
        user_obj.staff          = True
        if dob != "" and dob is not None:
            user_obj.age            = self.calculate_age(user_obj.dob)
        user_obj.username       = self.generate_username(user_obj.email)
        user_obj.user_id       = self.generate_userID(user_obj.user_type, user_obj.id)
        user_obj.save(using=self._db)
    
        return user_obj

    def create_superuser(self, email, first_name, last_name, sex, dob, user_type, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user_obj = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            dob=dob,
            user_type= user_type,
            password=password,
        )
        user_obj.staff          = True
        user_obj.admin          = True
        if dob != "" and dob is not None:
            user_obj.age            = self.calculate_age(user_obj.dob)
        user_obj.username       = self.generate_username(user_obj.email)
        user_obj.user_id       = self.generate_userID(user_obj.user_type, user_obj.id)
        user_obj.save(using=self._db)


        user_obj.save(using=self._db)
        return user_obj
