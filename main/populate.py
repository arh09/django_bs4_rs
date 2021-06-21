import urllib

from bs4 import BeautifulSoup
from .models import Usuario, Perfume, Puntuacion
import csv

path = "data"


def deleteTables():
    Puntuacion.objects.all().delete()
    Perfume.objects.all().delete()
    Usuario.objects.all().delete()


def populateUsers():
    print("Loading users...")

    lista = []
    dict = {}
    with open(path + '/usuarios.txt', 'r') as f:
        for row in csv.reader(f, delimiter='\t'):
            print(row)
            id_u = int(row[0].strip())
            u = Usuario(id=id_u, anyo_nacimiento=row[1].strip(), pais=row[2].strip())
            lista.append(u)
            dict[id_u] = u

        f.close()
        Usuario.objects.bulk_create(lista)

    print("Usuarios insertados: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")
    return dict


def populatePerfumes():
    print("Loading perfumes...")
    Perfume.objects.all().delete()
    lista = []
    dict = {}

    f = urllib.request.urlopen("https://perfumeria.com/perfumes/")
    s = BeautifulSoup(f, "lxml")
    l = s.find_all("div", class_="imagen")
    id_pe = 0
    for i in l:
        a = i.find("a")
        p = urllib.request.urlopen(a['href'])
        s = BeautifulSoup(p, "lxml")
        nombre = s.find("div", class_="nombre").text.strip()
        cantidad = s.find("div", class_="nombre_corto").text.strip()
        precio = s.find("div", class_="precio").text.strip()
        pe = Perfume(id=id_pe, nombre=nombre, cantidad=cantidad, precio=precio)
        lista.append(pe)
        dict[id_pe] = pe
        id_pe += 1
    Perfume.objects.bulk_create(lista)
    print("Perfumes insertados: " + str(Perfume.objects.count()))
    print("---------------------------------------------------------")
    return lista


def populatePuntuaciones(u, p):
    print("Loading ratings...")
    Puntuacion.objects.all().delete()

    lista = []
    with open(path + '/puntuaciones.txt', 'r') as f:
        for row in csv.reader(f, delimiter='\t'):
            print(row)
            lista.append(Puntuacion(
                usuario_id=u[int(row[1].strip())],
                perfume_id=p[int(row[0].strip())],
                puntuacion=row[2].strip(),
            ))
        f.close()
        Puntuacion.objects.bulk_create(lista)

    dict = {}
    for rating in Puntuacion.objects.all():
        dict[rating.id] = rating

    print("Ratings inserted: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")
    return dict


def populateDatabase():
    deleteTables()
    u = populateUsers()
    p = populatePerfumes()
    populatePuntuaciones(u, p)
    print("Finished database population")


if __name__ == '__main__':
    populateDatabase()
