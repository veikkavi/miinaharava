
import random
import haravasto
import ikkunasto
import datetime

tila = {
    "kentta": [],
    "miinat": 0,
    "lippuja": 0,
    "alku": True,
    "aloitusaika": "",
    "peliaika": "",
    "voitto": False,
    "vuorot": 0
}

def luo_kentta(leveys, korkeus):
    """
    Luo kentän tila-sanakirjaan
    """
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")

    tila["kentta"] = kentta
        

def miinoita(kentta, vapaat_ruudut, n):
    """
    Asettaa kentällä n kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(n):
        miina = random.choice(vapaat_ruudut)
        rivi = kentta[miina[1]]
        rivi[miina[0]] = "x"
        vapaat_ruudut.remove(miina)
        
def uusipeli():
    """
    Tarkistaa kentän tiedot ja luo uuden pelin lataamalla grafiikat ja alkutilan 
    sekä luomalla peli-ikkunan ja hiiren käsittelijän.
    """
    korkeus = ikkunasto.lue_kentan_sisalto(korkeuskentta)
    leveys = ikkunasto.lue_kentan_sisalto(leveyskentta)
    miinat = ikkunasto.lue_kentan_sisalto(miinalkmkentta)
    try:
        korkeus = int(korkeus)
        leveys = int(leveys)
        miinat = int(miinat)
    except ValueError:
        ikkunasto.kirjoita_tekstilaatikkoon(tekstilaatikko, "Anna kentän tiedot kokonaislukuina!")
    else:
        if miinat < 1 or korkeus < 1 or leveys < 1:
            ikkunasto.kirjoita_tekstilaatikkoon(tekstilaatikko, "Arvojen täytyy olla suurempia kuin 0!")
        elif korkeus > 25 or leveys > 45:
            ikkunasto.kirjoita_tekstilaatikkoon(tekstilaatikko, "Kenttä on liian suuri!")
        elif miinat >= leveys * korkeus:
            ikkunasto.kirjoita_tekstilaatikkoon(tekstilaatikko, "Liikaa miinoja!")
        else:
            ikkunasto.lopeta()
            tila["alku"] = True
            tila["vuorot"] = 0
            tila["lippuja"] = 0
            tila["miinat"] = miinat
            tila["voitto"] = False
            luo_kentta(leveys, korkeus)
            haravasto.lataa_kuvat("spritet")
            haravasto.luo_ikkuna(len(tila["kentta"][0]) * 40, len(tila["kentta"]) * 40)
            haravasto.aseta_piirto_kasittelija(piirra_kentta)
            haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
            haravasto.aloita()


def tilastot():
    """
    Luo uuden ikkunan, lukee tilastot tiedostosta ja kirjoittaa 
    ne tekstilaatikkoon. Jos tilastoja tai tiedostoa ei ole, 
    tai niitä ei voi lukea, tulostuu virheviesti.
    """
    ikkunasto.lopeta()
    tilasto_ikkuna = ikkunasto.luo_ikkuna("Tilastot")
    ylakehys = ikkunasto.luo_kehys(tilasto_ikkuna, ikkunasto.YLA)
    alakehys = ikkunasto.luo_kehys(tilasto_ikkuna, ikkunasto.YLA)
    tyhjenna_nappi = ikkunasto.luo_nappi(ylakehys, "Tyhjennä tilastot", tyhjenna_tilastot)
    takaisin_nappi = ikkunasto.luo_nappi(ylakehys, "Takaisin", takaisin_nappi_kasittelija)
    global tilastolaatikko
    tilastolaatikko = ikkunasto.luo_tekstilaatikko(alakehys, 70, 30)
    try:
        with open("tilastot.txt") as luku:
            try:     
                sisalto = luku.readlines()
                if not sisalto:
                    ikkunasto.kirjoita_tekstilaatikkoon(tilastolaatikko, "Tilastoja ei ole.")
                for rivi in sisalto:
                    voitto = ""
                    lista = rivi.split(",")
                    if lista[3] == "True":
                        voitto = "Voitto"
                    elif lista[3] == "False":
                        voitto = "Häviö"
                    ikkunasto.kirjoita_tekstilaatikkoon(tilastolaatikko,
                        "{}\n{}! Pelaaja: {}. Aika: {}. Vuorot: {}\nKentän koko: {}x{}. Miinoja: {}"
                        .format(lista[1], voitto, lista[0], lista[2], lista[4], lista[5], lista[6], lista[7]))
            except IndexError:
                ikkunasto.kirjoita_tekstilaatikkoon(tilastolaatikko,
                    "Tilastoja ei voida lukea. Tyhjennä tilastot", True)
    except FileNotFoundError:
        ikkunasto.kirjoita_tekstilaatikkoon(tilastolaatikko, "Tilastoja ei ole.")
    
def tyhjenna_tilastot():
    """
    Tyhjentää tilasto-tiedoston.
    """
    open("tilastot.txt", "w").close()
    ikkunasto.kirjoita_tekstilaatikkoon(tilastolaatikko, "Tilastoja ei ole.", True)
    
def takaisin_nappi_kasittelija():
    """
    Palaa päävalikkoon.
    """
    ikkunasto.lopeta()
    main()

def lopeta_nappi_kasittelija():   
    """
    Sammuttaa päävalikon.
    """
    ikkunasto.lopeta()
    
def peli_paattyi():
    """
    Näyttää pelin tiedot, kysyy nimimerkkiä ja tallentaa ne tiedostoon. 
    Palaa päävalikkoon kun nappia on painettu.
    """
    haravasto.lopeta()
    if tila["voitto"]:
        viesti = "Voitit"
    else:
        viesti = "Hävisit"
    pvm = datetime.datetime.now()
    aloitusaika = tila["aloitusaika"]
    aika_s = (pvm - aloitusaika).total_seconds()
    aika = ("{}min {:.1f}s".format(int(aika_s / 60), aika_s % 60))
    aikaleima = aloitusaika.strftime("%d.%m.%Y klo:%H.%M")
    tila["aloitusaika"] = aikaleima
    tila["peliaika"] = aika
    tallennus_ikkuna = ikkunasto.luo_ikkuna("{} pelin!".format(viesti))
    ylakehys = ikkunasto.luo_kehys(tallennus_ikkuna, ikkunasto.YLA)
    alakehys = ikkunasto.luo_kehys(tallennus_ikkuna, ikkunasto.YLA)
    nimiohje = ikkunasto.luo_tekstirivi(ylakehys, "Nimimerkki:")
    global nimikentta
    nimikentta = ikkunasto.luo_tekstikentta(ylakehys)
    tallenna_nappi = ikkunasto.luo_nappi(ylakehys, "Tallenna peli", tallenna_tilastot)
    ohita_nappi = ikkunasto.luo_nappi(ylakehys, "Ohita", takaisin_nappi_kasittelija)
    global tallennus_ikkuna_laatikko
    tallennus_ikkuna_laatikko = ikkunasto.luo_tekstilaatikko(alakehys, 40, 30)
    ikkunasto.kirjoita_tekstilaatikkoon(tallennus_ikkuna_laatikko,
        "{} pelin.\nAika: {}\nVuorot: {}\nKentän koko: {}x{}\nMiinoja: {}\nPäivämäärä: {}."
        .format(viesti, aika, tila["vuorot"], len(tila["kentta"][0]),
        len(tila["kentta"]), tila["miinat"], aikaleima))
    ikkunasto.kaynnista()
    
def tallenna_tilastot():
    """
    Tallentaa tilastot tiedostoon
    """
    nimi = ikkunasto.lue_kentan_sisalto(nimikentta)
    if not nimi:
        ikkunasto.kirjoita_tekstilaatikkoon(tallennus_ikkuna_laatikko, "Anna jokin nimimerkki")
    else:
        with open("tilastot.txt", "a+") as tiedosto:
            tiedosto.write("{},{},{},{},{},{},{},{}\n".format(nimi, tila["aloitusaika"], tila["peliaika"], 
                tila["voitto"], tila["vuorot"], len(tila["kentta"][0]), len(tila["kentta"]), tila["miinat"]))
        ikkunasto.lopeta()
        main()
                     
def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kentän ruudut näkyviin peli-ikkunaan. 
    Funktiota kutsutaan aina kun peli pyytää ruudun näkymän päivitystä.
    Piirtää myös käytettyjen lippujen sekä miinojen määrän näkyviin.
    """
    kentta = tila["kentta"]  
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for i, rivi in enumerate(reversed(kentta)):
        for j, sarake in enumerate(rivi):
            if sarake == "fx":
                haravasto.lisaa_piirrettava_ruutu("f", j * 40, i * 40)
            elif sarake == "x":
                haravasto.lisaa_piirrettava_ruutu(" ", j * 40, i * 40)
            else:
                haravasto.lisaa_piirrettava_ruutu(sarake, j * 40, i * 40)
    
    haravasto.piirra_ruudut() 
    haravasto.piirra_tekstia("Lippuja: {}/{}".format(tila["lippuja"], tila["miinat"]),
        0, 0, (255, 0, 0, 255), "serif", 15)

