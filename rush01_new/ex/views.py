from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import User
from .models import Post
from .models import UserDescrip
from django.views.generic import DetailView, ListView, FormView, CreateView
from django.contrib.auth import authenticate, login, logout
from .log_in import LogForm
from .log_in import UpdateUser
from django.contrib import auth
from .models import CustomUserCreationForm
from django.core.exceptions import ValidationError

class PostDisplay(ListView):
    model = Post
    template_name = 'article.html'


class Details(FormView):
    #model = User
    model = UserDescrip
    template_name = 'details.html'
    form_class = UpdateUser
    def post(self, request, pk):
        who = request.user.id
        form = UpdateUser(self.request.POST, self.request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            picture = form.cleaned_data['picture']
            u = User.objects.get(id = pk)
            u.username = username
            u.first_name = first_name
            u.email = email
            u.save()
            t = UserDescrip.objects.filter(id=pk)
            if t:
                len = UserDescrip.objects.get(id=pk)
                len.description = description
                len.picture = picture
                len.user = User.objects.get(id=pk)
                len.save()
                return redirect("/user_profile")
            else:
                save = UserDescrip(
                description = description,
                picture = picture,
                user = User.objects.get(id=pk)
                )
                save.save()
                return redirect("/user_profile")
        else:
            print("PICTURE")
            return redirect("/user_profile")

def add_admin(request):
    id = request.user.id
    des = User.objects.get(id=id)
    des.is_staff = True
    des.save()
    return HttpResponse("User add as Admin")

def Staff(request):
    id = request.user.username
    user = User.objects.all()
    return render(request, "staff.html", {'f':user, "id":id})

def SuperUser(request, pk):
    id = request.user.username
    user = User.objects.all()
    t = User.objects.get(id=pk)
    if t.is_superuser == False:
        t.is_superuser = True
    else:
        t.is_superuser = False
    t.save()
    return render(request, "staff.html", {'f':user, "id":id})

def Admin(request, pk):
    id = request.user.username
    user = User.objects.all()
    t = User.objects.get(id=pk)
    if t.is_staff == False:
        t.is_staff = True
    else:
        t.is_staff = False
    t.save()
    return render(request, "staff.html", {'f':user, "id":id})

def user_profile(request, pk):
    id = request.user.id
    user = User.objects.get(id=id)
    des = UserDescrip.objects.filter(user_id=id)
    res =''
    img =''
    for i in des:
        res = i.description
        img = i.picture
    return render(request, "user_profile.html", {'user':user, "res":res, "img":img})

def home_view(request):
	return render(request, "home.html")

def is_login(request):
    id = request.user.id
    len = User.objects.all()
    for i in len:
        res = i.id
    user = User.objects.get(id=res)
    auth.login(request, user)
    return render(request, "home_login.html")

class Login(FormView):
    form_class = LogForm
    template_name = 'log_in.html'
    success_url ="/"
    def form_valid(self, form):
        form = LogForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(self.request, user)
                return redirect("/log")
        return redirect("/Login")

class Register(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration.html"
    success_url="/log"
    #def get(self, request):
    #    user = self.form_class.save(self)
    #    print(user)
    #    auth.login(self.request, user)
    

    #def get(self,request): 
     #   return redirect('/')

class Logout(DetailView):
    def get(self,request): 
        auth.logout(request)
        return redirect('/')

class Populate(ListView):
    def get(self, request):
        id = request.user.id
        a = User.objects.get(id=id)
        save = Post(
            title = 'The Phantom Menace',
            author =   a,
            synopsis =  'Rick McCallum',
            created = '1999-05-19'
        )
        save.save()
        save = Post(
            title = 'Attack of the Clones',
            author =  a,
            synopsis =  'Rick McCallum',
            created = '2002-05-16'
        )
        save.save()
        save = Post(
            title = 'Revenge of the Sith',
           author =  a,
            synopsis =  'Rick McCallum',
            created  = '2005-05-19'
        )
        save.save()
        return HttpResponse("OK POPULATE")