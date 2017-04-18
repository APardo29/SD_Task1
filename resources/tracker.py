from datetime import datetime
from pyactor.context import interval
import random


class Tracker(object):
    _tell = ['announce', 'interval_tracker', 'comprova_inactius']
    _ask = ['get_peers']
    _ref = ['announce', 'get_peers']
    temps_max = 10

    def __init__(self):
        self.llista_peers = {}
        self.temps_announce = {}

    def announce(self, torrent_hash, peer_ref):
        trobat = False
        if torrent_hash in self.llista_peers:                       #Busquem parella has i peer a la llista
            for item in self.llista_peers.values():
                if peer_ref in item:
                    self.temps_announce[peer_ref] = datetime.now()  #Si els trobem, actualitzem amb ultim announce
                    trobat = True
                    break
            if not trobat:
                self.llista_peers[torrent_hash].append(peer_ref)    #Si no trobem el peer, l'afegim al hash corresponent
                self.temps_announce[peer_ref] = datetime.now()
        else:
            self.llista_peers[torrent_hash] = [peer_ref]            #Si no trobem el hash, l'afegim amb el nou peer
            self.temps_announce[peer_ref] = datetime.now()

    def get_peers(self, torrent_hash):
        if len(self.llista_peers[torrent_hash]) >= 3:               #Retornem 3 peers aleatoris
            return random.sample(self.llista_peers[torrent_hash], 3)
        else:                                                           #Si no hi ha 3, retornem els que tinguem
            return random.sample(self.llista_peers[torrent_hash], len(self.llista_peers[torrent_hash]))

    def interval_tracker(self):                                         #Comprovem la llista de peers cada segon
        self.interval_inactius = interval(self.host, 1, self.proxy, 'comprova_inactius')

    def comprova_inactius(self):
        inactius = []
        for item in self.llista_peers.values():
            for peer_ref in item:
                last_announce = self.temps_announce.get(peer_ref)
                time_dif = datetime.now() - last_announce
                if time_dif.total_seconds() > self.temps_max:   #Si superen el temps_max sense announce, els eliminem
                    inactius.append(peer_ref)
        for peer_ref in inactius:
            for torrent_hash in self.llista_peers:
                self.llista_peers[torrent_hash].remove(peer_ref)
            self.temps_announce.pop(peer_ref, None)