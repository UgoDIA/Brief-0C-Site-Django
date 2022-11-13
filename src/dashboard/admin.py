from django.contrib import admin

# Register your models here.

from dashboard.models import Projet, Histo, Stopgo, Threads, Comments, Statut, Stopgo

admin.site.register(Projet)
admin.site.register(Histo)
admin.site.register(Threads)
admin.site.register(Comments)
admin.site.register(Statut)
admin.site.register(Stopgo)