def laske_miinat(x, y):
    """
    Laskee kentällä yhden ruudun ympärillä olevat miinat ja palauttaa
    niiden lukumäärän.
    """
    huone = tila["kentta"]   
    miinat = 0
    y1 = y - 1
    y2 = y + 2
    x1 = x - 1
    x2 = x + 2
    a = 0
    b = 0
    if y1 < 0:
        y1 = 0
    if x1 < 0:
        x1 = 0
    if y2 > len(huone):
        y2 = len(huone)
    for a in huone[y1:y2]:
        if x2 > len(a):
            x2 = len(a)
        for b in a[x1:x2]: 
            if b == "x" or b == "fx":
                miinat += 1
    
    return miinat
        
def kasittele_hiiri(x, y, painike, muokkaus):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Funktio kutsuu peli funktiota oikean ruudun kohdalta. Jos peli on alussa, 
    funktio kutsuu miinoita-funktiota, ja asettaa aloitusajan.
    """
    if tila["alku"]:
        jaljella = []
        aloitusruutu = (x // 40, len(tila["kentta"]) - y // 40 - 1)
        for a in range(len(tila["kentta"][0])):
            for b in range(len(tila["kentta"])):
                jaljella.append((a, b))
                
        jaljella.remove(aloitusruutu)    
        miinoita(tila["kentta"], jaljella, tila["miinat"])
        tila["alku"] = False
        tila["aloitusaika"] = datetime.datetime.now()
        
        
    a = x // 40
    b = len(tila["kentta"]) - y // 40 - 1
    peli(a, b, painike)
      
def peli(x, y, painike):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä. Jos ruudussa on miina, häviää.
    Jos painetaan hiiren oikeaa painiketta, merkitään ruutuun lippu.
    Jos kaikki vapaat ruudut on avattu, voittaa pelin.
    """
    kentta = tila["kentta"]
    if painike == haravasto.HIIRI_OIKEA:
        if kentta[y][x] == "x":
            kentta[y][x] = "fx"
            tila["lippuja"] += 1
        elif kentta[y][x] == " ":
            kentta[y][x] = "f"
            tila["lippuja"] += 1
        elif kentta[y][x] == "f":
            kentta[y][x] = " "
            tila["lippuja"] -= 1
        elif kentta[y][x] == "fx":
            kentta[y][x] = "x"  
            tila["lippuja"] -= 1
    if painike == haravasto.HIIRI_VASEN:
        if tila["voitto"]:
            peli_paattyi()
        if kentta[y][x] == "x":
            tila["voitto"] = False
            peli_paattyi()
        if kentta[y][x] == " ":
            tila["vuorot"] += 1
            lista = [(x, y)]
            while len(lista) > 0:
                ruutu = lista.pop()
                kentta[ruutu[1]][ruutu[0]] = str(laske_miinat(ruutu[0], ruutu[1]))
                if kentta[ruutu[1]][ruutu[0]] == "0":
                    for y in range(-1, 2):
                        if ruutu[1] + y >= 0 and ruutu[1] + y < len(kentta):
                            for x in range(-1, 2):
                                if ruutu[0] + x >= 0 and ruutu[0] + x < len(kentta[0]):
                                    if kentta[ruutu[1] + y][ruutu[0] + x] == " ":
                                            lista.append((ruutu[0] + x, ruutu[1] + y))                             
    for rivi in kentta:
        if " " in rivi or "f" in rivi:
            tila["voitto"] = False
            break
        else:
            tila["voitto"] = True
      
