#from django.shortcuts import render

# # Create your views here.

# def home(request):
#     return render(request, 'blog/index.html',{'title': 'Home'})

from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Post, Comment
from .forms import NewComment
'''
posts=[
    {

    'title':'التدوينة الأولى',
    'content':'نص التدوينة الاولى كنص تجريبي',
    'post_date':'30-6-2022',
    'author':'abo al laith' 
    },
    {

    'title':'التدوينة الثانية  ',
    'content':'نص التدوينة الاولى كنص تجريبي',
    'post_date':'30-6-2022',
    'author':'abo al laith' 
    },
    {

    'title':'التدوينة الثالية',
    'content':'نص التدوينة الاولى كنص تجريبي',
    'post_date':'30-4-2022',
    'author':'abo al laith' 
    },
    {

    'title':'التدوينة الرابعة',
    'content':'نص التدوينة الاولى كنص تجريبي',
    'post_date':'30-5-2022',
    'author':'abo حسن' 
    }
]
'''


def home(request):
    context = {
        'title': 'الصفحة الرئيسية',
        'posts': Post.objects.all()  # video26 we will use 'posts' in latest_post.html
    }
    template = loader.get_template('blog/index.html')
    return HttpResponse(template.render(context, request))


def about(request):
    context = {
        'title': 'من أنا'
    }
    template = loader.get_template('blog/about.html')
    return HttpResponse(template.render({'title': 'من أنا'}, request))
# video 27


def post_detail(request, post_id):
    # video 28
    post = get_object_or_404(Post, pk=post_id)  # for get blog id
    print(post)
    comments = post.comments.filter(active=True)
    print(comments)
    comment_form = NewComment()  # video 30

    # new_comment=None# video 32

    if request.method == 'POST':
        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = NewComment()

    else:
        comment_form == NewComment()
    context = {
        'title': post,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    template = loader.get_template('blog/detail.html')
    return HttpResponse(template.render(context, request))
