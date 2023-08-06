import igraph
import random

class Gulosos:
    '''
    Classe que contém os algoritmos gulosos para coloração de grafos
     implementados através de funções da classe.
     Os algoritmos implementados nessa classe são o Guloso, DSatur e RLF.
    '''

    def guloso(self, grafo, ordem=None):
        '''
        Função que implementa o algoritmo guloso de coloração de grafos.
         A função devolve uma coloração para um grafo passado como argumento.
         A função também aceita uma lista de inteiros, os vértices
         são coloridos seguindo essa lista.
         Caso a lista não seja passado a ordem de coloração é aleatória.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        ordem (list): Lista ordenada dos vértices do grafo

        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da
        label "cor", para acessá-la use grafo.vs["cor"]
        '''
        if (type(ordem) != list) and (ordem is not None):
            raise Exception("A ordem dos vértices deve ser passada como uma lista")
        if (ordem is not None) and (len(ordem) != grafo.vcount()):
            raise Exception("Passe na ordem uma lista com tamanho igual à quantidade de vértices do grafo")
        if ordem is not None:
            if all(type(vertice) is int for vertice in ordem) is False:
                raise Exception("Todos os elementos da lista de ordem devem ser inteiros")
            if isinstance(grafo, igraph.Graph) is False:
                raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph")
        numero_vertices = grafo.vcount()
        lista_arestas = grafo.get_edgelist()
        cores = []
        if ordem is None:
            lista_vertices = list(range(numero_vertices))
            random.shuffle(lista_vertices)
        else:
            lista_vertices = ordem
        for vertice in lista_vertices:
            vertice_colorido = False
            for cor in cores:
                if FuncAux.conjunto_independente(lista_arestas, (cor.union({vertice}))):
                    cor.add(vertice)
                    grafo.vs[vertice]['cor'] = cores.index(cor)
                    vertice_colorido = True
                    break
            if vertice_colorido is False:
                cor = {vertice}
                cores.append(cor)
                grafo.vs[vertice]['cor'] = cores.index(cor)
        return grafo

    def dsatur(self, grafo, v_inicial=None):
        ''' 
        Função que implementa o algoritmo DSatur (Degree of Saturation)
         de coloração de grafos. 
        A função devolve uma coloração para um grafo passado
         como argumento.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        inicial (int): Inteiro que representa primero vértice a ser pintado

        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
         para acessá-la use grafo.vs["cor"]
        '''
        if isinstance(grafo, igraph.Graph) is False:
            raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph")
        if v_inicial is not None:
            if isinstance(v_inicial, int) is False:
                raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph")
        numero_vertices = grafo.vcount()
        lista_arestas = grafo.get_edgelist()
        lista_adjacencias = grafo.get_adjlist()
        vertices_coloridos = numero_vertices * [0]
        grau_saturacao = numero_vertices * [0]
        cores = []
        if v_inicial is not None:
            cor = {v_inicial}
            cores.append(cor)
            grafo.vs[v_inicial]['cor'] = cores.index(cor)
            vertices_coloridos[v_inicial] = 1
        while all(vertice == 1 for vertice in vertices_coloridos) is False:
            grau_saturacao = FuncAux.atualiza_grau_sat(lista_adjacencias, vertices_coloridos)
            vertice_maior_grau = FuncAux.seleciona_vertice_dsatur(grau_saturacao, vertices_coloridos)
            for cor in cores:
                if FuncAux.conjunto_independente(lista_arestas, cor.union({vertice_maior_grau})):
                    cor.add(vertice_maior_grau)
                    grafo.vs[vertice_maior_grau]['cor'] = cores.index(cor)
                    vertices_coloridos[vertice_maior_grau] = 1
                    break
            if vertices_coloridos[vertice_maior_grau] == 0:
                cor = {vertice_maior_grau}
                cores.append(cor)
                grafo.vs[vertice_maior_grau]['cor'] = cores.index(cor)
                vertices_coloridos[vertice_maior_grau] = 1
        return grafo
    
    def rlf(self, grafo):
        ''' 
        Função que implementa o algoritmo Recursive Largest First de coloração de grafos. 
         A função devolve uma coloração para um grafo passado como argumento.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph

        Returns:
        igraph.Graph: Retorna o mesmo grafo, porém, com adição da label "cor",
         para acessá-la use grafo.vs["cor"]
        '''
        if isinstance(grafo, igraph.Graph) is False:
            raise Exception("O grafo passado como parâmetro deve pertencer à classe igraph.Graph")
        numero_vertices = grafo.vcount()
        vertices_n_coloridos = list(range(numero_vertices))
        cores = []
        while len(vertices_n_coloridos) != 0:
            cores.append(set())
            vertices_n_coloridos_aux = vertices_n_coloridos.copy()
            while len(vertices_n_coloridos_aux) != 0:
                vertice_escolhido = random.choice(vertices_n_coloridos_aux)
                cores[-1].add(vertice_escolhido)
                vertices_n_coloridos.remove(vertice_escolhido)
                grafo.vs[vertice_escolhido]['cor'] = cores.index(cores[-1])
                vertices_n_coloridos_aux.remove(vertice_escolhido)
                vizinhos_vertice_colorido = grafo.neighbors(vertice_escolhido)
                vertices_n_coloridos_aux = [v for v in vertices_n_coloridos_aux if v not in vizinhos_vertice_colorido]
        return grafo

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