def main():
    """
    Luodaan aloitusvalikko, josta voi valita uuden pelin, lopettamisen ja 
    tilastojen katsomisen. Uuteen peliin voi valita kentän koon 
    sekä miinojen määrän
    """
    alku_ikkuna = ikkunasto.luo_ikkuna("Miinaharava")
    ylakehys = ikkunasto.luo_kehys(alku_ikkuna, ikkunasto.YLA)
    alakehys = ikkunasto.luo_kehys(alku_ikkuna, ikkunasto.YLA)
    syotekehys = ikkunasto.luo_kehys(ylakehys, ikkunasto.VASEN)
    nappikehys1 = ikkunasto.luo_kehys(ylakehys, ikkunasto.VASEN)
    nappikehys2 = ikkunasto.luo_kehys(ylakehys, ikkunasto.VASEN)
    uusipelinappi = ikkunasto.luo_nappi(syotekehys, "Uusi peli", uusipeli)
    tilastonappi = ikkunasto.luo_nappi(nappikehys1, "Katso tilastoja", tilastot)
    lopetusnappi = ikkunasto.luo_nappi(nappikehys2, "Lopeta", lopeta_nappi_kasittelija)
    leveysohje = ikkunasto.luo_tekstirivi(syotekehys, "Kentän leveys:")
    global leveyskentta
    leveyskentta = ikkunasto.luo_tekstikentta(syotekehys)
    korkeusohje = ikkunasto.luo_tekstirivi(syotekehys, "Kentän korkeus:")
    global korkeuskentta    
    korkeuskentta = ikkunasto.luo_tekstikentta(syotekehys)
    miinalkmohje = ikkunasto.luo_tekstirivi(syotekehys, "Miinojen lukumäärä:")
    global miinalkmkentta
    miinalkmkentta = ikkunasto.luo_tekstikentta(syotekehys)
    global tekstilaatikko
    tekstilaatikko = ikkunasto.luo_tekstilaatikko(alakehys,44 , 20)
    ikkunasto.kaynnista()    
    
if __name__ == "__main__": 
    main()
    