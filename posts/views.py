from django.http import HttpResponse
from django.shortcuts import render
from .models import Posts
from .forms import PostForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db import IntegrityError


def health_check(request):
    return HttpResponse('ok')

# Create your views here.
def index(request):
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})

def post_list(request):
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request,'post_form.html', {'form':form})

@login_required
def post_edit(request, post_id):
  post = get_object_or_404(Posts, pk=post_id, user = request.user)
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.save()
      return redirect('post_list')
  else:
    form = PostForm(instance=post)
  return render(request, 'post_form.html', {'form': form})

@login_required
def post_delete(request, post_id):
  post = get_object_or_404(Posts, pk=post_id, user = request.user)
  if request.method == 'POST':
    post.delete()
    return redirect('post_list')
  return render(request, 'post_confirm_delete.html', {'post': post})
  

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password1'])
      try:
        user.save()
      except IntegrityError:
        form.add_error('email', 'An account with this email already exists.')
        return render(request, 'registration/register.html', {'form': form})
      login(request, user)
      return redirect('post_list')
  else:
    form = UserRegistrationForm()

  return render(request, 'registration/register.html', {'form': form})