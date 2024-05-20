from django.shortcuts import render
from django.db import Error
from appPeliculas.models import Genero,Pelicula
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from bson import ObjectId
from django.shortcuts import render, redirect
import os
from django.conf import settings;

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
def eliminarPelicula(request, id):
    try:
        PeliEliminar = Pelicula.objects.get(pk=ObjectId(id))
        PeliEliminar.delete()
        mensaje = "Eliminado Correctamente"
    except Error as error:
        mensaje = str(error)
    retorno={"mensaje":mensaje}
    
    return redirect ("/")
def editarPelicula(request):
    try:
        IDPelicula = ObjectId(request.POST['IDPelicula'])
        peliculaeditar = Pelicula.objects.get(pk=IDPelicula)
        peliculaeditar.pelCodigo = request.POST["codigo"]
        peliculaeditar.pelTitulo = request.POST["titulo"]
        peliculaeditar.pelProtagonista = request.POST["protagonista"]
        peliculaeditar.pelDuracion = int(request.POST["duracion"])
        peliculaeditar.pelResumen = request.POST["resumen"]
        if 'foto' in request.FILES:
            foto = request.FILES["foto"]
            if peliculaeditar.pelFoto:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(peliculaeditar.pelFoto)))
            peliculaeditar.pelGenero = foto
        IDGenero = ObjectId(request.POST["IDGenero"])
        Genero = Genero.objects.get(pk=IDGenero)
        peliculaeditar.pelGenero = Genero
        peliculaeditar.save()
        mensaje = "Ha sido editado correctamente"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    return redirect("/")
