"""
In questo modulo mi occupo della produzione delle stampe per tutto il sistema.

La radice è /attesta/
A scendere
    /attesta/mdl/ : Per i corsi MDL
    /attesta/fci/ : Per i corsi FCI


Nomi dei files.
Le dichiarazioni devono essere salvate con la seguente convenzione :

- iscrizione_mdl : Dichiarazione di iscrizione mdl
- frequenza_mdl : Dichirazione di frequenza mdl


Le eventuali diverse tipologie della stessa domanda vanno salvate differenziandole con un _t[0-9].
Quindi tutte le dichiarazioni come iscrizione_mdl_t[0-9] saranno trattate allo stesso modo ma avranno un template
diverso per quanto con gli stessi campi. E' il caso delle dichiarazioni di frequenza che usano un file diverso per
gruppo di giorni di corso.
"""