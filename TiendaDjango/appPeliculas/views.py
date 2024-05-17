from django.shortcuts import render
from django.db import Error
from appPeliculas.models import Genero,Pelicula
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')
def vistaAgregarGenero(request):
    return render(request, 'agregarGenero.html')    
# @csrf_exempt
def agregarGenero(request):
        try:
            nombre=request.POST['txtNombre']
            genero=Genero(genNombre=nombre)
            genero.save()
            mensaje="Genero Agregado Correctamente"
        except Error as error:
            mensaje=str(error)
        retorno={"mensaje":mensaje}
        return render(request,"agregarGenero.html",retorno)
    
    
def listarPeliculas(request):
    # peliculas=Pelicula.objects.all().values()
    peliculas=Pelicula.objects.all()
    
    retorno={"peliculas":peliculas}
    # return JsonResponse(retorno)
    return render(request,"listarPeliculas.html",retorno)

def vistaAgregarPelicula (request):
    generos=Genero.objects.all()
    retorno={"generos":generos}
    return render(request,"agregarPelicula.html",retorno)

def agregarPelicula (request):
    try:
        codigo=request.POST['txtCodigo']
        titulo=request.POST['txtTitulo']
        protagonista=request.POST['txtProtagonista']
        duracion=int(request.POST['txtDuracion'])
        resumen=request.POST['txtResumen']
        foto=request.FILES['fileFoto']
        idgenero=int(request.POST['cbGenero'])
        # De esta manera se consulta el id
        genero=Genero.objects.get(pk=idgenero)
        
        #crear objeto pelicula
        pelicula=Pelicula(pelCodigo=codigo,pelTitulo=titulo,pelProtagonista=protagonista,pelDuracion=duracion,pelResumen=resumen,pelFoto=foto,pelGenero=genero)
        pelicula.save()
        
        mensaje="Pelicula Agregada Correctamente"
        
    except Error as error:
        mensaje=str(error)
        
    retorno={"mensaje":mensaje,'idPelicula':pelicula.id}
    
    # return JsonResponse(retorno)
    return render(request,"agregarPelicula.html",retorno)
