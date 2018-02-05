# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from django.contrib.auth.models import User
from django.test import TestCase
from ..models import get_real_perms, Ruoli


class RealPermsTests(TestCase):
    """
    Testing : get_real_perms
    In questo test case controllo che nella funzione i permssi negati prevalgano su quelli concessi e che questo valga
    anche per i permessi che arrivano dai ruoli.
    """
    
    # Crea l'utente per le prove.
    def setUp(self):
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.myuser = User.objects.get(username=self.username)

    def test_tutti_permessi_concessi(self):
        # Controlla che i permessi dell'utente arrivino tutti alla fine.
        # Salvo il modello altrimenti nella routine che chiama non trova i dati
        self.myuser.profile.permessi = {'primo', 'secondo'}
        self.myuser.save(force_update=True)
        
        # In questa condizione devo trovare tutti e due i permessi.
        permessi = get_real_perms(self.myuser)
        self.assertEqual(permessi, {'primo', 'secondo'})

    def test_permessi_negati_prevalgono_su_concessi(self):
        # Controlla che i permessi negati comportino la cancellazione di quelli permessi.
        self.myuser.profile.permessi = {'primo', 'secondo'}
        self.myuser.profile.negati = {'secondo'}
        self.myuser.save(force_update=True)

        # In questa condizione devo trovare solo 'primo'
        permessi = get_real_perms(self.myuser)
        self.assertEqual(permessi, {'primo'})

    def test_permessi_dei_ruoli_siano_assegnati_all_utente(self):
        # Controlla che i permessi del ruolo vengano assegnati tutti all'utente.
        # Creo il ruolo e lo salvo.
        ruolo = Ruoli()
        ruolo.ruolo = 'test'
        ruolo.permessi = {'primo', 'secondo'}
        ruolo.save()
        # Assegno l'utente a quel ruolo.
        self.myuser.profile.ruoli = {'test'}
        self.myuser.save(force_update=True)

        # In questa condizione devo trovare solo 'primo' e 'secondo'
        permessi = get_real_perms(self.myuser)
        self.assertEqual(permessi, {'primo', 'secondo'})

    def test_ruoli_permessi_negati_prevalgano_su_ruoli_permessi_concessi(self):
        # Controlla che i permessi del ruolo vengano assegnati togliendo quelli negati dal ruolo stesso.
        # Creo il ruolo e lo salvo.
        ruolo = Ruoli()
        ruolo.ruolo = 'test'
        ruolo.permessi = {'primo', 'secondo'}
        ruolo.negati = {'secondo'}
        ruolo.save()
        # Assegno l'utente a quel ruolo.
        self.myuser.profile.ruoli = {'test'}
        self.myuser.save(force_update=True)

        # In questa condizione devo trovare solo 'primo'
        permessi = get_real_perms(self.myuser)
        self.assertEqual(permessi, {'primo'})
