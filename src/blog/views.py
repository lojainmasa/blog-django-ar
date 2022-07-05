from urllib import request
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Post, Comment
from .forms import NewComment,PostCreateForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import CreateView ,UpdateView,DeleteView  #this id for class views video 49
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
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
    posts=Post.objects.all()
    paginator=Paginator(posts,5)
    page=request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_page)
    context = {
        'title': 'الصفحة الرئيسية',
        'posts': posts , # video26 we will use 'posts' in latest_post.html
        'page':page,
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

#vedio 48

class PostCreateView(LoginRequiredMixin,CreateView):
    model= Post
    # fields=['title','content',]
    template_name ='blog/new_post.html'
    form_class=PostCreateForm
    def form_valid(self, form) -> HttpResponse:
        form.instance.auther=self.request.user
        return super().form_valid(form)

#vedio 49

class PostUpdateView(UserPassesTestMixin ,LoginRequiredMixin,UpdateView):
    model= Post
    template_name ='blog/post_update.html'
    form_class=PostCreateForm

    def form_valid(self, form) -> HttpResponse:
        form.instance.auther=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.auther:

            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model= Post
    success_url='/'

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.auther:
            # messages.success(request,'تم تحديث الملف الشخصي')
            return True

        return False
