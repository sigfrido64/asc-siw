ATTENZIONE

Django-Widget-Tweaks NON funziona con Django 2.0 se non fai il fix indicato in :

https://github.com/simhnna/django-widget-tweaks/commit/a327bbe205e2d1299dd7eaf28cf89146c5868ff9

In sostanza basta un cast a str e tutto funziona !!!


ATTENZIONE ! TEST ! ATTENZIONE

Nei test quando non trova un url su cui fare il reverse match NON DA ERRORE e salta semplicemente il template che
contiene l'errore. C'è da diventare matti perchè il template viene chiamato ma non esce un carattere nella risposta
HTML !!!!!

Per i test uso questa funzione per il debug delle risposte.

def response_debug(response):
    print('\nresponse :', response)
    print('\ncontent : ', response.content)
    print('\nurl match : ', response.resolver_match)
    for template in response.templates:
        print('\n template : ', template.name)



MIGRAZIONI

Se le voglio resettare l'articolo di Simple è il migliore.
1) Cancello fisicamente tutti i files delle migrazioni.
2) Nel DB cancello i dati delle migrazioni uno per uno.
3) Poi lancio il migrate --fake-initial così le applica per finta e siamo tutti contenti !
