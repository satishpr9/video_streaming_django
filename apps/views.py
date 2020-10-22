from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from .models import Post,Comment,Channel
from .forms import VideoForm,ChannelForm
import subprocess
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    vd=Post.objects.all().order_by('-id')

    vdList= [vd[i:i+3] for i in range(0, len(vd), 3)]
    context={
        'vd':vd,
        'img':vdList,
    }

    return render(request,"index.html",context)


def trend(request):
    week_ago = datetime.date.today() - datetime.timedelta(days = 7)
    trends = Post.objects.filter(time_uplaod__gte = week_ago).order_by('-view')
    
    context={
        'trends':trends[:3],
    }
    return render(request,"trend.html",context)

def view(request, slug):
    post=Post.objects.filter(slug=slug)
    comment=Comment.objects.filter(post__in=post).order_by('-created')
    channel=Channel.objects.filter(id__in=comment)
    
    context={
        'post':post,
        'pop_post': Post.objects.order_by('-id')[:5],
        'comment':comment,
        'channel':channel,
        
    }
    
    return render(request,"view.html",context)





def channel(request, username):
    user=User.objects.filter(username=username)
   
    if user:
        user = user[0]
        channel = Channel.objects.get(user=user)
        name=Channel.objects.filter(user=user)
        post=getPost(user)
        subscribe = channel.subscribe
        user_img = channel.image
    
        
        # is_subscribe=Subscribe.objects.filter(user=request.user, followed=user)
        data = {
            'user_obj':user,
            'img':user_img,
            'subscribe':subscribe,
            
            'name':name,
            'posts':post,
            
        }
    else: 
        return HttpResponse('no such user')

    return render(request, 'channel.html', data)



def getPost(user):
    post_obj = Post.objects.filter(user=user)
    videoList= [post_obj[i:i+3] for i in range(0, len(post_obj), 3)]
    return videoList





def edit_channel(request):
    if request.method=="POST":
        channel_form=ChannelForm(data=request.POST or None, instance=request.user.channel, files=request.FILES)
        if channel_form.is_valid():
            channel_form.save()
            return redirect("/")
    else:
        channel_form=ChannelForm(instance=request.user)
    return render(request,'editchannel.html',{'channel_form':channel_form})            

@login_required
def upload(request):
    if request.method=="POST":
        user_=request.user
        form=VideoForm(request.POST, request.FILES, user_)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form=VideoForm()
    return render(request,"upload.html",{'form':form})    


def user_login(request):
    if request.method=='POST':
        user_name=request.POST.get('username','')
        pass_word=request.POST.get('password','')

        user=authenticate(username=user_name,password=pass_word)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Something Wrong Try Again")
            return redirect("/signup")
    return redirect("/signup")


def signup(request):
    if request.method=="POST":
        username=request.POST.get('username','')
        mail=request.POST.get('email','')
        password=request.POST.get('password','')
        conf_pass=request.POST.get('confpass','')
        
        userCheker=User.objects.filter(username=username)

        if userCheker:
            messages.error(request,"already have an account")
            return redirect("/")


        print(username)
        
        print(mail)
        print(password)
        print(conf_pass)

        if password==conf_pass:
            user_obj=User.objects.create_user(username=username,email=mail,password=password)
            user_obj.save()
            Channel.objects.create(user=user_obj,name=user_obj)
            messages.success(request,'SuccessFully Register')
            

    return render(request,'signup.html')


@login_required
def postComment(request):
    if request.method=='POST':
        comment=request.POST.get("comment")
        user=request.user
        postSno=request.POST.get("postSno")
        post=Post.objects.get(id=postSno)
        comment=Comment(comment=comment,user=user,post=post)
        comment.save()

    return render(request,'view.html')



def user_logout(request):
    logout(request)
    messages.success(request,"successfully logout")
    return redirect("/")




def success(request): 
    return HttpResponse('successfully uploaded') 