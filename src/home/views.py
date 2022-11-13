from tkinter.tix import Select
from django.shortcuts import render
from dashboard.models import Histo
from dashboard.models import Projet
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count


# Create your views here.
def home(request):
    context = {}
    context["histos"] = Histo.objects.all()[:10]

    projets = set()
    
    print(Projet.objects.order_by())
    for projet in Projet.objects.order_by(): #récupére tous les projets
        projets.add(Histo.objects.filter(projetId = projet).order_by('-dateRel')[0])

    projetRels = Histo.objects.values("projetId").annotate(hcount=Count("projetId"))

    histo = zip(projets,projetRels)
    
    if not request.user.is_authenticated:
        return render(request, 'home/public.html', context= context)
    return render(request, 'home/private.html', {'histo': histo})


