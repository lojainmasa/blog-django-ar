from django.shortcuts import redirect, render
from .forms import UserCreationForm,LoginForm,UserUpdateForm,profileUpdateForm
from django.contrib import messages # for show message  to user after register information
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def register(request):
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            # form.save()  
            print('save a new user ')      
            # username=form.cleaned_data['username']
            messages.success(request,f'تهانيا {new_user} لقد تمت عمليىة التسجيل بنجاح')# show message
            return redirect('login')
    else:
        form=UserCreationForm()
    '''
    # context={
    #     'title':'التسجيل',
    #     'form':form,
    # }

    # template = loader.get_template('blog/register.html')
    # return HttpResponse(template.render(context, request))
'''
    return render(request,'user/register.html',{
        'title':'التسجيل',
        'form':form,
    })

def login_user(request):
    if request.method=='POST':
        #form= LoginForm()
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print('Done right entered')
            login(request,user)
            messages.success(request,f'تهانيا {username} لقد تمت عمليىة التسجيل الدخول بنجاح')
            return redirect('profile')
        else:
            print('error in username or password')
            messages.warning(request,'هناك خطأ في اسم المستخدم أو كلمة المرور')
            # return redirect('login')
            
    # else:
    #     form=LoginForm()        
    return render(request, 'user/login.html',{
        'title':'تسجيل الدخول',
        # 'form':form,
    })
def logout_user(request):
    logout(request)
    return render(request,'user/logout.html',{
        'title':'تسجيل الخروج',
        
    })
@login_required(login_url='login') # بدون الدكيكوريتر يمكن لاي شخص ان يصل لصفحة البروفايل 
def profile(request):
    posts = Post.objects.filter(auther=request.user)
    post_list = Post.objects.filter(auther=request.user)
    paginator=Paginator(post_list,2)
    page=request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_page)
    print('posts',posts)
    return render(request,'user/profile.html',{
        'title':'الملف الشخصي',
        'posts':posts,
        'page':page,
        'post_list':post_list,
    })
@login_required(login_url='login') 
def profile_update(request): #video 47
    if request.method=='POST':
        pass
        user_form=UserUpdateForm(request.POST, instance=request.user)
        profile_form=profileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request,'تم تحديث الملف الشخصي')
            return redirect('profile')
    else:
        pass
        user_form=UserUpdateForm(instance=request.user)
        profile_form=profileUpdateForm(instance=request.user.profile)
    
    context={
        'title':'تعديل الملف الشخصي',
        'user_form':user_form,
        'profile_form':profile_form,

    }
    
    return render(request,'user/profile_update.html',context)


