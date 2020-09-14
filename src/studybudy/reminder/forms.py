import json, os
from django import forms
from .models import TaskReminder
from datetime import datetime


# from .models import User

class DateInput(forms.DateInput):
    input_type = "date"

class TimeInput(forms.TimeInput):
    input_type = "time"

class TaskForm(forms.Form):

    task = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "col": 4,
                "placeholder" : "Enter Task",
                "class" : "form-control", 
                "id" : "task",
            }
        )
    )

    date_scheduled = forms.DateField(
        widget=DateInput(
            format="%Y-%m-%d",
                attrs={
                "col" : 4,
                "class": "form-control",
                "id" : "date_scheduled",
                "placeholder" : "dd/mm/yyy"
            }
        )
    )

    time = forms.TimeField(
        widget=TimeInput(
            format="%H:%M:%S",
                attrs={
                "col" : 4,
                "class": "form-control",
                "id" : "time",
            }
        )
    )



    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        instance    = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     print("here")
        #     self.fields['date_scheduled'].required = False

        #     if instance is not None:
        #         self.fields["task"].initial             = instance.task
        #         self.fields["date_scheduled"].initial   = instance.time.strftime('%Y-%m-%d')

    def clean_date_scheduled(self):
        expiry_date = self.cleaned_data.get('date_scheduled')
        now         = datetime.today().strftime('%Y-%m-%d')
        format_exp  = datetime.strptime(str(expiry_date), "%Y-%m-%d").date()
        format_now  = datetime.strptime(str(now), "%Y-%m-%d").date()
        if format_now > format_exp:
             raise forms.ValidationError("Cannot set a past Date")
        else:
            return expiry_date

    def clean(self):
        data = self.cleaned_data
        print(data)
        return data