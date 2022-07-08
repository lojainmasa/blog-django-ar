#video 34 
from cProfile import label
from curses import use_default_colors
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserCreationForm(forms.ModelForm):
    username=forms.CharField(label='اسم المستخدم',max_length=30,help_text='اسم المستخدم يجب الا يحتوي على مسافات')
    email=forms.EmailField(label='البريد الإلكتروني')
    first_name=forms.CharField(label='الأسم الأول')
    last_name=forms.CharField(label='الأسم الأخير')
    password1=forms.CharField(label='كلمة المرور',widget=forms.PasswordInput(),min_length=8,help_text='كلمة المرور يجب ان لا تقل عن 8')
    password2=forms.CharField(label='تأكيد كلمة المرور',widget=forms.PasswordInput(),min_length=8)

    class Meta:
        model=User
        fields=('username','email','first_name',
                'last_name','password1','password2'
        )
        
    def clean_password2(self): #video35 thid function to verify that passwords match
        cd=self.cleaned_data
        if cd['password1']!=cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cd['password2']# الخطا السابق سيظهر تحت حقل password2

    def clean_username(self):
        cd=self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد مستخدم مسجل بهذا الأسم')
        return cd['username']# الخطا السابق سيظهر تحت حقل username


class LoginForm(forms.ModelForm):#video 38
    username=forms.CharField(label='اسم المستخدم')
    password=forms.CharField(label='كلمة المرور',widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','password')

class UserUpdateForm(forms.ModelForm):
    
    first_name=forms.CharField(label='الأسم الأول')
    last_name=forms.CharField(label='الأسم الأخير')
    email=forms.EmailField(label='البريد الإلكتروني')

    class Meta:
        model=User
        fields=('first_name', 'last_name','email')

class profileUpdateForm(forms.ModelForm):

    class Meta:
        model= Profile
        fields=('image',)
