from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Leads,Agent, Category

User = get_user_model()

class leadmodelforms(forms.ModelForm):
    class Meta: #meta specify the model
        model = Leads
        fields = ('firstname', 'lastname','age', 'assigned_agent','description','phone_number', 'email',)

class leadcategorymodelforms(forms.ModelForm):
    class Meta: #meta specify the model
        model = Leads
        fields = ('category',)



class Agentmodelforms(forms.ModelForm):
    class Meta: #meta specify the model
        model = User
        fields = ('email','username','first_name','last_name',)

class userprofileform(forms.ModelForm):
    class Meta: #meta specify the model
        model = User
        fields = ('email','username','first_name','last_name',)


class AssignAgentmodelforms(forms.Form):
    agent =  forms.ModelChoiceField(queryset= Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentmodelforms, self).__init__(*args,**kwargs)
        self.fields['agent'].queryset = agents

class Leadform(forms.Form):
    firstname = forms.CharField()
    lastname = forms.CharField()
    age = forms.IntegerField(min_value=0)




class CustomUserCreationform(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class Categorymodelform(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('Name',)
