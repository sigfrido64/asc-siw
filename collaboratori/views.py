# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Collaboratore, Persona
from .forms import NewCollaboratoreForm


# Create your views here.
@has_permission_decorator(SiwPermessi.COLLABORATORI_LISTA_READ)
def lista_collaboratori_view(request):
    # Devo prendere la lista con cognome, nome e poi mettere un link per i dettagli.
    collaboratori = Collaboratore.objects.all()
    return render(request, 'collaboratori/lista_collaboratori.html', {'collaboratori': collaboratori})


@has_permission_decorator(SiwPermessi.COLLABORATORE_MOSTRA)
def mostra_collaboratore_view(request, pk):
    collaboratore = get_object_or_404(Collaboratore, pk=pk)
    return render(request, 'collaboratori/mostra_collaboratore.html', {'collaboratore': collaboratore})


@has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def propone_inserimento_collaboratore_view(request):
    return render(request, 'collaboratori/propone_inserimento_collaboratore.html')


@has_permission_decorator(SiwPermessi.COLLABORATORE_INSERISCE)
def inserisce_nuovo_collaboratore_view(request, pk_persona):
    persona = get_object_or_404(Persona, pk=pk_persona)
    # Se il collaboratore è già anagrafato segnala l'errore e non prosegue.
    try:
        collaboratore = Collaboratore.objects.get(persona__pk=pk_persona)
    except ObjectDoesNotExist:
        pass
    else:
        return render(request, 'collaboratori/errore_collaboratore_gia_presente.html', {'collaboratore': collaboratore})
    # Altrimenti lavoro normalmente come inserimento.
    if request.method == 'POST':
        print("Form con dati")
        form = NewCollaboratoreForm(request.POST)
        if form.is_valid():
            print("Form valido !")
            collaboratore = form.save(commit=False)
            collaboratore.persona = persona
            collaboratore.save()
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to lista collaboratori
        else:
            print(form.errors)
    else:
        print("Form senza dati")
        form = NewCollaboratoreForm()
    return render(request, 'collaboratori/inserisce_collaboratore.html', {'persona': persona, 'form': form})
