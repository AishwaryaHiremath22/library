from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.db.models import Q, Max, Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.core.urlresolvers import reverse
from E_library.forms import usersignupform, authorsignupform, userloginform, addbookform, authorloginform, \
    addeventform, editbookform
from E_library.models import Users, Book, Author, Group, belongs_to, borrows, Event, event_genre, written_by, \
    genre_allot
import datetime

def index(request):
    return render(request,'E_library/mainpage.html')

def usersignup(request):
    form = usersignupform(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('Email_id')
        password = form.cleaned_data.get('Password')
        user = User.objects.create_user(username=username, password=password)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'E_library/login.html', {'form': userloginform})
    return render(request,'E_library/userreg.html',{'form':form})

def authorsignup(request):
    form = authorsignupform(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('Email_id')
        password = form.cleaned_data.get('Password')
        user = User.objects.create_user(username=username, password=password)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'E_library/authorlogin.html', {'form': authorloginform})
    return render(request, 'E_library/authorreg.html', {'form': form})

def userlogin(request):
    form = userloginform(request.POST or None)
    if request.method == "POST":
        username = request.POST.get('email_id')
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user = Users.objects.get(Email_id=request.POST.get('email_id'))
                return HttpResponseRedirect(reverse('E_library:homepage', args=(user.id,)))
            else:
                return render(request, 'E_library/login.html', {'error_message': 'Inavlid username or password'})
        else:
            return render(request, 'E_library/login.html', {'error_message': 'Invalid login'})
    return render(request, 'E_library/login.html',{'form':form})

def logout_user(request):
    logout(request)
    form = userloginform(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'E_library/login.html', context)


def authorlogin(request):
    form = userloginform(request.POST or None)
    if request.method == "POST":
        username = request.POST.get('email_id')
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                user = Author.objects.get(Email_id=request.POST.get('email_id'))
                return HttpResponseRedirect(reverse('E_library:authorhomepage', args=(user.id,)))
            else:
                return render(request, 'E_library/login.html', {'error_message': 'Inavlid username or password'})
        else:
            return render(request, 'E_library/login.html', {'error_message': 'Invalid login'})
    return render(request, 'E_library/authorlogin.html', {'form': form})


def logout_author(request):
    logout(request)
    form = authorloginform(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'E_library/authorlogin.html', context)

@login_required(login_url="/E_library/userlogin/")
def mylibrary(request,uid):
    if request.user.is_authenticated:
        all_books = borrows.objects.filter(user_id=uid)
        if all_books is None:
            err = 'You can borrow books and enjoy reading'
        all_book = Book.objects.all()
        return render(request,'E_library/mylibrary.html',{'all_books':all_books, 'uid':uid,'all_book':all_book,})
    else:
        return render(request, 'E_library/login.html', {'form': userloginform})

def homepage(request, uid):
    if request.user.is_authenticated:
        all_book = Book.objects.all()
        my_book = borrows.objects.filter(user_id=uid)
        b = []
        for i in all_book:
            found = False
            for j in my_book:
                if i.Isbn == j.Isbn_id:
                    found = True
                    break
            if not found:
                b.append(i)

        auth = written_by.objects.all()
        genre = genre_allot.objects.order_by('genre').values('genre').distinct()
        return render(request, 'E_library/homepage.html',
                          {'uid': uid, 'all_book': all_book,'auth':auth,'genre':genre,'my_book':my_book,'b':b})
    else:
        return render(request, 'E_library/login.html', {'form': userloginform})

def genre(request,uid,gen):

    m = borrows.objects.values('Isbn_id')
    a = genre_allot.objects.filter(genre=gen)
    a = a.exclude(Isbn__in=m)
    b = Book.objects.exclude(Isbn__in=m)
    return render(request,'E_library/genre.html',{'a':a,'b':b})

def books(request,uid):
    all_books = Book.objects.all()
    author = Author.objects.all()
    query = request.GET.get("q")
    if query:
        all_books = all_books.filter(
            Q(Title__icontains=query)
        ).distinct()
        authors = author.filter(
            Q(Fname__icontains=query) | Q(Lname__icontains=query)
        ).distinct()
        return render(request, 'E_library/book.html', {'all_books': all_books,'authors':authors, 'uid': uid})
    else:
        return HttpResponseRedirect(reverse('E_library:homepage', args=(uid,)))

