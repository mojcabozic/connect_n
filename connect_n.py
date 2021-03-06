import bottle
import model
SECRET = "secret123"

upravljalec_iger = model.Upravljalec_iger()


@bottle.get("/")
def index():
    return bottle.template("zacetna-stran.html")


@bottle.post("/")
def index_post():

    return bottle.redirect("/")


@bottle.post("/nova-igra-<tip_igre_str>/")
def nova_igra(tip_igre_str):
    tip_igre = int(tip_igre_str)

    if tip_igre not in {3, 4, 5}:
        return bottle.abort(400, "napacen tip igre " + tip_igre_str)

    igralec1 = model.Igralec(model.roza)
    igralec2 = model.Igralec(model.modra)
    id_igre = upravljalec_iger.nova_igra(tip_igre, igralec1, igralec2)
    bottle.response.set_cookie('idigre', id_igre, secret=SECRET, path='/')

    return bottle.redirect('/nastavi-ime/1/')


@bottle.get("/nastavi-ime/<id_igralec>/")
def nastavi_ime(id_igralec):
    return bottle.template("nastavi-ime.html", id_igralec=id_igralec)


@bottle.post("/nastavi-ime/<id_igralec>/")
def nastavi_ime_post(id_igralec):
    id_igre = bottle.request.get_cookie("idigre", secret=SECRET)
    igra = upravljalec_iger.igre[id_igre]

    ime = bottle.request.forms.ime_igralca
    print(ime)

    if int(id_igralec) == 1:
        igralec = igra.igralec1

    else:
        igralec = igra.igralec2

    igralec.ime = ime

    if int(id_igralec) == 1:
        return bottle.redirect("/izbira-barve/1/")

    else:
        return bottle.redirect("/izbira-barve/2/")


@bottle.get("/izbira-barve/<id_igralec>/")  # izbira barve za vsakega igralca
def izberi_barvo(id_igralec):
    id_igre = bottle.request.get_cookie("idigre", secret=SECRET)
    igra = upravljalec_iger.igre[id_igre]

    return bottle.template("izbira-barve.html", id_igralec=id_igralec, skrij_barvo=igra.igralec1.barva if id_igralec == "2" else None)


@bottle.post("/izbira-barve/<id_igralec>/<barva>")
def izberi_barvo_post(id_igralec, barva):    # nastavi barvo
    id_igre = bottle.request.get_cookie("idigre", secret=SECRET)
    igra = upravljalec_iger.igre[id_igre]

    if int(id_igralec) == 1:
        igralec = igra.igralec1

    else:
        igralec = igra.igralec2

    igralec.barva = barva

    if int(id_igralec) == 1:
        return bottle.redirect("/nastavi-ime/2/")

    else:
        return bottle.redirect("/igra/")


@bottle.get("/igra/")
def serviraj_igro():
    id_igre = bottle.request.get_cookie("idigre", secret=SECRET)
    igra = upravljalec_iger.igre[id_igre]

    return bottle.template("igra.html", igra=igra)


@bottle.post("/stolpec<stolpec>/<st_igralca>")
def poteza(stolpec, st_igralca):
    id_igre = bottle.request.get_cookie("idigre", secret=SECRET)
    igra = upravljalec_iger.igre[id_igre]
    igra.poteza(int(stolpec), int(st_igralca))

    zmaga = igra.zmaga()
    if zmaga != None:
        igra.zmagovalec = zmaga["zmagovalec"]
        return bottle.redirect("/zmaga/")

    elif igra.neodlocena_igra() == True:
        return bottle.redirect("/zmaga/")

    else:
        return bottle.redirect("/igra/")


@bottle.get("/zmaga/")
def konec_igre():
    id_igre = bottle.request.get_cookie("idigre", secret=SECRET)
    igra = upravljalec_iger.igre[id_igre]
    zmaga = igra.zmaga()

    if zmaga != None:
        zmagovalec = zmaga["zmagovalec"]
        ime_zmagovalca = zmagovalec.ime

    else:
        ime_zmagovalca = ""

    upravljalec_iger.izbrisi_igro(id_igre)

    return bottle.template("igra-zmaga.html", igra=igra, ime_zmagovalca=ime_zmagovalca)


@bottle.get("/img/<picture>")
def serve_pictures(picture):

    return bottle.static_file(picture, root='img')


@bottle.get("/css/<file_name>")
def static_css(file_name):

    return bottle.static_file(file_name, root="css")


bottle.run(reloader=True, debug=True, port=8080)
