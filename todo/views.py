from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout ,authenticate
from .forms import Todoform
from .models import Todo 
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        #create a new user 
        # first check if both paswd matches then
        if request.POST['password1'] == request.POST['password2']:
            try:
                # to create the user , username and password are taken from the inspect>name=''
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # save the user
                user.save()
                # login the user so he can be at his own account 
                login(request, user)
                #then we must redirect them to some page so
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': "Username is already been taken."})                
        else:
            #if password didnt matched then show the home page again with the form
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': "Password did not match"})

#import the Todo class from the models
def currenttodos(request):
    #filter is used here bcaz we want only user who is logged in can see his own todos and not all which are created by everyone.
    #so we use user= only the req user can see it 
    #datecompleted column or entity is used here from models to check if its null or not so if its not means it is not yet completed and can be shown
    # in current todo's
        todos =Todo.obejcts.filter(user=request.user, datecompleted__isnull=True)
        return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
#pass the req but also pass the primary key you can have any naem to primary key but remeber what name you pass in url you have to pass here after req
def viewtodo(request,todo_pk):
    #import the get_object_or_404 then pass the class in which we are looking for , then the primary key for which the django will check in that class
    #user = bcaz only the req user can see his own we dont want anyone to play with url and see someones todo 
        todo = get_object_or_404(Todo ,pk=todo_pk, user=request.user)
        if request.method == "GET":
            #if ther request is get then create the instance of todo 
            #this instnce is going to get all the data of perticular id into the form
            form = Todoform(instance=todo)
            #then pass both the todo and form to the html page
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form': form})
        else:
            #and if someone then post the data i.e. edit the data and update 
            try:
                #while taking the information we need to take req.post which means the data but also the instance 
                #  which means the data will be added to existing object
                form = Todoform(request.POST,instance=todo)
                #save the updated form 
                form.save()
                #return to the success page.
                return redirect('currenttodos')
            except ValueError:
                return render(request, 'todo/viewtodo.html', {'todo':todo, 'form': form, 'error': 'bad information'})


def loginuser(request):
    #if the user want to get log in and the req is get then show the login page
    #import the AuthenticationForm from django.contrib.auth.forms
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        #to check the correct user name and password use authenticate 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # if user is not found in the database.
        if user is None:
            # send them back to login page with error
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error': "Username and Password did not matched."})                
        else:
            #if user mathes then 
            login(request, user) #login the user 
            return redirect('home') #redirect the user to success page 

@login_required            
def logoutuser(request):
    logout(request)
    return redirect('home')

def home(request):
    form = AuthenticationForm()
    return render(request, 'todo/home.html', {'form':form})

@login_required
def createtodo(request):
    if request.method == 'GET':
        #if the method is get then show the html page and siplay our model but wait how to pass our model on html page
        # we need to create our own form now i.e. forms.py [check there] once you done there then come here,
        #now import the forms i.e. TodoForm 
        #Now pass the Todo form in dictionary 
        return render(request, 'todo/createtodo.html', {'form':Todoform()})
    else:
        #if request is post and someone saves the form then 
        try:
            form = Todoform(request.POST)  #get all the data from the req.post in ToDOForm and then assign it to the form variable 
            newtodo = form.save(commit=False) #get the form in newtodo but dont save it to the database.
            newtodo.user = request.user #now newtodo.user is going to get the user who made the ToDo
            newtodo.save() #now save to the database.
            return redirect('currenttodos') #redirect to the succespage
        except (ValueError):
                    return render(request, 'todo/createtodo.html', {'form':Todoform(), 'error':'Bad data passed in. Try again.'})

@login_required
def comlpetetodo(request, todo_pk):
    todo = get_object_or_404(Todo ,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
    return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo ,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

def completedtodos(request):
        todos =Todo.obejcts.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        return render(request, 'todo/completedtodos.html', {'todos':todos})

