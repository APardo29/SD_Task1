from random import choice
from pyactor.context import interval, later
from pyactor.exceptions import TimeoutError


chars_frase = 0


class Peer(object):
    _tell = ['stay_alive', 'assignar_tracker',  'inicia_gossip_push',
             'inicia_gossip_pull', 'usuari_seed', 'push', 'make_push',
             'make_pull', 'assignar_grafic', 'stop_interval', 'genera_graf']
    _ask = ['get_peer_id', 'pull']
    _ref = ['assignar_tracker', 'assignar_grafic']

    def __init__(self):
        self.frase = {}

    def assignar_tracker(self, tracker):
        self.tracker = tracker

    def stay_alive(self):                               #Metode per fer announce al tracker
        self.tracker.announce("tasca1", self.proxy)

    def assignar_grafic(self, grafic):
        self.grafic = grafic

    def get_peer_id(self):
        return self.id

    def usuari_seed(self):                              #Carrega les dades del fitxer al seed
        aux = 0
        f = open("dades.txt", "r")
        for aux, char in enumerate(f.read()):
            self.frase[aux] = char
        f.close()
        global chars_frase
        chars_frase = aux + 1

    def inicia_gossip_push(self):                      #Inicia proces de gossip amb metode Push
        self.n_cicles = 0
        self.interval = interval(self.host, 5, self.proxy, 'stay_alive')        #Ens anunciem en un interval continu
        self.interval_push = interval(self.host, 1, self.proxy, 'make_push')    #Realitzem un cicle de gossip cada segon
        later(24, self.proxy, 'genera_graf', 'Metode Push', 'GraficPush')

    def push(self, chunk_id, chunk_data):
        self.frase[chunk_id] = chunk_data
        self.grafic.pretty_print(str(self.id) + str(self.frase.items()))        #Printem el progrés per consola

    def make_push(self):
        self.n_cicles = self.n_cicles + 1
        for peer in self.tracker.get_peers("tasca1"):
            try:
                data = choice(self.frase.items())                   #Fem push d'un chunk aleatori
                peer.push(data[0], data[1])
            except IndexError:
                pass
            self.grafic.pretty_print(str(self.id) + str(self.frase.items()))
            if self.id != "seed":
                self.grafic.afegir_mostra(self.id, self.n_cicles, len(self.frase.keys()))   #Cada cicle dibuixem el progrés al grafic

    def inicia_gossip_pull(self):
        self.n_cicles = 0
        self.interval = interval(self.host, 5, self.proxy, 'stay_alive')    #Interval de announce al tracker
        self.interval_pull = interval(self.host, 1, self.proxy, 'make_pull')    #Interval de gossip pull
        later(7, self.proxy, 'genera_graf', 'Metode Pull', 'GraficPull')        #Despres de 7 cicles fem grafic

    def pull(self, chunk_id):
        return self.frase[chunk_id]                     #Retorna el chunk demanat (ask)

    def make_pull(self):
        llista_caracters = set(range(chars_frase))      #llista completa de caracters a la frase
        self.n_cicles = self.n_cicles + 1

        for peer in self.tracker.get_peers("tasca1"):
            if self.id == peer.actor.id:
                continue                                #Ens saltem la iteració de un peer amb si mateix
            used = set(self.frase.keys())
            diff = list(llista_caracters - used)        #A diff tindrem les keys(chunks) que ens falten
            if not diff:
                continue                                #Si ja les tenim totes, passem a següent iteració
            pos = choice(diff)                          #Escull chunk aleatori d'entre els que ens falten
            try:
                self.frase[pos] = peer.pull(pos)        #Demanem al peer el chunk escollit
            except (TimeoutError, KeyError):
                pass
                self.grafic.pretty_print(str(self.id) + str(self.frase.items()))
            self.grafic.afegir_mostra(self.id, self.n_cicles,
                                      len(self.frase.keys()))

    def genera_graf(self, title, filename):
        self.grafic.generar_grafic(title, filename)