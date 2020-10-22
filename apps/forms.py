from django import forms
from .models import Post,User,Channel

class VideoForm(forms.ModelForm):
    class Meta:
        model= Post
        fields= ["user","title", "video","thumbnail","desc_field"]


class ChannelForm(forms.ModelForm):
    class Meta:
        model=Channel
        fields=["name","image"]