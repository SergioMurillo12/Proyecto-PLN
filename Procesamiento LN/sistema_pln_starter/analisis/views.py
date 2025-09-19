from django.shortcuts import render, redirect
from .forms import TextoAnalizadoForm
from .nlp_utils import clean_text_to_tokens
from .models import TextoAnalizado

# Vista para listar los textos
def lista_textos(request):
    textos = TextoAnalizado.objects.all()
    return render(request, 'analisis/lista_textos.html', {'textos': textos})

def subir_texto(request):
    tokens = []
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            texto_obj = form.save()  # guarda el archivo

            # Leer archivo correctamente
            with texto_obj.archivo.open('r') as archivo:
                texto = archivo.read()

            # Analizar texto
            tokens = clean_text_to_tokens(texto)
            return render(request, 'analisis/resultado.html', {'tokens': tokens})
    else:
        form = TextoAnalizadoForm()

    return render(request, 'analisis/subir_texto.html', {'form': form})
