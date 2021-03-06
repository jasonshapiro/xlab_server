from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class InviteForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='E-mail')
    group = forms.ChoiceField(label='Group',
                choices=[(g.id, g.name) for g in Group.objects.all().order_by('name')])

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(InviteForm, self).__init__(*args, **kwargs)

        if user.is_staff:
            pass

class UserCreationFormWithEmail(UserCreationForm):
    def __init__(self, *args, **kwargs):
        try:
            email = kwargs.pop('email')
        except KeyError:
            email = None
        super(UserCreationFormWithEmail, self).__init__(*args, **kwargs)
        #self.fields['first_name'].required = True
        #self.fields['last_name'].required = True
        self.fields['username'].validators = [self.validate_username]
        self.fields['email'].initial = "" if email is None else email

        self.fields['phone_model'] = forms.ChoiceField(label='Your phone is',
            choices=( ('android', 'Android'), ('iphone', 'iPhone') ),
            help_text="Please choose Android. Our iPhone application will be available soon." )
    class Meta:
        model = User
        #fields = ('username', 'email', 'first_name', 'last_name')
        fields = ('username', 'email')


    def validate_username(self, value):
        if value in ('anonymous', 'training') or value.startswith('phone'):
            raise ValidationError(u'%s is not a valid username. Please choose a different one.' % value)


    def clean_username(self):
        username = self.cleaned_data['username'] \
            if self.cleaned_data['username'] is None else self.cleaned_data['username'].lower()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'%s already exists' % self.cleaned_data['username'] )