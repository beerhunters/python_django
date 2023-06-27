from django.forms import ModelForm
from myauth.models import Profile

class AvatarForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']