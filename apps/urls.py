from django.urls import path
from apps import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("user_login",views.user_login, name="user_login"),
    path("signup",views.signup, name="signup"),
    path("user_logout",views.user_logout, name="user_logout"),
    path("",views.index, name="index"),
    path("view/<slug>",views.view,name="view"),
    path("upload/",views.upload, name="upload"),
    path('success', views.success, name = 'success'), 
    path('trending',views.trend, name="trends"),
    path("postComment",views.postComment, name="postComment"),
    path('<str:username>',views.channel, name="channel"),
    path('accounts/editchannel',views.edit_channel, name="editchannel"),
    
    
]
urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)