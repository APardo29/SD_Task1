from resources.peer import *
from resources.tracker import *
from pyactor.context import set_context, create_host, serve_forever
from resources.grafic import *
import plotly


# plotly.tools.set_credentials_file(username='APardo', api_key='Qmj5H4z4Ga9jTpwXFkSM')

set_context()
host = create_host()

printer = host.spawn('printer', Grafic)

# Spawn tracker and peers
tracker = host.spawn('tracker', Tracker)

s = host.spawn('seed', Peer)
s.usuari_seed()

p1 = host.spawn('peer1', Peer)
p2 = host.spawn('peer2', Peer)
p3 = host.spawn('peer3', Peer)
p4 = host.spawn('peer4', Peer)
p5 = host.spawn('peer5', Peer)

# Attach printer to peers
s.assignar_grafic(printer)
p1.assignar_grafic(printer)
p2.assignar_grafic(printer)
p3.assignar_grafic(printer)
p4.assignar_grafic(printer)
p5.assignar_grafic(printer)

# Attach tracker to peers
s.assignar_tracker(tracker)
p1.assignar_tracker(tracker)
p2.assignar_tracker(tracker)
p3.assignar_tracker(tracker)
p4.assignar_tracker(tracker)
p5.assignar_tracker(tracker)

# Start intervals
tracker.interval_tracker()

s.inicia_gossip_pull()
p1.inicia_gossip_pull()
p2.inicia_gossip_pull()
p3.inicia_gossip_pull()
p4.inicia_gossip_pull()
p5.inicia_gossip_pull()

serve_forever()