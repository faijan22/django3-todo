from django.contrib import admin
from .models import Todo

#create the class with any name and then pass this main thing admin.ModelAdmin
class TodoAdmin(admin.ModelAdmin):
    #and make this field visible in terms of read only to user's 
    readonly_fields = ('created',)  #passed the name of column we wantr to set the read only 


admin.site.register(Todo, TodoAdmin) #register the class as well 