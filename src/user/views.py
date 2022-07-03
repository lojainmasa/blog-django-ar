from django.shortcuts import redirect, render
from .forms import UserCreationForm,LoginForm
from django.contrib import messages # for show message  to user after register information
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout


def register(request):
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()        
            username=form.cleaned_data['username']
            messages.success(request,f'تهانيا {username} لقد تمت عمليىة التسجيل بنجاح')# show message
            return redirect('home')
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
            return redirect('home')
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
def profile(request):
    return render(request,'user/profile.html',{
        'title':'الملف الشخصي',
    })