import shelve

from django.shortcuts import render, get_object_or_404

from .models import Puntuacion, Perfume, Usuario
from .forms import PerfumeForm
from .populate import populateDatabase
from .recommendations import transformPrefs, calculateSimilarItems, getRecommendations


def recommendedPerfumes(request):
    if request.method == 'POST':
        form = PerfumeForm(request.POST)
        if form.is_valid():
            idPerfume = form.cleaned_data['id']
            perfume = get_object_or_404(Perfume, pk=idPerfume)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['ItemsPrefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idPerfume))
            recommended = rankings[:3]
            perfumes = []
            scores = []
            for re in recommended:
                perfumes.append(Usuario.objects.get(pk=re[1]))
                scores.append(re[0])
            items = zip(perfumes, scores)
            return render(request, 'recommendationPerfumes.html', {'perfume': perfume, 'items': items})
    else:
        form = PerfumeForm()
    return render(request, 'search_perfume.html', {'form': form})

def loadDict():
    Prefs = {}  # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.usuario_id.id)
        itemid = int(ra.perfume_id.id)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems'] = calculateSimilarItems(Prefs, n=10)
    shelf.close()


#  CONJUNTO DE VISTAS

def index(request):
    return render(request, 'index.html')


def populateDB(request):
    populateDatabase()
    return render(request, 'populate.html')


def loadRS(request):
    loadDict()
    return render(request, 'loadRS.html')
