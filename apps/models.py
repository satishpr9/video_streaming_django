from django.db import models

# Create your models here.

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
import subprocess
import time
from django.contrib.auth.models import User
# Create your models here.

class Channel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    image=models.ImageField(default="default.png")
    subscribe=models.IntegerField(default=0, blank=True)
    def __str__(self):
        return str(self.user)




class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=200,null=True)
    time_uplaod=models.DateTimeField(auto_now_add=True)
    video=models.FileField()
    thumbnail=models.ImageField()
    slug=models.CharField(max_length=120, blank=True)
    view=models.BooleanField(default=0)
    desc_field=models.TextField(default="Hello")

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("view", kwargs={"slug": self.slug}) 

    def save(self,*args, **kwargs):
        super().save(*args,**kwargs)
        # video_input_path = (self.video.path)
        # img_output_path = (self.thumbnail.path + time.strftime("%Y%m%d-%H%M%S"))
       
        # subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])

        # img=Image.open(self.thumbnail.path)
        # if img.height >500 or img.width >500:
        #     resize=(img.size)
        #     img.thumbnail(resize)
        #     img.save(self.thumbnail.path)

@receiver(pre_save, sender=Post)
def pre_save_slug(sender,  **kwargs):
    print(kwargs)
    slug=slugify(kwargs['instance'].title)
    kwargs['instance'].slug=slug        


class Comment(models.Model):

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user= models.ForeignKey(User,on_delete=models.CASCADE) 
    comment = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return self.comment



    
