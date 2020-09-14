import re
from datetime import datetime
from users.models import User


class DataValidator:
    def __init__(self):
        self.cleaned_data  =  []

    def is_empty(self, arr):
        for d in arr:
            if d == "":
                return True
        return False

    def nameRegex(self, arr):
        for d in arr:
            z = re.match("/^[A-Za-z.\s_-]*$/", d)
            if z == False:
                return d
        return True

    # def socialRegex(self, arr):
    #     for d in arr:
    #         z = re.match("/^[A-Za-z.\s_-]*$/", d)
    #         if not z:
    #             return False
    #     return True

    def teleRegex(self, arr):
        for d in arr:
            z = re.match("/^[\s()+-]*([0-9][\s()+-]*){6,20}$/", d)
            if z == False:
                return False
        return True

    def email_unique(self, email):
        qs = User.objects.filter(email=email)
        if qs.exists():
            return False
        return True

    def telephone_unique(self, telys):
        qs = User.objects.filter(telephone=telys)
        if qs.exists():
            return False
        return True


    def date_format(self, arr):
        if (arr[1] == 2 and arr[0] > 29): 
                return false
        elif ((arr[1] == 4 or arr[1] == 6 or arr[1] == 9 or arr[1] == 11) and (arr[0] > 30)):
            return False
        else:
            datey = '%s-%s-%s' % (arr[2], arr[1], arr[0])
            date_object = datetime.strptime(datey, '%Y-%m-%d').date()
            return date_object