def detail(request, uid,isbn):
    b = get_object_or_404(Book, pk=isbn)
    w = borrows.objects.filter(Isbn=isbn).aggregate(Avg('ratings'))
    d = w['ratings__avg']
    return render_to_response('e_library/details.html', {'book_detail': b, 'uid': uid, 'isbn': isbn,'w':d})

def download(request,uid,isbn):
    u = Users.objects.get(pk=uid)
    b = Book.objects.get(Isbn=isbn)
    br = borrows(user_id=u, Isbn=b)
    br.save()
    return HttpResponseRedirect(reverse('E_library:details', args=(uid, isbn)))
    #return render(request, 'E_library/borrow.html', {'uid': uid, 'isbn': isbn})

def joingroup(request, uid):
    all_groups = Group.objects.all()
    return render(request, 'E_library/group.html', {'all_groups': all_groups, 'uid': uid})

def join(request,uid,gid):
    genre = Group.objects.get(pk=gid)
    u = Users.objects.get(pk=uid)
    p = belongs_to(G_id=genre, user_id=u)
    try:
        p.save()
    except IntegrityError:
        return HttpResponse("<h2>You have already joined group</h2>")
    return render(request, 'E_library/joinmsg.html', {'genre': genre, 'uid': uid})

def joinevent(request,uid):
    e = Event.objects.filter(DateE__lt=datetime.datetime.now())
    e.delete()
    all_eve = Event.objects.filter(DateE__gte=datetime.datetime.now())
    #all_gen = event_genre.objects.all()
    return render(request,'E_library/joinevent.html',{'all_events':all_eve,'uid':uid})

def authorhomepage(request,aid):
    return render(request,'E_library/authhomepage.html',{'aid':aid})

def addbook(request,aid):
    form = addbookform(request.POST or None,request.FILES or None)
    Aid = Author.objects.get(pk=aid)
    err = ''
    if form.is_valid():
        form.save(request.POST)
        isbn = request.POST.get('Isbn')
        isbn = Book.objects.get(Isbn=isbn)
        p = written_by(A_id=Aid, Isbn=isbn)
        p.save()
        genre1 = request.POST.get('Genre1')
        if not genre1:
            genre1 = None
        genre2 = request.POST.get('Genre2')
        if not genre2:
            genre2 = None
        genre3 = request.POST.get('Genre3')
        if not genre3:
            genre3 = None
        if genre1 is not None:
            g = Group(Genre=genre1)
            try:
                g.save()
            except IntegrityError:
                err=''
            obj = genre_allot(Isbn=isbn, genre=genre1)
            try:
                obj.save()
            except IntegrityError:
                err = "This Genre is already alloted to this book"
        if genre2 is not None:
            g = Group(Genre=genre2)
            try:
                g.save()
            except IntegrityError:
                err =''
            obj1 = genre_allot(Isbn=isbn, genre=genre2)
            try:
                obj1.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
        if genre3 is not None:
            g = Group(Genre=genre3)
            try:
                g.save()
            except IntegrityError:
                err =''
            obj2 = genre_allot(Isbn=isbn, genre=genre3)
            try:
                obj2.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
            #addgroup()
        return HttpResponseRedirect(reverse('E_library:authorhomepage', args=(aid,)))

    return render(request, 'E_library/addbook.html', {'form': form, 'aid': aid,'err':err})

def addevent(request,aid):
    form = addeventform(request.POST or None,request.FILES or None)
    Aid = Author.objects.get(pk=aid)
    if form.is_valid():
        event = Event(A_id=Aid, E_title=request.POST.get('Event_title'),DateE=request.POST.get('DateOfEvent'),\
                      Location=request.POST.get('Location'),Picture=request.POST.get('Picture'))
        #event = Event(A_id=Aid)
        event.save()
        eve = Event.objects.get(E_title=request.POST.get('Event_title'))
        genre1 = request.POST.get('Genre1')
        if not genre1:
            genre1 = None
        genre2 = request.POST.get('Genre2')
        if not genre2:
            genre2 = None
        genre3 = request.POST.get('Genre3')
        if not genre3:
            genre3 = None

        if genre1 is not None:
            obj = event_genre(Title=eve, Genre=genre1)
            try:
                obj.save()
            except IntegrityError:
                err = "This Genre is already alloted to this book"
        if genre2 is not None:
            obj1 = event_genre(Title=eve, Genre=genre2)
            try:
                obj1.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
        if genre3 is not None:
            obj2 = event_genre(Title=eve, Genre=genre3)
            try:
                obj2.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
        return HttpResponseRedirect(reverse('E_library:authorhomepage', args=(aid,)))
    return render(request,'E_library/addevent.html',{'form':form,'aid':aid})


