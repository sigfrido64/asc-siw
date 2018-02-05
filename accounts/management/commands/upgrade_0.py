from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from accounts.models import Profile, Ruoli


class Command(BaseCommand):
    help = 'Upgrade existing database to version 0.0'

    """def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)
    """

    def handle(self, *args, **options):
        # Cerco gli utenti senza profilo.
        users = User.objects.filter(profile=None)
        # A questi creo un profilo.
        for user in users:
            Profile.objects.create(user=user)
        # Adesso loop su tutti gli utenti per assegnazione del ruolo di default 'mdl'
        utenti = User.objects.all()
        for utente in utenti:
            self.stdout.write(self.style.SUCCESS('Aggiornamento Utente : ' + utente.username))
            utente.profile.ruoli = str({'mdl'})
            utente.profile.permessi = set()
            utente.profile.negati = set()
            utente.save(force_update=True)
            
        # Infine creo il ruolo
        ruolo = Ruoli()
        ruolo.ruolo = 'mdl'
        ruolo.permessi = Profile.mdl
        ruolo.save()
        
        self.stdout.write(self.style.SUCCESS('Database aggiornato'))

