import sys

lines = []
for line in sys.stdin:
    lines.append(line)


def main():
    # 1 redak: Ulazni nizovi odvojeni znakom |. Simboli svakog pojedinog niza odvojeni su zarezom.
    ulazni_nizovi = (lines[0].strip().split('|'));
    # 2. redak: Skup stanja odvojenih zarezom
    Q = (lines[1].strip().split(','));
    # 3. redak: Skup ulaznih znakova odvojenih zarezom
    E = (lines[2].strip().split(','));
    # 4. redak: Skup znakova stoga odvojenih zarezom
    T = lines[3].strip().split(',')
    # 5. redak: Skup prihvatljivih stanja odvojenih zarezom
    F = lines[4].strip().split(',')
    # 6. redak: Početno stanje
    q0 = lines[5].strip()
    # 7. redak: Početni znak stoga
    z = lines[6].strip()
    # 8. redak i svi ostali retci: Funkcija prijelaza u formatu
    d = {}
    # populacija prijelaza, lijeva strana kljuc, desna vrijednost
    for line in lines[7:]:
        ulazi, izlazi = line.strip().split("->")
        d[ulazi] = izlazi

    #print("Prihvatljiva stanja su.... ")
    #print(T)
    #print("Biblioteka prijelaza je: ", d)
    # rjesavanje
    for ulazni_niz in ulazni_nizovi: 
        ulazni_niz = ulazni_niz.split(',')
        rez =[]
        stog = []
        stog.append(z)
        trenutno_stanje = q0 
        #print("Ulazni niz je... ", ulazni_niz)
        #print("Duljina ulaznog niza je ", len(ulazni_niz))

        rez.append(f"{trenutno_stanje}#{stog[0]}|") #OPREZ
        i = 0
        brojac = 0 # za potrebe zaustavljanja beskonacne petlje

        while i < len(ulazni_niz): #iteriraj kroz znakove ulaznog niza
            stari_i = i # da znam kada povecavati brojac
            # prvo moramo provjeriti postoji li fja prijelaza koja odgovara 
            if len(stog) > 0:
                    stog_top = stog[0]
            else:
                stog_top = '$'

            kljuc = f"{trenutno_stanje},{ulazni_niz[i]},{stog_top}"
            kljuc2 = f"{trenutno_stanje},$,{stog_top}"

            if kljuc in d:
                # popamo zadnji element stoga 
                stog.pop(0)
                djelovi = d[kljuc].split(",")
                # novo stanje je prvi element iz vrijednosti
                trenutno_stanje = djelovi[0]
                # drugi element vrijednosti je niz znakova od kojih je svaki znak element koji cemo pushati na stog 
                novi_el_stoga = list(djelovi[1])
                if novi_el_stoga[0] != '$': 
                    for el in novi_el_stoga[::-1]: 
                        # znak na vrhu stoga nakon prijelaza je krajnje lijevi
                        stog.insert(0, el)

                #sredivanje rezultata 
                rez.append(f"{trenutno_stanje}#")
                if len(stog) > 0: 
                    for el in stog: 
                        rez.append(el)
                else: 
                    rez.append('$')
                rez.append('|')
            
            # ako nema fje prijelaza moramo vidjeti moze li se naci u epsilon okolini
            elif kljuc2 in d:
                # popamo zadnji element stoga 
                stog.pop(0)
                djelovi = d[kljuc2].split(",")
                # novo stanje je prvi element iz vrijednosti
                trenutno_stanje = djelovi[0]
                # drugi element vrijednosti je niz znakova od kojih je svaki znak element koji cemo pushati na stog 
                novi_el_stoga = list(djelovi[1])
                if novi_el_stoga[0] != '$': 
                    for el in novi_el_stoga[::-1]: 
                        # znak na vrhu stoga nakon prijelaza je krajnje lijevi
                        stog.insert(0, el)

                #sredivanje rezultata 
                rez.append(f"{trenutno_stanje}#")
                if len(stog) > 0: 
                    for el in stog: 
                        rez.append(el)
                else: 
                    rez.append('$')
                rez.append('|')
                # VAZNO - vrati i za 1 da se ne bi progutao ulazni znak 
                i = i - 1
                brojac = brojac  + 1

            # ako se ne nalazi niti u epsilonu niti na pocetnoj 
            else:
                rez.append('fail|')
                trenutno_stanje = -1 
                break

            i = i + 1
            if stari_i == i: # znaci da se nije pomakao niz, epsilon se dogodio
                brojac = brojac + 1
            else: # niz se pomakao
                brojac = 0

        # GOTOVI S ITERACIJOM - sada moramo provjeriti konacna stanja 
        #print("Zavrsno stanje je", trenutno_stanje)
        if trenutno_stanje in F: #ako je u prihvatljivim stanjima 
            rez.append('1')
        else: # moramo provjeriti epsilon okolinu 
            brojac = 0
            while(brojac < 100): 
                if len(stog) > 0:
                            stog_top = stog[0]
                else:
                    stog_top = '$'
                kljuc2 = f"{trenutno_stanje},$,{stog_top}"
                
                if kljuc2 in d:
                    # popamo zadnji element stoga 
                    stog.pop(0)
                    djelovi = d[kljuc2].split(",")
                    # novo stanje je prvi element iz vrijednosti
                    trenutno_stanje = djelovi[0]
                    # drugi element vrijednosti je niz znakova od kojih je svaki znak element koji cemo pushati na stog 
                    novi_el_stoga = list(djelovi[1])
                    if novi_el_stoga[0] != '$': 
                        for el in novi_el_stoga[::-1]: 
                            # znak na vrhu stoga nakon prijelaza je krajnje lijevi
                            stog.insert(0, el)
                    #sredivanje rezultata 
                    rez.append(f"{trenutno_stanje}#")
                    if len(stog) > 0: 
                        for el in stog: 
                            rez.append(el)
                    else: 
                        rez.append('$')
                    rez.append('|')

                    if trenutno_stanje in F:
                        rez.append('1')
                        break
                    brojac = brojac + 1
                else: 
                    brojac = brojac + 100

        if trenutno_stanje not in F: 
            rez.append('0')

        print(''.join(rez))

if __name__ == "__main__":
    main()