import plotly.plotly as py
import plotly.graph_objs as go


class Grafic(object):
    _tell = ['pretty_print', 'afegir_mostra', 'generar_grafic']

    def __init__(self):
        self.dades_grafic = {}

    def pretty_print(self, aux):     #Metode per arreglar els prints
        print aux

    def afegir_mostra(self, peer_id, n_cicles, n_chunks):   #afegeix mostra (punt al grafic)
        try:
            self.dades_grafic[peer_id].x.append(n_cicles)
            self.dades_grafic[peer_id].y.append(n_chunks)
        except KeyError:                                    #Si encara no s'habia afegit el peer...
            self.dades_grafic[peer_id] = go.Scatter(
                x=[n_cicles],
                y=[n_chunks],
                name=peer_id
            )

    def generar_grafic(self, title, filename):              #Genera el grafic a mostrar
        layout = go.Layout(                                 #Opcions d'estil
            title=title,
            width=1024,
            height=576,
            xaxis=dict(
                title='N Cicles',
                autotick=False,
                tick0=0,
                dtick=1
            ),
            yaxis=dict(
                title='Chunks obtinguts',
                autotick=False,
                tick0=0,
                dtick=1
            )
        )

        fig = go.Figure(data=self.dades_grafic.values(), layout=layout) #Genera Grafic amb dades
        py.image.save_as(fig, filename=filename + '.png')               #Guarda en una imatge
