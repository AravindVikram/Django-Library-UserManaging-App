from datetime import date, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
# from .forms import MedicineForm
from .models import Book , BookInstance
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        name= request.POST['username']                                  
        pw= request.POST['password1']
        pw2=request.POST['password2']
        e_mail=request.POST['email']

        if not name or not pw or not pw2 or not e_mail:
            messages.error(request, 'Error: All fields are required')
            return redirect('register')
        if (pw==pw2):
            if User.objects.filter(username=name).exists():
                messages.info(request,'Error: Username Already Exists')
                return render('register.html')                              
            else:
                user = User.objects.create_user(username=name,password=pw,email=e_mail)
                user.save()
                messages.info(request,'User Registration Successfull')
                return redirect('dashboard')     
        else:
            messages.info(request,'The passwords does not match')
            return redirect('register')                                        
    return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        name=request.POST['username']
        pw=request.POST['password']
        user= auth.authenticate(username=name,password=pw)

        if user is not None:
             auth.login(request,user)
             return redirect('dashboard')
        else:
            messages.info(request,'Error : invalid credentials') 
            return redirect('login')
    return render(request, "login.html")

@login_required
def logout(request):
    auth.logout(request)
    return render(request,'dashboard.html')

@login_required
def dashboard(request):
    user = User.objects.get(username=request.user.username)
    borrowed_books = BookInstance.objects.filter(borrower=user)
    if user.is_staff:
        users = User.objects.all()
    else:
        users = None
    context = {
        'user': user,
        'borrowed_books': borrowed_books,
        'users': users
    } 
    return render(request,'dashboard.html',context) 


@login_required
def books(request): 
    books=Book.objects.all()
    context={
        'books':books
    }
    return render(request,'books.html',context)

@login_required
def user(request,id):
    user = get_object_or_404(User,id=id)
    book_instances = user.bookinstance_set.all()  
    if request.method == 'POST':
        for book_instance in book_instances:
            if book_instance.is_due_date_expired:
                book_instance.due_date = date.today() + timedelta(days=7)
                book_instance.save()
                return redirect('user', id=id)
  
    context = {
        'user': user, 
        'book_instances': book_instances
    }
    return render(request,'user.html',context) 

