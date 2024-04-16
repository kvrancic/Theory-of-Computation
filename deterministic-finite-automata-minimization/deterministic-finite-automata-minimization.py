import sys

lines = []
for line in sys.stdin:
    lines.append(line)

def procitaj_funkcije_prijelaza():
    prijelazi = {}
    for line in lines[4:]:
        trenutno_stanje, simbol, iduce_stanje = line.strip().replace('->',',').split(',')
        prijelazi[(trenutno_stanje, simbol)] = iduce_stanje
    return prijelazi

# u nekim megarijetkim slucajevima lista istovjetni ne daje konstantan rez jer python nepredvidivo upisuje podatke -> rezultira rijetkim 19/20 na testovima, ovako popravljeno 
def edit_list(list_of_lists):
    list_of_lists.sort(key=len)

    contained_lists = set()

    for i, sublist in enumerate(list_of_lists):
        for superlist in list_of_lists[i+1:]:
            if set(sublist).issubset(set(superlist)):
                contained_lists.add(tuple(sublist))

    new_list_of_lists = [list(sublist) for sublist in list_of_lists if tuple(sublist) not in contained_lists]
    return new_list_of_lists

def pronadi_nedohvatljiva_stanja(pocetno_stanje, skup_stanja, prijelazi, abeceda):
    # inicijaliziraj skup dohvatljivih stanja s pocetnim stanjem
    dohvatljiva_stanja = set([pocetno_stanje])
    
    # prođi kroz sve dohvatljive stanja i proširi skup dohvatljivih stanja novim stanjima
    # koja se mogu dohvatiti preko prijelaza iz trenutnog stanja
    while True:
        broj_dohvatljivih_stanja = len(dohvatljiva_stanja)
        
        for stanje in dohvatljiva_stanja.copy():
            for simbol in abeceda:
                if (stanje, simbol) in prijelazi:
                    sljedece_stanje = prijelazi[(stanje, simbol)]
                    dohvatljiva_stanja.add(sljedece_stanje)
        
        if len(dohvatljiva_stanja) == broj_dohvatljivih_stanja:
            break
    
    # skup nedohvatljivih stanja je komplement skupa dohvatljivih stanja u odnosu na skup svih stanja
    nedohvatljiva_stanja = set(skup_stanja) - dohvatljiva_stanja
    
    return sorted(nedohvatljiva_stanja)


def konstruiraj_automat_bez_nedohvatljivih_stanja(pocetno_stanje, skup_stanja, prijelazi, abeceda, zavrsna_stanja):
    #print("usao konstruiraj_nedohvatljiva")
    #if not isinstance(prijelazi, dict):
        #print("Funkcija prijelaza nije tipa dict!")
    # pronađi nedohvatljiva stanja
    nedohvatljiva_stanja = pronadi_nedohvatljiva_stanja(pocetno_stanje, skup_stanja, prijelazi, abeceda)
    
    # izbaci nedohvatljiva stanja iz skupa stanja
    nova_skup_stanja = set(skup_stanja) - set(nedohvatljiva_stanja)
    
    novo_pocetno_stanje = pocetno_stanje
    
    # ažuriraj završna stanja ako su nedohvatljiva
    nova_zavrsna_stanja = set()
    for stanje in nova_skup_stanja:
        if stanje not in nedohvatljiva_stanja and stanje in zavrsna_stanja:
            nova_zavrsna_stanja.add(stanje)
    
    # ažuriraj funkciju prijelaza tako da izbacuje prijelaze koji vode u nedohvatljiva stanja
    nova_funkcija_prijelaza = {}
    for prijelaz, sljedece_stanje in prijelazi.items():
        if prijelaz[0] not in nedohvatljiva_stanja and sljedece_stanje not in nedohvatljiva_stanja:
            nova_funkcija_prijelaza[prijelaz] = sljedece_stanje
    
    return novo_pocetno_stanje, sorted(nova_skup_stanja), nova_zavrsna_stanja, nova_funkcija_prijelaza


