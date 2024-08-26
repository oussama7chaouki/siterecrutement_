from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from shared.models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding the 'form-control' class to specific fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 2
        if commit:
            user.save()
        return user