from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'site_name': 'blogapp',
        'posts': posts
    }

    return render(request, 'home.html', context)


def about(request):
    context = {
        'title': 'About'
    }

    return render(request, 'about.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)

    context = {
        'post': post
    }

    return render(request, 'post_detail.html', context)


def post_list(request, username):
    posts = Post.objects.filter(author__username=username).order_by('-created_at')

    context = {
        'posts': posts,
        'username': username
    }

    return render(request, 'post_list.html', context)


 # <-- Optional: agar sirf logged-in users ko allow karna hai
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  # Include request.FILES to handle image uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect('blogapp:post_detail', pk=post.pk)
    else:
        form = BlogPostForm()

    context = {'form': form}
    return render(request, 'create_post.html', context)
@login_required

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        # Don't forget request.FILES here!
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blogapp:my_posts')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form})
@login_required
def my_posts(request):
    # Check karein ke user login hai ya nahi
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
    else:
        posts = [] # Agar login nahi hai toh khali list bhej dein, query chalaye hi na

    context = {
        'posts': posts
    }

    return render(request, 'my_posts.html', context)
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)  # Ensure only the author can delete
    
    if post.author != request.user:
        return redirect('blogapp:home')

    if request.method == 'POST':
        post.delete()
        return redirect('blogapp:my_posts')  # Delete hone ke baad My Posts ya Home par bhej dein

    context = {
        'post': post
    }
    return render(request, 'delete_confirm.html', context)
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful! Welcome to the platform.')
            return redirect('blogapp:home')
        else:
            # This triggers when form validation fails
            messages.error(request, 'Please correct the errors below to register.')
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'register.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in.')
            
            # Yeh check karega ke user ko pehle kahan jana tha
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('blogapp:home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('blogapp:home')