def minimize_dfa(states, symbols, acceptable_states, starting_state, transitions):
    #if not isinstance(transitions, dict):
        #print("Funkcija prijelaza nije tipa dict!")
    initial_pairs = [(s1, s2) for s1 in states for s2 in states if s1 != s2]
    state_pairs = []
    for tup in initial_pairs:
        sorted_tup = tuple(sorted(tup))
        if sorted_tup not in state_pairs:
            state_pairs.append(sorted_tup)
    #print("potenicjalni parovi")
    #print(state_pairs)
    
    
    # MAZANJE
    marked_pairs = set()
    initial_pairs = {(s1, s2) for s1 in acceptable_states for s2 in states if s2 not in acceptable_states}
    for tup in initial_pairs:
        sorted_tup = tuple(sorted(tup))
        if sorted_tup not in marked_pairs:
            marked_pairs.add(sorted_tup)
    #print("inicijalni parovi")
    marked_pairs = sorted(marked_pairs)
    #print(marked_pairs)
    #print("gotovi parovi")
    #print(transitions[('p5','c')])
    #print(transitions[('p6','c')])
    
    # VRTI GA VRTI GA VRTI MILE VRTI GA
    while True:
        newly_marked_pairs = set()
        for pair in state_pairs:
            for symbol in symbols:
                next_state1 = transitions[(pair[0], symbol)]
                next_state2 = transitions[(pair[1], symbol)]
                pair = tuple(sorted(pair))
                if next_state1 is not None and next_state2 is not None and (((next_state1, next_state2) in marked_pairs) or ((next_state2, next_state1) in marked_pairs)) and (pair[0],pair[1]) not in marked_pairs:
                    newly_marked_pairs.add(pair)
                    marked_pairs.append(pair)
        marked_pairs = sorted(marked_pairs)
        #print("novi parovi")
        #print(newly_marked_pairs)
        if not newly_marked_pairs:
            break
        #marked_pairs |= newly_marked_pairs
    #print("gotovo - markirani")
    #print(sorted(marked_pairs))
    
    
    
    #print("nemarkirani")
    unmarked_pairs = set(sorted(set(state_pairs) - set(marked_pairs)))
    #print(unmarked_pairs)
    #print("dalje")
    unmarked_pairs = list(unmarked_pairs)

    istovjetni = [] # lista lista 
    #MIJENJALICA
    for par in unmarked_pairs: 
        par = sorted(par)
        if len(istovjetni) == 0:
            istovjetni.append(par)
        flag = 0
        for i in range(len(istovjetni)):
            #if not isinstance(istovjetni, list):
                #print("bok")
            if par[0] in istovjetni[i] and par[1] not in istovjetni[i]:
                istovjetni[i].append(par[1])
                flag = 1
                break
            if par[1] in istovjetni[i] and par[0] not in istovjetni[i]:
                istovjetni[i].append(par[0])
                flag = 1
                break 
            if par[0] in istovjetni[i] and par[1] in istovjetni[i]:
                flag = 1
                break 
        if flag == 0:
            istovjetni.append(par)

    istovjetni = edit_list(istovjetni)
    istovjetni = sorted(istovjetni)
    for i in range(len(istovjetni)):
        istovjetni[i] = sorted(istovjetni[i]) # BITNO: u istovjetnima je sve sortirano i onda uvijek uzimamo prvi element 
    #print(istovjetni)

    #novo pocetno
    novo_pocetno = starting_state
    for i in range(len(istovjetni)):
        if starting_state in istovjetni[i]:
            if istovjetni[i].index(starting_state) != 0:
                novo_pocetno = istovjetni[i][0]
                break

    #nova stanja 
    nova_stanja = set()
    flag = 0
    for stanje in states: 
        for i in range(len(istovjetni)):
            if stanje in istovjetni[i]: 
                flag = 1
                nova_stanja.add(istovjetni[i][0])
                break
        if flag == 0: 
            nova_stanja.add(stanje)
        flag = 0
    #print("stanja")
    #print(sorted(nova_stanja))
    ispis = ','.join(sorted(nova_stanja))
    print(ispis)
    ispis = ','.join(sorted(symbols))
    print(ispis)

    #nova prihvatljiva
    nova_prihvatljiva = set()
    for stanje in acceptable_states:
        if stanje in nova_stanja: 
            nova_prihvatljiva.add(stanje)
    #print("prihvatljiva")
    #print(nova_prihvatljiva)
    ispis = ','.join(sorted(nova_prihvatljiva))
    print(ispis)
    print(novo_pocetno)

    #novi prijelazi 
    novi_prijelazi = dict()
    for key, value in transitions.items(): 
        key = list(key);
        for i in range(len(istovjetni)):
            if key[0] in istovjetni[i]:
                key[0] = istovjetni[i][0]
            if value in istovjetni[i]: 
                value = istovjetni[i][0]
        novi_prijelazi[(key[0], key[1])] = value

    for keys, value in novi_prijelazi.items():
        print('{},{}->{}'.format(keys[0], keys[1], value))
    
    #print("prijelazi")
    #print(novi_prijelazi)




def main():
    # 1. redak: Leksikografski poredan skup stanja odvojenih zarezom.
    skup_stanja = lines[0].strip().split(',')
    # 2. redak: Leksikografski poredan skup simbola abecede odvojenih zarezom
    abeceda = lines[1].strip().split(',')
    # 3. redak: Leksikografski poredan skup prihvatljivih stanja odvojenih zarezom.
    prihvatljiva_stanja = lines[2].strip().split(',')
    # 4. redak: Početno stanje.
    pocetno_stanje = lines[3].strip()
    # 5. redak i svi ostali retci: Funkcija prijelaza u formatutrenutnoStanje,simbolAbecede->skupIdućihStanja. U skupu skupIdućihStanja stanja su odvojena zarezom.
    fje_prijelaza = {}
    fje_prijelaza = procitaj_funkcije_prijelaza()

    pocetno_stanje, skup_stanja, prihvatljiva_stanja, fje_prijelaza = konstruiraj_automat_bez_nedohvatljivih_stanja(pocetno_stanje, skup_stanja, fje_prijelaza, abeceda, prihvatljiva_stanja)

    minimize_dfa(skup_stanja, abeceda, prihvatljiva_stanja, pocetno_stanje, fje_prijelaza)



    

if __name__ == "__main__":
    main()