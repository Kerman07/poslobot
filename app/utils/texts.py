from viberbot.api.messages.text_message import TextMessage

conversation_started = TextMessage(
    text="Zdravo, ja sam Poslobot, da bi počeli koristiti moje usluge pošaljite mi poruku"
)

subscribed = TextMessage(
    text="""Dobro došli!\n
    Svaki dan u 18:00h ćete dobijati poruku sa objavljenim poslovima toga dana.\n
    Da bi postavili kategorije koje vas interesuju pošaljite Cat\n
    Da bi promjenili lokaciju poslova pošaljite Loc\n
    Da vidite sve dostupne komande pošaljite Help.
    """
)

categories = [
    TextMessage(
        text="""Da bi postavili željene kategorije pošaljite cat i listu kategorija odvojenu sa .\n
    Npr. Cat 23.24.37
    """
    ),
    TextMessage(
        text="""Lista dostupnih kategorija:\n
        1 Administrativne i slične usluge
        2 Arhitektonske usluge
        3 Bankarstvo
        4 Biotehnologija i farmacija
        5 Konsalting
        6 Državna služba i uprava
        7 Ekonomija i finansije
        8 Građevinarstvo
        11 Zanatske usluge
        12 Menadžment i upravljanje
        13 Marketing - PR
        14 Mediji
        15 Obrazovanje
        16 Osiguranje
        17 Ostalo
        18 Policija - Zaštitarske usluge
        19 Poljoprivreda - Ribarstvo - Šumarstvo
        20 Pravo
        21 Proizvodnja
        22 Računovodstvo - Revizija
        23 Socijalne usluge - Neprofitne organizacije
        24 Telekomunikacije
        25 Transport - Skladištenje i logika
        26 Turizam
        27 Ugostiteljstvo
        29 Nauka - Istraživački rad
        31 Energetika
        32 Elektrotehnika - Mašinstvo
        33 Zdravstvo
        34 Komercijala - Prodaja
        37 Mali oglasi
        38 Ljepota i zdravlje
        39 Prehrambena industrija
        42 Grafički dizajn
        43 Nekretnine
        45 Saobraćaj i komunikacije
        46 Ekologija
        47 IT
        48 Grafička industrija
        49 Ekonomija, finansije i računovodstvo
        50 Ugostiteljstvo i turizam
        51 Ljudski resursi
    """
    ),
]