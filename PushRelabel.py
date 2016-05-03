# Push Relabel Algorithm
"""
    Representation of Graph in txt file as:
    s,v1,v2,v3,t <"comma separated list of vertices with s as source and t as sink">
    s,v1,12 
    s,v2,23
    v1,v2,5  
    ...so on
    <Each line represents an edge with capacity in the format src,dest,capacity >
"""
"""
Example on how to run the program.
G1 = createGraphFromFile("edgeclrs.txt")
G2 = createGraphFromFile("edgetest.txt")
G3 = createGraphFromFile("edgewiki.txt")
print "Max flow for G1:",maxflow(G1)
print "Max flow for G2:",maxflow(G2)
print "Max flow for G3:",maxflow(G3)
"""

def createGraphFromFile(filename):
    f = open(filename)
    g = graph()
    count = 0
    for row in f:
        if count == 0:
            vs = row.rstrip('\n')
            g.V = vs.split(",")
            count = count + 1
        else:
            edgeString = row.split(",")
            edge = (edgeString[0],edgeString[1])
            g.E[edge] = int(edgeString[2])
            g.Ef[edge] = int(edgeString[2])
    f.close()
    return g

class Queue:
    def __init__(self):
        self.q = list()
        
    def push(self, data):
        self.q.append(data)
        
    def front(self):
        return self.q[0]
        
    def pop(self):
        self.q.pop(0)
        
    def size(self):
        return len(self.q)

class graph:
    def __init__(self):
        self.V = list()
        self.E = dict()
        self.Ef = dict() # residual edges
        
    def Edges(self):
        edgeList = list()
        for edge in self.E.keys():
            if self.E[edge] > 0:
                edgeList.append(edge)
        return edgeList
    
    def EdgesFrom(self, src):
        edgeList = list()
        for edge in self.E.keys():
            if self.E[edge] > 0 and edge[0] == src:
                edgeList.append(edge)
        return edgeList    
    
    def ResEdgesFrom(self, src):
        edgeList = list()
        for edge in self.Ef.keys():
            if self.Ef[edge] > 0 and edge[0] == src:
                edgeList.append(edge)
        return edgeList
        
    def number_of_vertices(self):
        return len(self.V)
    
    def number_of_edges(self):
        return len(self.E)

h = dict() # height
e = dict() # excess
f = dict() # flow



def initializeExcess(G):
    for vertex in G.V:
        e[vertex] = 0
        
def initializePreflow(G, startVertex):
    # set height of each to 0
    for vertex in G.V:
        h[vertex] = 0
    # set flow through each edge to 0
    for edge in G.Ef.keys():
        f[edge] = 0
    # set the height of the start to number_of_vertices
    h[startVertex] = G.number_of_vertices()
    # Initialize the residual capacity and Excess
    initializeExcess(G)
    # for each edge from startVertex
    for s,v in G.ResEdgesFrom(startVertex):
        # Flow
        f[(startVertex,v)] = G.E[(startVertex,v)]
        f[(v,startVertex)] = -G.E[(startVertex,v)]
        # Excess
        e[v] = G.E[(startVertex,v)]
        e[startVertex] = e[startVertex] - G.E[(startVertex,v)]
        # Residual Capacity
        G.Ef[(startVertex,v)] = G.E[(startVertex,v)] - f[(startVertex,v)]
        G.Ef[(v,startVertex)] = -f[(v,startVertex)]
        
# Push flow from u to v.
def push(G, u , v):
    temp = min(e[u],G.Ef[(u,v)])
    # Flow from u to v is existing + min(excess at u, residual capacity of edge uv) 
    f[(u,v)] = f[(u,v)] + temp
    f[(v,u)] = -f[(u,v)]
    # Excess decreases at u
    e[u] = e[u] - temp 
    # Excess inccreases at v
    e[v] = e[v] + temp
    if (u,v) in G.E.keys():
        G.Ef[(u,v)] = G.E[(u,v)] - f[(u,v)]
        G.Ef[(v,u)] = -f[(v,u)]
    else:
        G.Ef[(u,v)] = - f[(u,v)]
        G.Ef[(v,u)] = G.E[(v,u)] + f[(v,u)]
    
def addBackEdges(G):
    # adding back edges with cf(edge) = 0
    for edge in G.Ef.keys():
        src,dest = edge
        G.Ef[(dest,src)] = 0

def maxflow(G):
    addBackEdges(G)
    initializePreflow(G, "s")
    q = Queue()
    # Active Vertices
    av = dict()
    for vertex in G.V:
        av[vertex] = 0
    for u,v in G.EdgesFrom("s"):
        if v != "t":
            q.push(v)
            av[v] = 1
    while q.size() != 0 :
        u = q.front()
        m = -1 # temp variable used to find the min height among neighbors
        # For each edge from u to v in Residual Network
        for u,v in G.ResEdgesFrom(u):
            if e[u] > 0:
                if G.Ef[(u,v)] > 0:
                    # Push iff height contraint is satisfied
                    #if h[u] > h[v]:
                    if h[u] == h[v] + 1:
                        push(G, u, v)
                        if av[v] == 0 and v != "s" and v!= "t":
                            av[v] = 1
                            q.push(v)
                    elif m == -1:
                        m = h[v]
                    else:
                        m = min(m,h[v])
        # Relabel
        if e[u] != 0:
            h[u] = 1 + m
        else:
            av[u] = 0
            q.pop()
    return e["t"]
    