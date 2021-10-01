from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from App_Blood.forms import CommentForm
from App_Blood.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    return render(request, 'App_Blood/index.html')


def About(request):
    return render(request, 'App_Blood/about-us.html')


def Contact(request):
    return render(request, 'App_Blood/contact.html')


def Gallery(request):
    return render(request, 'App_Blood/gallery-2.html')


def Doner(request):
    return render(request, 'App_Blood/donor.html')


def Blog(request):
    all_blog = Blogpost.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_blog, 6)
    try:
        all_blog = paginator.page(page)
    except PageNotAnInteger:
        all_blog = paginator.page(1)
    except EmptyPage:
        all_blog = paginator.page(paginator.num_pages)
    context = {
        'all_blog': all_blog,
    }
    return render(request, 'App_Blood/blog.html', context)


@login_required(login_url="App_Accounts:login")
def Blogdetails(request, id):
    try:
        blog_post = Blogpost.objects.get(id=id)
        recent_blog = Blogpost.objects.exclude(id=blog_post.id).order_by('-post_on')[:8]
        comments = Comment.objects.filter(post=blog_post, reply=None).order_by('-id')
        if request.method == "POST":
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(
                    post=blog_post, user=request.user, content=content,reply=comment_qs
                )
                comment.save()
        else:
            comment_form = CommentForm()
        is_liked = False
        if blog_post.like.filter(id=request.user.id).exists():
            is_liked = True
        context = {
            'blog_post': blog_post,
            'recent_blog': recent_blog,
            'comment_form': comment_form,
            'comments':comments,
            'is_liked':is_liked,
        }
    except:
        return redirect('App_Blood:blog')
    if request.is_ajax():
        html = render_to_string('App_Blood/comment_section.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'App_Blood/blog_details.html', context)

def blog_like(request):
    blog_post = get_object_or_404(Blogpost, id=request.POST.get('blog_id'))
    is_liked = False
    if blog_post.like.filter(id=request.user.id).exists():
        blog_post.like.remove(request.user)
        is_liked = False
    else:
        blog_post.like.add(request.user)
        is_liked = True

    context = {
        'blog_post': blog_post,
        'is_liked': is_liked,
    }
    if request.is_ajax():
        html = render_to_string('App_Blood/reaction_section.html', context, request=request)
        return JsonResponse({'form': html})

def Privacy(request):
    return render(request, 'App_Blood/privacy.html')
