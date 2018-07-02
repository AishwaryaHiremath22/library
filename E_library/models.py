from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
# Create your models here.

"""class UserProfile(models.Model):
    user = models.OneToOneField(User)"""

class Users(models.Model):
    #user_type = models.ForeignKey(User,default=1)
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')
    digit = RegexValidator(r'^[0-9]*$','Enter valid phone number.')
    Fname = models.CharField(max_length=50, validators=[alphanumeric])
    Mname = models.CharField(max_length=50,blank=True,validators=[alphanumeric])
    Lname = models.CharField(max_length=50, validators=[alphanumeric])
    #user_type = models.OneToOneField(User,max_length=4,blank=True,null=True)
    Password = models.CharField(max_length=15)
    Email_id = models.EmailField(unique=True)
    Phone_no = models.CharField(max_length=10,validators=[digit])
    Picture = models.FileField(blank=True)


    #ser = models.ForeignKey(User)
    def __str__(self):
        return self.Fname+' '+self.Lname

class Author(models.Model):
    #Author_id = models.CharField(max_length=10,primary_key=True)
    #user_type = models.IntegerField(default=2)
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')
    digit = RegexValidator(r'^[0-9]*$', 'Enter valid phone number.')
    Fname = models.CharField(max_length=50,validators=[alphanumeric])
    Mname = models.CharField(max_length=50,blank=True,validators=[alphanumeric])
    Lname = models.CharField(max_length=50,validators=[alphanumeric])
    #user_type = models.OneToOneField(User,max_length=4,blank=True,null=True)
    Password = models.CharField(max_length=15)
    Email_id = models.EmailField(unique=True)
    Phone_no = models.CharField(max_length=10,validators=[digit])
    Picture = models.FileField(blank=True)
    def __str__(self):
        return self.Fname+' '+self.Lname

class Book(models.Model):
    ival = RegexValidator(r'^[0-9-]*$', 'Enter valid ISBN number.')
    Isbn = models.CharField(max_length=13,primary_key=True,validators=[ival])
    Title = models.CharField(max_length=50,unique=True)
    Price = models.FloatField()
    Copy = models.FileField()
    Cover = models.ImageField()
    def __str__(self):
        return self.Title


class genre_allot(models.Model):
    class Meta:
        unique_together = 'Isbn','genre'

    ival = RegexValidator(r'^[0-9-]*$', 'Enter valid ISBN number.')
    Isbn = models.ForeignKey(Book,on_delete=models.CASCADE,validators=[ival])
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')
    genre = models.CharField(max_length=50,validators=[alphanumeric])
    def __str__(self):
        return self.genre

class Group(models.Model):
    #Group_id = models.IntegerField(primary_key=True)
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')
    Genre = models.CharField(max_length=50,unique=True,validators=[alphanumeric])

    def __str__(self):
        return self.Genre

class Event(models.Model):
    A_id = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    DateE = models.DateField()
    E_title = models.CharField(max_length=50,unique=True)
    Picture = models.FileField(blank=True)
    Location = models.CharField(max_length=500)
    def __str__(self):
        return self.E_title

class borrows(models.Model):
    class Meta:
        unique_together = 'user_id','Isbn'

    ival = RegexValidator(r'^[0-9-]*$', 'Enter valid ISBN number.')
    rate = RegexValidator(r'^[0-10]$','Enter ratings 0-10.')
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    Isbn = models.ForeignKey(Book,on_delete=models.CASCADE,validators=[ival])
    ratings = models.FloatField(validators=[rate],null=True,blank=True)


class written_by(models.Model):
    class Meta:
        unique_together = 'A_id', 'Isbn'

    ival = RegexValidator(r'^[0-9-]*$', 'Enter valid ISBN number.')
    A_id = models.ForeignKey(Author,on_delete=models.CASCADE)
    Isbn = models.ForeignKey(Book,on_delete=models.CASCADE,validators=[ival])

class belongs_to(models.Model):
    class Meta:
        unique_together = 'G_id','user_id'
    G_id = models.ForeignKey(Group,on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)


class event_genre(models.Model):
    class Meta:
        unique_together = 'Title','Genre'
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')
    Title = models.ForeignKey(Event,on_delete=models.CASCADE)
    Genre = models.CharField(max_length=50,validators=[alphanumeric])
