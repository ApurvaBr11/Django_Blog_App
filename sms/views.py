from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.urls import reverse


# Create your views here.

def home(r):
    data = Notes.objects.all().order_by('-id')
    categories = Categories.objects.all().order_by('-id')
    recent_users = User.objects.order_by('-date_joined')[:6]
    context = {'notes':data , 'categories':categories , 'recent_users':recent_users}
    return render(r, 'home.html',context )

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None )
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()
            return redirect('home')  
    else:
        form = PostForm()
    return render(request, 'create_notes.html', {'form': form})

def register(r):
    form = UserCreationForm(r.POST or None)
    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(login_view)
    return render(r, 'accounts/register.html', {'form': form})

def login_view(r):
    if r.method == 'POST':
        form = AuthenticationForm(r, data=r.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(r, username=username, password=password)
            if user is not None:
                login(r, user)
                return redirect('home')
        else:
            error_message = 'Invalid username or password'
    else:
        form = AuthenticationForm()

    return render(r, 'accounts/login.html', {'form': form })

def logout_view(request):
    logout(request)
    return redirect('home')

def view(r,id):
    note = Notes.objects.get(id = id)
    related = Notes.objects.filter(categories = note.categories)
    likes = Like.objects.filter(post = id).count
    commentlists = Comment.objects.filter(post = id).order_by('-id')
    if r.method == 'POST':
        form = CommentForm(r.POST or None )
        if form.is_valid():
            post = form.save(commit=False)
            post.user = r.user
            post.post = note
            post.save()
            context = {'note':note , 'related':related , 'form':form , 'commentlists':commentlists ,'like':likes}
            return render(r , 'view.html' ,context)
    else:
        form = CommentForm()
    context = {'note':note , 'related':related , 'form':form , 'commentlists':commentlists,'likes':likes }
    return render(r , 'view.html' ,context)

def delete(r,id):
    note = Notes.objects.get(id = id)
    if r.user.id == note.user.id:
            note.delete()
            return redirect(home)
    else:
        return redirect(home)

def viewmyposts(r):
    notes = Notes.objects.filter(user = r.user.id)
    context = {'notes':notes}
    return render(r,'viewmyposts.html',context)

def viewUser(r,id):
    if id == r.user.id:
       notes = Notes.objects.filter(user = r.user.id)
       context = {'notes':notes}
       return render(r,'viewmyposts.html',context)
    else:
        user = User.objects.get(id = id)
        notes = Notes.objects.filter(user = id)
        context = {'user':user,'notes':notes}
    return render(r,'viewUser.html',context)

def viewcategorie(r,id):
    if id == 18:
        data = Notes.objects.all()
        categories = Categories.objects.all().order_by('-id')
        context = {'notes':data , 'categories':categories}
        return render(r, 'home.html',context )
    else:
       data = Notes.objects.filter(categories = id)
       categories = Categories.objects.all().order_by('-id')
       count = Notes.objects.filter(categories = id).count
       context = {'notes':data , 'categories':categories , 'count':count}
       return render(r, 'home.html',context )
    
def searchNews(r):
    search = r.GET.get('search')
    data = {
        "notes":Notes.objects.filter(content__icontains=search),
        "categories":Categories.objects.all()
    }
    return render(r, "home.html",data) 

def deletecomment(r,id):
    Commentdata = Comment.objects.get(id=id)
    Commentdata.delete()
    idd = Commentdata.post.id
    
    function1_url = reverse('view', args=[idd])
    return redirect(function1_url)
    
@login_required
def like_student(r, student_id):
    student = get_object_or_404(Notes, id=student_id)
    like, created = Like.objects.get_or_create(user=r.user, post=student)
    if not created:
        like.delete()
    function1_url = reverse('view', args=[student_id])
    return redirect(function1_url)

def edit(r,id):
    post = Notes.objects.get(id=id)
    form = PostForm(r.POST or None, r.FILES or None, instance=post)
    data = {
        "form":form,
    }

    if r.method == "POST":
        formData = form.save(commit=False)
        formData.author = r.user
        formData.save()
        return redirect(home)
    
    return render(r, "create_notes.html",data)

def toggle_follow(request, user_id):
    # Get the user to be followed/unfollowed
    followed_user = User.objects.get(id=user_id)

    # Check if a follow relationship already exists
    follow_exists = Follow.objects.filter(followed_by=request.user, followed_to=followed_user).exists()

    if follow_exists:
        # If already following, unfollow the user
        Follow.objects.filter(followed_by=request.user, followed_to=followed_user).delete()
        message = f"You have unfollowed {followed_user.username}."
    else:
        # If not following, create a follow relationship
        follow = Follow.objects.create(followed_by=request.user, followed_to=followed_user)
        message = f"You are now following {followed_user.username}."

    # Perform any additional actions or validations if needed

    # Optionally, redirect or return a response with the appropriate message
    return redirect(home)