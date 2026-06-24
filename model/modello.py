from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapStates = {}

        self._bestPath = []
        self._bestPathVal = None

    # GRAPH

    def buildGraph(self, lat, lng, shape):
        self._graph.clear()
        # NODI
        self._addNodes(lat, lng, shape)
        # ARCHI
        self._addEdges(lat, lng, shape)

    def _addNodes(self, lat, lng, shape):
        self._graph.add_nodes_from(DAO.getNodes(lat, lng, shape))
        self._idMapStates = {s.id: s for s in list(self._graph.nodes)}

    def _addEdges(self, lat, lng, shape):
        self._graph.add_weighted_edges_from(DAO.getEdges(lat, lng, shape, self._idMapStates))

    # PATH

    def buildPath(self):
        self._bestPath = []
        self._bestPathVal = 0

        for n in self._graph.nodes:
            parziale = [n]
            self._ricorsione(parziale)

        return self._bestPath, self._bestPathVal

    def _ricorsione(self, parziale):

        if self._score(parziale) > self._bestPathVal:
            self._bestPath = parziale.copy()
            self._bestPathVal = self._score(parziale)

        nodo_corrente = parziale[-1]

        for vicino in self._graph.neighbors(nodo_corrente):
            if vicino.getDesita() > nodo_corrente.getDesita():
                parziale.append(vicino)
                self._ricorsione(parziale)
                parziale.pop()

    # AUX

    def _score(self, parziale):
        somma = 0
        distanza = 0
        if len(parziale) > 1:
            for i in range(1, len(parziale)):
                somma += self._graph[parziale[i-1]][parziale[i]]['weight']
                distanza += parziale[i-1].distance_HV(parziale[i])
            return somma/distanza
        return 0


    # FUNZIONI GETTER

    def getInfoGraph(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestNodes(self):
        nodesSorted = sorted(self._graph.degree(), key=lambda d: d[1],reverse=True)
        return nodesSorted[:5]

    def getBestEdges(self):
        egesSorted = sorted(self._graph.edges(data=True), key=lambda e: e[2]["weight"], reverse=True)
        return egesSorted[:5]

    @staticmethod
    def getRangeCoord():
        return DAO.getRangeCoord()

    @staticmethod
    def getShapes():
        return DAO.getShapes()

