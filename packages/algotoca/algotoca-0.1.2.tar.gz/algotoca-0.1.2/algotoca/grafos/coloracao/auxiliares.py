import igraph
import random

class FuncAux:
    '''
    Classe que contém funções auxiliares usadas pelos algoritmos gulosos.
    '''
    def conjunto_independente(lista_arestas, subconjunto_vertices):
        '''
        Função que pega a lista de arestas de um grafo e um subconjunto de seus vértices e
         verifica se esse subconjunto é conjunto independente de vértices.
        
        Parameters:
        lista_arestas (list): Lista das arestas do grafo, cada aresta
         deve ser representada por uma tupla
        subconjunto_vertices (list): Subconjunto de vértices do grafo original
         qual deseja-se saber se o subconjunto de vértices passado forma
         ou não conjunto independente

        Returns:
        resultado: Retorna True se o subconjunto é independente,
         retorna False se não for
        '''
        for vertice_a in subconjunto_vertices:
            for vertice_b in subconjunto_vertices:
                if ((vertice_a, vertice_b) or (vertice_b, vertice_a)) in lista_arestas:
                    return False
        return True

    def atualiza_grau_sat(lista_adjacencias, vertices_coloridos):
        ''' 
        Função que devolve uma lista de grau de saturação, usada durante a execução do algoritmo DSatur.

        Parameters:
        lista_arestas (list): Lista das listas de adjacências de cada vértice.
        cores_vertice (list) : Lista com os vértices que já foram coloridos.

        Returns:
        list: Devolve a lista com o grau de saturação de cada vértice.
        '''
        grau_saturacao = len(vertices_coloridos) * [0]
        for vertice in range(len(vertices_coloridos)):
            for vertice_adjacente in lista_adjacencias[vertice]:
                if vertices_coloridos[vertice_adjacente] != 0:
                    grau_saturacao[vertice] += 1
        return grau_saturacao

    def seleciona_vertice_dsatur(grau_saturacao, vertices_coloridos):
        ''' 
        Função que recebe uma lista com o grau de saturação de todos os
         vértices de um grafo e devolve o vértice com maior grau de saturação.
        Caso haja mais de um vértice com maior grau de saturação o vértice devolvido
         é aletaório entre esses vértices de maior grau.

        Parameters:
        grau_saturacao (list): Lista com os graus de saturação de cada vértice.

        Returns:
        int: Devolve inteiro que indica qual vértice ainda não colorido o com maior grau de saturação no grafo.
        '''
        vertices_n_coloridos_grau_max = []
        grau_max = 0
        for vertice in range(len(vertices_coloridos)):
            if vertices_coloridos[vertice] == 0:
                if grau_saturacao[vertice] == grau_max:
                    vertices_n_coloridos_grau_max.append(vertice)
                elif grau_saturacao[vertice] > grau_max:
                    vertices_n_coloridos_grau_max.clear()
                    vertices_n_coloridos_grau_max.append(vertice)
                    grau_max = grau_saturacao[vertice]
        vertice_escolhido = random.choice(vertices_n_coloridos_grau_max)
        return vertice_escolhido