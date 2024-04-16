import sys

lines = []
for line in sys.stdin:
    lines.append(line)

def procitaj_funkcije_prijelaza():
    prijelazi = {}
    for line in lines[5:]:
        trenutno_stanje, simbol, *skup_iducih_stanja = line.strip().replace('->',',').split(',')
        skup_iducih_stanja = set(skup_iducih_stanja)
        prijelazi[(trenutno_stanje, simbol)] = skup_iducih_stanja
    return prijelazi

def epsilon_prijelazi(stanje, tranzicije):
    closure = set()
    stack = [stanje]
    while stack:
        curr = stack.pop()
        closure.add(curr)
        epsilon_next = tranzicije.get((curr, '$'), set())
        for next in epsilon_next:
            if next not in closure:
                stack.append(next)
    return closure

def nka_simulator(ulazni_niz, skup_stanja, abeceda, prihvatljiva_stanja, pocetno_stanje, fje_prijelaza):
    res = []
    ulaz = ulazni_niz.split(',')
    l = []
    trenutna_potencijalna_stanja = epsilon_prijelazi(pocetno_stanje, fje_prijelaza)
    for simbol in ulaz: 
        l = list(trenutna_potencijalna_stanja)
        l.sort()
        if '#' in l and len(l) > 1: 
            l.remove('#')
        res.append(','.join(l)) if trenutna_potencijalna_stanja else res.append('#') 
        sljedeca_stanja = set()
        for stanje in trenutna_potencijalna_stanja:
            sljedeca_stanja |= fje_prijelaza.get((stanje, simbol), set())
        nova_stanja = set()
        for stanje in sljedeca_stanja:
            nova_stanja |= epsilon_prijelazi(stanje, fje_prijelaza)
        trenutna_potencijalna_stanja = nova_stanja
        res.append('|')
    l = list(trenutna_potencijalna_stanja)
    l.sort()
    if '#' in l and len(l) > 1: 
        l.remove('#')
    res.append(','.join(l)) if trenutna_potencijalna_stanja else res.append('#')
    return res
        
    
def main():
    # 1 redak: Ulazni nizovi odvojeni znakom |. Simboli svakog pojedinog niza odvojeni su zarezom.
    ulazni_nizovi = lines[0].strip().split('|') 
    # 2. redak: Leksikografski poredan skup stanja odvojenih zarezom.
    skup_stanja = lines[1].strip().split(',')
    # 3. redak: Leksikografski poredan skup simbola abecede odvojenih zarezom
    abeceda = lines[2].strip().split(',')
    # 4. redak: Leksikografski poredan skup prihvatljivih stanja odvojenih zarezom.
    prihvatljiva_stanja = lines[3].strip().split(',')
    # 5. redak: Početno stanje.
    pocetno_stanje = lines[4].strip()
    # 6. redak i svi ostali retci: Funkcija prijelaza u formatutrenutnoStanje,simbolAbecede->skupIdućihStanja. U skupu skupIdućihStanja stanja su odvojena zarezom.
    fje_prijelaza = procitaj_funkcije_prijelaza()

    for niz in ulazni_nizovi:
        print(''.join(nka_simulator(niz, skup_stanja, abeceda, prihvatljiva_stanja, pocetno_stanje, fje_prijelaza)))

if __name__ == "__main__":
    main()





