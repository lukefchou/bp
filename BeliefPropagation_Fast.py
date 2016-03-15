import networkx as nx
import math
from math import e

def convergeGraph(g, u, threshold):
    g1 = nx.DiGraph(g).copy()
    total_max = 0
    while(True):
        total_pre = 0.0
        total_post = 0.0
        for (x, y) in g1.edges():
            total_pre = total_pre + g[x][y]['weight']
            numerator = 0.0
            denominator = 0.0
            for m in g.neighbors(x):
                if(m != y):
                    numerator = numerator + g[m][x]['weight']
                    denominator = denominator + g[m][x]['weight'] * g[m][x]['weight']

            denominator = 1 + 0.25 * u * u * (numerator * numerator - denominator)
            numerator = u * numerator
            g1[x][y]['weight'] = numerator / denominator
            total_post = total_post + g1[x][y]['weight']

        #print(str(total_post) + " : " + str(total_pre))
        if total_post > total_max:
            total_max = total_post
        if(abs(total_post - total_pre)  < threshold)or (abs(total_post - total_pre)/abs(total_max)  < threshold):
            return g1

        g = g1.copy()

def initGraph(g):
    # Remove nodes with degree equals to 0 or 1
    c = 0
    while 1 :
        c = 0
        for x in g.nodes():
            if g.degree(x) < 2 :
                g.remove_node(x)
                c = c + 1
        if c == 0 :
            break 
    
    g = nx.DiGraph (g)
    for (x, y) in g.edges():
        g[x][y]['weight'] = 0.1

    return g

def estimateCycle(g, u):
    l = 0.0
    ee = 0.0
    for (x, y) in g.edges():
        indice = u * g[x][y]['weight'] * g[y][x]['weight'] 
        l = l + indice/ (1 + indice)
        ee = ee + math.log(1 + indice, e)

    ee = ee / len(g.nodes())

    nodes = 0.0
    for i in g.nodes():
        node = 0.0
        node_sub = 0.0
        for m in g.neighbors(i):
            node = node + g[m][i]['weight']
            node_sub = node_sub + g[m][i]['weight'] * g[m][i]['weight']

        node = 1 + 0.25 * u * u * (node * node - node_sub)
        nodes = nodes + math.log(node, e)

    nodes = nodes / len(g.nodes())
    cycles = nodes - ee - l * math.log(u, e) / len(g.nodes())
    cycles = cycles * len(g.nodes())

    return l, cycles

def print_cycle_stat(stat, path=''):
    strStat = ''
    for key, value in stat.items():
        #if key > 2:
        #    value = value / 2
            
        strStat += str(value) + "\n"
    print strStat

    if path != '':
        fh = open(path, 'w')
        fh.write(strStat)
        fh.close()

path = 'D:\\!Experiments\\!exp_polygon\\arvix\\arvix.edges'
G = nx.read_edgelist(path)
v1 = len(G.nodes ())
e1 = len(G.edges())
print("ori graph with vertices: " + str(v1) + ", edges: " + str(e1))
#G = nx.read_gml(path)
G = initGraph(G)
v2 = len(G.nodes ())
e2 = len(G.edges())
print("leaf nodes removed graph with vertices: " + str(v2) + ", edges: " + str(e2))

thr = 0.0001
u = 0.022
sep = 0.00001
sep_sub = 0.01
cycles = dict()
l_old = 0
first = True
while(True):
    g = G.copy()
    G = convergeGraph(G, u, thr)
    l, c = estimateCycle(G, u)
    s = str(u) + "\t" + str(l) + "\t" + str(c)
    cycles[u] = s
    print(s)

    #if(first and l > 2):
    #    if (u > 0.02):
    #        u = u - 0.01
    #    else:
    #        u = u / 2
    #    continue

    #first = False
    #if abs(l - l_old) < 0.1 :
    #    u = u * 1.05
    #else:
    u = u + sep

    l_old = l

    G = g.copy()

    if(u >= 0.023):
        break

    if(l >= len(G.nodes())):
        break

print_cycle_stat(cycles, path + "_" + str(v1)+"_" + str(e1) + "_" + str(v2)+"_" + str(e2) + ".apx.poly")
print("Finished")
