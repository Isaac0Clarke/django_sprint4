from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserEditForm

User = get_user_model()
POSTS_PER_PAGE = 10


def get_paginator(request, queryset):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    posts = Post.objects.filter(
        is_published=True,
        pub_date__lt=timezone.now(),
        category__is_published=True,
        location__is_published=True
    ).annotate(
        comment_count=Count('comment', filter=Q(comment__is_published=True))
    ).order_by('-pub_date')

    return render(request, 'blog/index.html', {
        'page_obj': get_paginator(request, posts)
    })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    posts = category.post_set.filter(
        is_published=True,
        pub_date__lt=timezone.now()
    ).annotate(
        comment_count=Count('comment', filter=Q(comment__is_published=True))
    ).order_by('-pub_date')

    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': get_paginator(request, posts)
    })


def post_detail(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.filter(pk=post_id).first()
        if not post or post.author != request.user:
            post = get_object_or_404(
                Post,
                pk=post_id,
                is_published=True,
                pub_date__lt=timezone.now(),
                category__is_published=True,
                location__is_published=True
            )
    else:
        post = get_object_or_404(
            Post,
            pk=post_id,
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True,
            location__is_published=True
        )

    comments = post.comment_set.filter(
        is_published=True
    ).select_related('author').order_by('created_at')

    return render(request, 'blog/detail.html', {
        'post': post,
        'form': CommentForm(),
        'comments': comments
    })


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    post_filter = Q(author=profile_user)

    if request.user != profile_user:
        post_filter &= Q(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True,
            location__is_published=True
        )

    posts = Post.objects.filter(post_filter).annotate(
        comment_count=Count('comment', filter=Q(comment__is_published=True))
    ).order_by('-pub_date')

    return render(request, 'blog/profile.html', {
        'profile': profile_user,
        'page_obj': get_paginator(request, posts)
    })


@login_required
def create_post(request, post_id=None): 
    post = get_object_or_404(Post, pk=post_id) if post_id else None

    if post and post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if request.method == 'POST' and form.is_valid():
        post_instance = form.save(commit=False)
        post_instance.author = request.user
        post_instance.save()
        return redirect('blog:post_detail', post_id=post_instance.pk)

    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/create.html', {'post': post})


@login_required
def edit_profile(request):
    form = UserEditForm(request.POST or None, instance=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/user.html', {'form': form})


@login_required
def add_comment(request, post_id, comment_pk=None):
    post = get_object_or_404(Post, pk=post_id)

    comment = get_object_or_404(
        Comment, pk=comment_pk, post=post, author=request.user
    ) if comment_pk else None

    form = CommentForm(request.POST or None, instance=comment)

    if request.method == 'POST' and form.is_valid():
        comment_obj = form.save(commit=False)
        comment_obj.post = post
        comment_obj.author = request.user
        comment_obj.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, post_id, comment_pk):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_pk, post=post, author=request.user)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html', {
    'comment': comment,
    'form': CommentForm(instance=comment),
    'is_delete': True,
})