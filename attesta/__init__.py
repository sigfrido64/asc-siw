"""
In questo modulo mi occupo della produzione delle stampe per tutto il sistema.

La radice è /attesta/
A scendere
    /attesta/mdl/ : Per i corsi MDL
    /attesta/fci/ : Per i corsi FCI


Nomi dei files.
Le dichiarazioni devono essere salvate con la seguente convenzione :

- iscrizione_mdl : Dichiarazione di iscrizione mdl.
- frequenza_mdl : Dichirazione di frequenza mdl.
- frequenza_mdl_gg : Dichiarazione di frequenza mdl con analitico delle presenze.
- esame_pre_qualifica : Dichiarazione dei giorni di esame previsti per esame di qualifica.
- esame_post_qualifica : Dichiarazione dei giorni di esame effettivi dopo esame di qualifica.
- esame_pre_special : Dichiarazione dei giorni di esame previsti per esame di specializzazione.
- esame_post_special : Dichiarazione dei giorni di esame effettivi dopo esame di specializzazione.

TIP) Le eventuali diverse tipologie della stessa domanda vanno salvate differenziandole con un _t[0-9].
Quindi tutte le dichiarazioni come iscrizione_mdl_t[0-9] saranno trattate allo stesso modo ma avranno un template
diverso per quanto con gli stessi campi. E' il caso delle dichiarazioni di frequenza che usano un file diverso per
gruppo di giorni di corso.

TIP) La descrizione dei giorni di esame va messa nel record di estensione dei corsi in quanto, al momento, l'ambiente
di questo sistema e quello di SQLServer sono separati.

TIP) La descrizione dei giorni d'esame con il relativo calendario va su più righe e per andare a capo devo usare il
newline di word per i docx che è <w:br/>
"""