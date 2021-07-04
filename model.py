#konstante:
roza = "1"
oranzna = "2"
rumena = "3"
zelena = "4"
modra = "5"
vijolicna = "6"




class Igra:
    def __init__(self, tip_igre, igralec1, igralec2):
        self.tip_igre = tip_igre
        self.st_vrstic = tip_igre + 2
        self.st_stolpcev = tip_igre + 3
        self.igralec1 = igralec1
        self.igralec2 = igralec2
        self.na_potezi = 1
        self.grid = []


    def prazen_grid(self):
        grid_prazen = []

        for i in range(self.st_vrstic):
            vrstica = []
            for j in range(self.st_stolpcev):
                    vrstica.append(0)
            grid_prazen.append(vrstica)

        self.grid = grid_prazen

    

    def poteza(self, stolpec, st_igralca):
        if st_igralca != self.na_potezi:
            return "igralec ni na potezi"

        if self.na_potezi == 1:
            barva_igralca = self.igralec1.barva

        else:
            barva_igralca = self.igralec2.barva
        
        for i in reversed(range(self.st_vrstic)):
            if self.grid[i][stolpec] == 0:
                self.grid[i][stolpec] = int(barva_igralca) #nastima barvo zetona na pravo barvo
                break
            
        if st_igralca == 1:
            self.na_potezi = 2

        else:
            self.na_potezi = 1
        #TODO: ugotovi kaj nrdit kadar je poln stolpec

    def zmaga(self):
        return Igra.zmaga_staticna(self.igralec1, self.igralec2, self.tip_igre, self.grid)
    
    # vrne zmagovalca, ce je zmagal
    # vrne None, ce ni noben zmagal

    @staticmethod
    def zmaga_staticna(igralec1, igralec2, tip_igre, grid):
        igralca = [igralec1, igralec2]
        st_vrstic = len(grid)
        st_stolpcev = len(grid[0])

        # horizontalno
        for vrstica in range(st_vrstic):
            trenutna_barva = 0
            zaporedne_pojavitve = 0
            zacetne_koordinate = (0, 0)
            koncne_koordinate = (0, 0)

            for stolpec in range(st_stolpcev):
                trenutna_celica = grid[vrstica][stolpec] 
                if trenutna_celica == trenutna_barva:
                    zaporedne_pojavitve += 1
                    if zaporedne_pojavitve >= tip_igre and trenutna_barva != 0:
                        koncne_koordinate = (vrstica, stolpec)
                        return {"z": zacetne_koordinate, "k": koncne_koordinate, "zmagovalec" : igralca[trenutna_barva - 1]}

                else:
                    trenutna_barva = trenutna_celica
                    zacetne_koordinate = (vrstica, stolpec)
                    zaporedne_pojavitve = 1

        # vertikalno

        for stolpec in range(st_stolpcev):
            trenutna_barva = 0
            zaporedne_pojavitve = 0
            zacetne_koordinate = (0, 0)
            koncne_koordinate = (0, 0)

            for vrstica in range(st_vrstic):
                trenutna_celica = grid[vrstica][stolpec] 
                if trenutna_celica == trenutna_barva:
                    zaporedne_pojavitve += 1
                    if zaporedne_pojavitve >= tip_igre and trenutna_barva != 0:
                        koncne_koordinate = (vrstica, stolpec)
                        return {"z": zacetne_koordinate, "k": koncne_koordinate, "zmagovalec" : igralca[trenutna_barva - 1]}

                else:
                    trenutna_barva = trenutna_celica
                    zacetne_koordinate = (vrstica, stolpec)
                    zaporedne_pojavitve = 1

        # diagonala gor-levo --> spodaj-desno
        

        for zacetni_stolpec in range(st_stolpcev - 1 - (tip_igre - 1), -st_stolpcev + (tip_igre - 1), -1):  # zacetnih n - 1 diagonal ni treba preverjati, ker je premalo mest za zmago, ce je tip igre = n
            trenutna_barva = 0
            zaporedne_pojavitve = 0
            zacetne_koordinate = (0, 0)
            koncne_koordinate = (0, 0)

            for zamik in range(st_vrstic):
                if 0 <= zamik < st_vrstic and 0 <= zacetni_stolpec + zamik < st_stolpcev:
                    trenutna_celica = grid[zamik][zacetni_stolpec + zamik] 

                    if trenutna_celica == trenutna_barva:
                        zaporedne_pojavitve += 1
                        if zaporedne_pojavitve >= tip_igre and trenutna_barva != 0:
                            koncne_koordinate = (zamik, zacetni_stolpec + zamik)
                            return {"z": zacetne_koordinate, "k": koncne_koordinate, "zmagovalec" : igralca[trenutna_barva - 1]}

                    else:
                        zacetne_koordinate = (zamik, zacetni_stolpec + zamik)
                        trenutna_barva = trenutna_celica
                        zaporedne_pojavitve = 1

        # diagonala gor-desno --> spodaj-levo
        

        for zacetni_stolpec in range(tip_igre - 1, 2 * st_stolpcev - 1, 1):
            trenutna_barva = 0
            zaporedne_pojavitve = 0
            zacetne_koordinate = (0, 0)
            koncne_koordinate = (0, 0)

            for zamik in range(st_vrstic):
                if 0 <= zamik < st_vrstic and 0 <= zacetni_stolpec - zamik < st_stolpcev:
                    trenutna_celica = grid[zamik][zacetni_stolpec - zamik] 

                    if trenutna_celica == trenutna_barva:
                        zaporedne_pojavitve += 1
                        if zaporedne_pojavitve >= tip_igre and trenutna_barva != 0:
                            koncne_koordinate = (zamik, zacetni_stolpec - zamik)
                            return {"z": zacetne_koordinate, "k": koncne_koordinate, "zmagovalec" : igralca[trenutna_barva - 1]}

                    else:
                        zacetne_koordinate = (zamik, zacetni_stolpec - zamik)
                        trenutna_barva = trenutna_celica
                        zaporedne_pojavitve = 1

        return None







    


class Upravljalec_iger:
    def __init__(self):
        self.igre = {}
        self.max_id = 0

    def prost_id_igre(self):
        self.max_id += 1
        return self.max_id

    def nova_igra(self, tip_igre, igralec1, igralec2):
        nov_id = self.prost_id_igre()
        self.igre[nov_id] = Igra(tip_igre, igralec1, igralec2)
        self.igre[nov_id].prazen_grid()
    
        return nov_id

    def izbrisi_igro(self, id_igre):
        del self.igre[id_igre]


class Igralec:
    def __init__(self, barva):
        self.barva = barva


    



