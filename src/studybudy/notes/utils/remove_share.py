from notes.models import FileSystem
from users.models import User





class RemoveShare():
    def __init__(self):
        self.folt   = ""

    def remove_shared_rigth (self, persons, file_id):
        for pp in persons:
            user    = User.objects.get(pk=int(pp))
            wk      = eval(user.shared_with_me)
            wk.remove(str(file_id))
            user.shared_with_me = wk
            user.save()
        return True
