from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
def profile(request):
    user = request.user
    return HttpResponse("profile: " + str(user) + 
                        "<br> nom: " + user.first_name + " " + user.last_name + 
                        "<br> email: " + user.email)

# Create your views here.
def index(request):
    return render(request, "index.html")

def editar_equip(request):
    return render(request, "editar_equip_ajax.html")

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    # email = forms.EmailField()
    
def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio', lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

def classificacio(request,lliga_id):
    lliga = get_object_or_404(Lliga, pk=lliga_id)

    equips = lliga.equip_set.all()
    classi = []
    
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partit_set.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partit_set.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append( (punts,equip.nom) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga":lliga,
                })

class CrearLligaForm(forms.Form):
    nom = forms.CharField(max_length=100)

def crearLliga(request):
    form = CrearLligaForm()
    if request.method == "POST":
        form = CrearLligaForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get("nom")
            validateNom = True
            
            if Lliga.objects.filter(nom=nom).exists():
                form.errors["nom"] = ["Ja existeix una lliga amb aquest nom"]
                validateNom = False

            if validateNom:
                lliga = Lliga(nom=nom)
                lliga.save()
                return redirect('menu')
    return render(request, "crearLliga.html",{
                    "form": form,
            })

class crearEquipForm(forms.ModelForm):
    class Meta:
        model = Equip
        fields = ['nom', 'lligues']
        

def crearEquip(request):
    form = crearEquipForm()
    # Poner valores por defecto
    # form = crearEquipForm(initial = {"nom": "Hola"})

    if request.method == "POST":
        form = crearEquipForm(request.POST)
        if form.is_valid():
            validateNom = True
            nom = form.cleaned_data.get("nom")

            if Equip.objects.filter(nom=nom).exists():
                form.errors["nom"] = ["Ja existeix un equip amb aquest nom"]
                validateNom = False

            if validateNom:
                equip = form.save()
                return redirect('menu')
    return render(request, "crearEquip.html",{
                    "form": form,
            })
