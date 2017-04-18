from resources.peer import *
from resources.tracker import *
from pyactor.context import set_context, create_host, serve_forever
from resources.grafic import *
import plotly


#plotly.tools.set_credentials_file(username='APardo', api_key='Qmj5H4z4Ga9jTpwXFkSM')
set_context()
host = create_host()

grafic = host.spawn('grafic', Grafic)       #Actor que fara els grafics

tracker = host.spawn('tracker', Tracker)    #Creem el tracker

s = host.spawn('seed', Peer)                #Creem el peer que fara de seed
s.usuari_seed()                             #Assignat a seed

p1 = host.spawn('peer1', Peer)              #Creem els altres 5 peers
p2 = host.spawn('peer2', Peer)
p3 = host.spawn('peer3', Peer)
p4 = host.spawn('peer4', Peer)
p5 = host.spawn('peer5', Peer)

s.assignar_grafic(grafic)                   #Assignem el creador de grafics a cada actor
p1.assignar_grafic(grafic)
p2.assignar_grafic(grafic)
p3.assignar_grafic(grafic)
p4.assignar_grafic(grafic)
p5.assignar_grafic(grafic)

s.assignar_tracker(tracker)                 #Assignem el tracker a cada peer
p1.assignar_tracker(tracker)
p2.assignar_tracker(tracker)
p3.assignar_tracker(tracker)
p4.assignar_tracker(tracker)
p5.assignar_tracker(tracker)

tracker.interval_tracker()                  #Iniciem la busuqeda de peers inactius al tracker

s.inicia_gossip_push()                      #Comença a compartir
p1.inicia_gossip_push()
p2.inicia_gossip_push()
p3.inicia_gossip_push()
p4.inicia_gossip_push()
p5.inicia_gossip_push()

serve_forever()
