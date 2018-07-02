from E_library.models import Users, Author, belongs_to, Book, genre_allot, Event, event_genre
from  django import forms
from django.contrib.auth.models import User
from django.forms.fields import MultiValueField

class usersignupform(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ['Fname','Mname','Lname','Email_id','Phone_no','Password','Picture']


class authorsignupform(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Author
        fields = ['Fname','Mname','Lname','Email_id','Phone_no','Password','Picture']

        def __init__(self):
            self.cleaned_data = None

        def clean_phone_no(self):
            phone_no = self.cleaned_data.get('phone_no', None)
            if phone_no > 9999999999 or phone_no < 1000000000:
                raise forms.ValidationError('Please enter a valid phone number')
            return phone_no


class userloginform(forms.Form):
    email_id = forms.EmailField()
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email_id','password']

class authorloginform(forms.Form):
    email_id = forms.EmailField()
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email_id','password']

class addbookform(forms.ModelForm):
    Genre1 = forms.CharField(max_length=50,required=False)
    Genre2 = forms.CharField(max_length=50,required=False)
    Genre3 = forms.CharField(max_length=50,required=False)
    class Meta:
        model = Book
        fields = ['Isbn','Title','Copy','Cover','Genre1','Genre2','Genre3','Price']

class addeventform(forms.Form):
    Event_title = forms.CharField(max_length=100)
    DateOfEvent = forms.DateField()
    Location = forms.CharField(max_length=200)
    Picture = forms.ImageField()
    Genre1 = forms.CharField(max_length=50, required=False)
    Genre2 = forms.CharField(max_length=50, required=False)
    Genre3 = forms.CharField(max_length=50, required=False)
    class Meta:
        model = Event
        fields = ['Event_title','DateOfEvent','Location','Picture','Genre1','Genre2','Genre3']

class editbookform(forms.ModelForm):
    Genre1 = forms.CharField(max_length=50, required=False)
    Genre2 = forms.CharField(max_length=50, required=False)
    Genre3 = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Book
        fields = ['Title', 'Copy', 'Cover', 'Genre1', 'Genre2', 'Genre3']
