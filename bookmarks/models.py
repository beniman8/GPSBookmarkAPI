from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey,TextField,DateTimeField


    

class Bookmark(models.Model):
    user = ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE)
    lat = TextField(default='', max_length=100)
    lon = TextField(default='', max_length=100)
    alt = TextField(default='', max_length=100)
    timestamp = DateTimeField(auto_now_add=True)


    

    
    



