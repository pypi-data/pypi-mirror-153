import igraph
import random
from auxiliares import FuncAux

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
