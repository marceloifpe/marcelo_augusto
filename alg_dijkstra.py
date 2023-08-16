#Atividade da disciplina Matemática Discreta II: Implemente o algoritmo de Dijkstra em python (ou 
# outra linguagem de sua preferência) e execute o mesmo usando o grafo do exercício 14 da lista 4 
# (Grafos). O algoritmo de Dijkstra deve retornar a lista das menores distâncias a partir de um 
# vértice de origem e uma lista de predecessores para cada vértice.Você deve também implementar 
# uma função que retorna o melhor caminho dados os vértices de origem e chegada.
#Aluno: Marcelo Augusto de Barros Araújo.
#Professor:Marcos Maia.

import networkx as nx
import matplotlib.pyplot as plt

def algoritmo_de_dijkstra(grafo, fonte):
    #definindo os tipos de dados que iram percorrer a lista
    distancias = {node: float('inf') for node in grafo}
    antecessores = {node: 'und' for node in grafo}
    
    # Listando os vértices do grafo
    Q = [node for node in grafo]
    
    distancias[fonte] = 0
    antecessores[fonte] = fonte
    
    while len(Q) > 0:
        e = float('inf')
        vertice_atual = None  # Armazenar o vértice atual escolhido
        for node in Q:
            if distancias[node] < e:
                e = distancias[node]
                vertice_atual = node
        if vertice_atual is None:
            break  # Sai do loop se nenhum vértice for escolhido
        
        Q.remove(vertice_atual)  # Remove o vértice escolhido da lista
        
        for vizinho, peso in grafo[vertice_atual].items():
            alt = distancias[vertice_atual] + peso
            if alt < distancias[vizinho]:
                distancias[vizinho] = alt
                antecessores[vizinho] = vertice_atual
    
    return distancias, antecessores

grafo = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 1, 'D': 3, 'E': 5},
    'C': {'A': 4, 'B': 1, 'D': 2, 'E': 3},
    'D': {'B': 3, 'C': 2, 'E': 2},
    'E': {'B': 5, 'C': 3, 'D': 2}
}

# Executando a função
fonte = 'A'
dist, prev = algoritmo_de_dijkstra(grafo, fonte)
print("Lista da distância entre cada ponto do grafo:\n=>",dist)
print("-------------------------------------------")
print("Lista de predecessores:\n=>",prev)

#Função/método que define  melhor caminho entre os dois Vértice, baseado no algoritmo
def esc_camin(fonte, des_v):
    m_camin = []
    m_camin.append(des_v)
    antecessor = prev[des_v]
    m_camin.append(antecessor)
    while antecessor != fonte:
        antecessor = prev[antecessor]
        m_camin.append(antecessor)
    
    return sorted(m_camin, reverse=True)

T = esc_camin(fonte, 'E')
print('-------------------------------------------')
print("Melhor caminho gerado:\n=>",T)

# Geração do grafo
print('Grafo-(Utilizando Algoritmo de dijkstra )')
G = nx.Graph(grafo)

for node in grafo:
    for vizinho, peso in grafo[node].items():
        G.add_edge(node, vizinho, weight=peso)

pos = nx.circular_layout(G)

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels)

# Destacar as arestas do melhor caminho
best_path_edges = [(T[i], T[i+1]) for i in range(len(T) - 1)]
nx.draw_networkx_edges(G, pos, edgelist=best_path_edges, edge_color='b', width=2)

plt.show()
