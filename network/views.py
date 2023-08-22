from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from .models import User, Post

def getPaginated():
    posts = Post.objects.filter().order_by('-date')
    return Paginator(posts, 10)


def index(request):
    # Display all posts on the first page
    paginated = getPaginated()
    pageNumber = 1
    currentPage = paginated.page(pageNumber)
    hasNext = True if currentPage.has_next() else False
    hasPrev = True if currentPage.has_previous() else False

    return render(request, "network/index.html", {
        "currentPage": currentPage,
        "paginated": paginated,
        "hasNext": hasNext,
        "hasPrev": hasPrev,
        "pageNumber": pageNumber,
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

def send(request):
    if request.method == "POST":
        content = request.POST["text"]
        username = request.user

        post = Post(userPerson=username, content=content, likes=0)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    
def profile(request, userPerson):
    user_object = User.objects.get(username=userPerson)
    posts = Post.objects.filter(userPerson=user_object).order_by('-date')
    followerCount = len(user_object.followers.all())
    followingCount = len(user_object.following.all())

    actualUser = request.user
    isFollowing = True if (user_object in actualUser.following.all()) else False

    paginated = getPaginated()
    pageNumber = 1
    currentPage = paginated.page(pageNumber)
    hasNext = True if currentPage.has_next() else False
    hasPrev = True if currentPage.has_previous() else False 

    return render(request, "network/profile.html", {
        "current_user": user_object,
        "posts": posts,
        "followerCount": followerCount,
        "followingCount": followingCount,
        "isFollowing": isFollowing,
        "currentPage": currentPage,
        "paginated": paginated,
        "hasNext": hasNext,
        "hasPrev": hasPrev,
        "pageNumber": pageNumber,
    })

def follow(request, userFollowing):
    user = request.user
    followingUser = User.objects.get(username=userFollowing)
    user.following.add(followingUser)
    followingUser.followers.add(user)
    return profile(request, userFollowing)

def unfollow(request, userUnfollowing):
    user = request.user
    unfollowingUser = User.objects.get(username=userUnfollowing)
    user.following.remove(unfollowingUser)
    unfollowingUser.followers.remove(user)
    return profile(request, userUnfollowing)

def following(request, username):
    userObject = User.objects.get(username=username)
    usersFollowing = userObject.following.all()
    posts = Post.objects.all().order_by('-date')

    finalList = []
    for post in posts:
        if post.userPerson in usersFollowing:
            finalList.append(post)

    paginated = getPaginated()
    pageNumber = 1
    currentPage = paginated.page(pageNumber)
    hasNext = True if currentPage.has_next() else False
    hasPrev = True if currentPage.has_previous() else False
    
    return render(request, "network/following.html", {
        "posts": finalList,
        "currentPage": currentPage,
        "paginated": paginated,
        "hasNext": hasNext,
        "hasPrev": hasPrev,
        "pageNumber": pageNumber,
    })

def next(request, pageNumber):
    pageNumber += 1
    paginated = getPaginated()
    currentPage = paginated.page(pageNumber)
    hasNext = True if currentPage.has_next() else False
    hasPrev = True if currentPage.has_previous() else False

    return render(request, "network/index.html", {
        "currentPage": currentPage,
        "paginated": paginated,
        "hasNext": hasNext,
        "hasPrev": hasPrev,
        "pageNumber": pageNumber,
    })

def previous(request, pageNumber):
    pageNumber -= 1
    paginated = getPaginated()
    currentPage = paginated.page(pageNumber)
    hasNext = True if currentPage.has_next() else False
    hasPrev = True if currentPage.has_previous() else False

    return render(request, "network/index.html", {
        "currentPage": currentPage,
        "paginated": paginated,
        "hasNext": hasNext,
        "hasPrev": hasPrev,
        "pageNumber": pageNumber,
    })

def update(request, action, postId):
    post = Post.objects.get(id=postId)
    if action == "like":
        user = request.user
        if (user in post.usersLiked):
            return JsonResponse({'status': 'success', 'action': 'nothing', 'likes': post.likes})
        post.likes += 1
        post.usersLiked.add(user)
        post.save()
        return JsonResponse({'status': 'success', 'action': 'like', 'likes': post.likes})
    if action == "unlike":
        if (user not in post.usersLiked):
            return JsonResponse({'status': 'success', 'action': 'nothing'})
        post.likes -= 1
        post.usersLiked.remove(user)
        post.save()
        return JsonResponse({'status': 'success', 'action': 'unlike', 'likes': post.likes})
    return JsonResponse({'status': 'error'})
    
def tempUpdate(request, action, postId):
    post = Post.objects.get(id=postId)
    user = request.user
    if action == "like":
        if (user in post.usersLiked.all()):
            return JsonResponse({'status': 'success', 'action': 'nothing', 'likes': post.likes})
        post.usersLiked.add(user)
        post.likes += 1       
        post.save()
        return JsonResponse({'status': 'success', 'action': 'like', 'likes': post.likes})
    if action == "unlike":
        if (user not in post.usersLiked.all()):
            return JsonResponse({'status': 'success', 'action': 'nothing', 'likes': post.likes})
        post.usersLiked.remove(user)
        post.likes -= 1       
        post.save()
        return JsonResponse({'status': 'success', 'action': 'unlike', 'likes': post.likes})
    return JsonResponse({'status': 'failure'})