def borrow(request,uid, isbn):
    u = Users.objects.get(pk =uid)
    b = Book.objects.get(Isbn=isbn)
    if request.method == 'POST':
        rate = request.POST.get('ratings')
        if not rate:
            rate = None
        if not None:
            br = borrows(user_id=u,Isbn=b,ratings=rate)
            br.save()
        return HttpResponseRedirect(reverse('E_library:details', args=(uid,isbn)))
    return render(request,'E_library/borrow.html',{'uid':uid,'isbn':isbn})

def deletebook(request,aid):
    book = written_by.objects.filter(A_id=aid)
    all_book = Book.objects.all()
    return render(request,'E_library/delete.html',{'book':book,'aid':aid,'all_book':all_book})

def deleteb(request,aid,isbn):
    book = Book.objects.get(Isbn=isbn)
    a = Author.objects.get(pk=aid)
    w = written_by.objects.get(A_id=a,Isbn=book).delete()
    book.delete()
    return HttpResponseRedirect(reverse('E_library:authorhomepage', args=(aid)))

def editb(request,aid,isbn):
    form = editbookform(request.POST or None, request.FILES or None)
    Aid = Author.objects.get(pk=aid)
    err = ''
    if form.is_valid():
        title = request.POST.get('Title')
        copy = request.POST.get('Copy')
        cover = request.POST.get('Cover')
        i = Book.objects.get(Isbn=isbn)
        obj = Book(Isbn=isbn,Title=title,Copy=copy,Cover=cover)
        obj.save()
        genre1 = request.POST.get('Genre1')
        if not genre1:
            genre1 = None
        genre2 = request.POST.get('Genre2')
        if not genre2:
            genre2 = None
        genre3 = request.POST.get('Genre3')
        if not genre3:
            genre3 = None
        ob = genre_allot.objects.filter(Isbn=i).delete()

        if genre1 is not None:
            obj = genre_allot(Isbn=i, genre=genre1)
            try:
                obj.save()
            except IntegrityError:
                err = "This Genre is already alloted to this book"
        if genre2 is not None:
            obj1 = genre_allot(Isbn=i, genre=genre2)
            try:
                obj1.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
        if genre3 is not None:
            obj2 = genre_allot(Isbn=i, genre=genre3)
            try:
                obj2.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
        return HttpResponseRedirect(reverse('E_library:authorhomepage', args=(aid,)))
    return render(request,'E_library/editform.html',{'form':form,'aid':aid,'isbn':isbn})

def deleteevent(request,aid):
    event = Event.objects.filter(A_id=aid)
    return render(request,'E_library/deleteevent.html',{'event':event,'aid':aid})

def deleteeve(request,aid,title):
    event = Event.objects.filter(E_title=title)
    event.delete()
    return HttpResponseRedirect(reverse('E_library:authorhomepage', args=(aid)))

def editeve(request,aid,title):
    form = addeventform(request.POST or None, request.FILES or None)
    Aid = Author.objects.get(pk=aid)
    if form.is_valid():
        event = Event.objects.get(E_title=title,A_id=Aid)
        event.delete()
        event = Event(A_id=Aid,E_title=request.POST.get('Event_title'),DateE=request.POST.get('DateOfEvent'),\
                      Location=request.POST.get('Location'),Picture=request.POST.get('Picture'))
        event.save()
        genre1 = request.POST.get('Genre1')
        if not genre1:
            genre1 = None
        genre2 = request.POST.get('Genre2')
        if not genre2:
            genre2 = None
        genre3 = request.POST.get('Genre3')
        if not genre3:
            genre3 = None
        t = Event.objects.get(E_title=request.POST.get('Event_title'))
        if genre1 is not None:
            obj = event_genre(Title=t, Genre=genre1)
            try:
                obj.save()
            except IntegrityError:
                err = "This Genre is already alloted to this book"
        if genre2 is not None:
            obj1 = event_genre(Title=t, Genre=genre2)
            try:
                obj1.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
        if genre3 is not None:
            obj2 = event_genre(Title=t, Genre=genre3)
            try:
                obj2.save()
            except IntegrityError:
                err = 'This Genre is already alloted to this book'
        return HttpResponseRedirect(reverse('E_library:authorhomepage', args=(aid,)))
    return render(request, 'E_library/editevent.html', {'form': form, 'aid': aid, 'title':title})


