from django.forms import ModelForm
from .models import Todo #import the model

class Todoform(ModelForm):
    #create a class with any name 
    class Meta:
        #now in this class which is by Default Meta 
        #we need to specify what model we are workin with and what fiels we want to display.
        model = Todo #so our model is ToDo that we passed here
        fields = ['title', 'memo', 'important'] #specify th fields in list that we want to display in the page 