from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Todo(models.Model):
    obejcts = models.Manager()
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) #this is for the admin site and it will not be shown to admin and user even so to see that as admin goto admin.py
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    #to know who made the todo which user made the todo and to assign him that todo we
    #   need to create this field and also import User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



