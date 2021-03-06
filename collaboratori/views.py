# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from siw.decorators import has_permission_decorator
from accounts.models import SiwPermessi
from .models import Collaboratore, Persona
from .forms import NewCollaboratoreForm, UpdateCollaboratoreForm


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
        form = NewCollaboratoreForm(request.POST)
        if form.is_valid():
            collaboratore = form.save(commit=False)
            collaboratore.persona = persona
            collaboratore.save()
            return redirect('collaboratori:lista_collaboratori')
    else:
        form = NewCollaboratoreForm(initial={'tel1': persona.tel1, 'tel2': persona.tel2, 'tel3': persona.tel3,
                                             'tel4': persona.tel4, 'doc_tel1': persona.doc_tel1,
                                             'doc_tel2': persona.doc_tel2, 'doc_tel3': persona.doc_tel3,
                                             'doc_tel4': persona.doc_tel4, 'mail1': persona.mail1,
                                             'mail2': persona.mail2, 'doc_mail1': persona.doc_mail1,
                                             'doc_mail2': persona.doc_mail2,
                                             'persona': persona})
    return render(request, 'collaboratori/inserisce_collaboratore.html', {'persona': persona, 'form': form})


@has_permission_decorator(SiwPermessi.COLLABORATORE_MODIFICA)
def modifica_collaboratore_view(request, pk_collaboratore):
    # Se il collaboratore non esiste segnala l'errore e non prosegue.
    try:
        collaboratore = Collaboratore.objects.get(pk=pk_collaboratore)
    except ObjectDoesNotExist:
        return render(request, 'collaboratori/errore_collaboratore_non_esiste.html', {'pk': pk_collaboratore})
    persona = collaboratore.persona
    # Altrimenti prosegue con la modifica.
    if request.method == 'POST':
        form = UpdateCollaboratoreForm(request.POST, instance=collaboratore)
        if form.is_valid():
            collaboratore.save()
            return redirect('collaboratori:lista_collaboratori')
    else:
        form = UpdateCollaboratoreForm(instance=collaboratore)
    return render(request, 'collaboratori/modifica_collaboratore.html', {'form': form, 'persona': persona})

