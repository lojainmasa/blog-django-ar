from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    # video 22
    title=models.CharField(max_length=100)
    content=models.TextField() #محتوى التدوينة
    Post_date=models.DateTimeField(default=timezone.now)# auto_now_add  يتم إنشاءه اول ما يتم عندما شاء التدوينة
    post_update=models.DateTimeField(auto_now=True) # auto_now يتم انشاءه عندما يتم تحديث التدوينة
    auther=models.ForeignKey(User, on_delete=models.CASCADE) #كاتب او ناشر التدوينة 

    def __str__(self):# video23 this fuction to show 'title' in blog ,control panel
        return self.title 
    
    class Meta:
        ordering=('-Post_date',) # vdeo 26 this is for ordering blogs from latest to first

#python manage.py makemigrations يحول الكود السابق إلى وسيط وليتم تحويل إلى جدول قواعد البيانات 
#python manage.py mirgrate يحول الكود الناتج عن الامر السابق إلى قواعد البيانات


#video 28
class Comment(models.Model):
    name=models.CharField(max_length=50,verbose_name='الأسم')
    email=models.EmailField(verbose_name='البريد الالكتروني')
    body= models.TextField(verbose_name='التعليق')
    comment_date=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=False)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')

    def __str__(self):
        return ' علق {} على {}.'.format(self.name,self.post)

    class Meta:
        ordering =('-comment_date',)



