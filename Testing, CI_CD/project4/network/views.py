from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.shortcuts import get_object_or_404



def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    user = request.user
    who_you_liked = []
    if user.is_authenticated:
        user_likes = user.liked_posts.all()
        for post in user_likes:
            who_you_liked.append(post.id)

    if list(posts) != []:
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        return render(request, "network/index.html", {
            "posts":posts,
            "page_obj":page_obj,
            "who_you_liked":who_you_liked
        })
    
    else:
        return render(request, "network/index.html", {
            "message": "Currently no posts"
        })



    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

    
@login_required 
def create_post(request):
    if request.method == "POST":
        current_user = request.user
        content = request.POST["content"]
        post = Post(content = content, owner = current_user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
        

def user_profile(request, owner):
    current_user = request.user
    user_owner = User.objects.get(username = owner)
    current_username = current_user.username
    valid_follow = current_username != owner
    
    all_posts = user_owner.user_posts.all().order_by('-timestamp')
    if current_user.is_authenticated:
        current_user_follows = user_owner in current_user.following.all()
        if list(all_posts) != []:
            paginator = Paginator(all_posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "network/userprofile.html", {
            "valid_follow":valid_follow,
            "user":current_user,
            "owner": user_owner,
            "posts":all_posts,
            "current_user_follows":current_user_follows,
            "page_obj":page_obj
                })
        else:
            return render(request, "network/index.html", {
            "message": "Currently no posts"
        })
    else:
        return render(request, "network/userprofile.html", {
            "valid_follow":False,
            "user":current_user,
            "owner": user_owner,
            "posts":all_posts,
            "current_user_follows":False
                })
@login_required
def follow(request):
    user = request.user
    username = user.username
    
    user_following = user.following.all()
    owner = str(request.POST["owner"])
    user_owner = User.objects.get(username = owner)
    if request.method =="POST" and username != owner:
        if user_owner not in list(user_following):
            user.following.add(user_owner.id)
        else:
            user.following.remove(user_owner.id)
        return HttpResponseRedirect(reverse("userprofile", args=(owner,)))

@login_required
def following_page(request):
    user = request.user
    user_following = user.following.all()
    posts = Post.objects.filter(owner__in=user_following)
    if list(posts) != []:
        return render(request, "network/following.html", {
            "posts":posts
        })
    else:
        return render(request, "network/following.html", {
            "message": "Users you follow have no posts yet!"
        })
    

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data":data["content"]})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk = pk)
    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return JsonResponse({"message":"liked successfully"
        
    })





