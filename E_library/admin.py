from django.contrib import admin

# Register your models here.
from .models import Users
admin.site.register(Users)
from .models import Author

admin.site.register(Author)

from .models import Book

admin.site.register(Book)
from .models import Group

admin.site.register(Group)

from .models import borrows

admin.site.register(borrows)

from .models import belongs_to

admin.site.register(belongs_to)

from .models import written_by

admin.site.register(written_by)

from .models import Event

admin.site.register(Event)

from .models import genre_allot

admin.site.register(genre_allot)

from .models import event_genre

admin.site.register(event_genre)