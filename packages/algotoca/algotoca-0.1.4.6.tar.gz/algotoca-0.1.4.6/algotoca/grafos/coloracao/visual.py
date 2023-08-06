from igraph import *
import igraph
import random

class Visual:
    '''
        Classe que contém os algoritmos métodos que permitem visualização de uma coloração de grafos.
        A classe permite tanto mostrar o grafo colorido quanto exportá-lo como imagem.
    '''

    def visualizar_coloracao(grafo, cores = None):
        '''
        Função para plot de uma visualização de coloração de um grafo passado como parâmetro.

        Parameters:
        grafo (igraph.Graph): Objeto grafo do pacote igraph
        ordem (dic): Dicionário que associe cada inteiro que representa uma
                    cor na coloração do grafo (vs["cor"]) a uma string que contém
                    uma cor no formato hexadecimal

        Returns:
        plot: Plot do grafo passado colorido. Os labels dos vértices estão no formato <vértice>:<cor>.
        '''

        try:
            grafo.vs['cor']
        except:
            raise Exception("O grafo não foi colorido. A coloração do grafo deve estar representada como atributo 'cor' do objeto grafo.")
        if cores is not None:
            if isinstance(cores, dict) is False:
                raise Exception('O dicionário de cores deve ser passado considerando que a chave é o inteiro associado a cor no grafo e os valores são cores em RGB hex.')
            if len(cores.keys()) != len(list(set(grafo.vs["cor"]))):
                raise Exception('A quantidade de chaves no dicionário de cores deve ser igual a quantidade de cores distintas usadas na coloração.')
            if set(cores.keys()) != set(grafo.vs["cor"]):
                raise Exception('As cores passadas no dicionário de cores não são iguais às cores usadas na coloração.')
        if isinstance(grafo, igraph.Graph) is False:
            raise Exception('O parâmetro passado para a função deve ser um grafo.')
        if len(grafo.vs['cor']) != grafo.vcount():
            raise Exception("O tamanho do atributo 'cor' deve ser igual à quantidade de vértices.")
        if all(type(vertice) is int for vertice in grafo.vs['cor']) is False:
                raise Exception("Todos os elementos do atributo 'cor' devem ser inteiros.")
        
        if cores == None:
            cores = dict()
            for cor in set(grafo.vs["cor"]):
                cores[cor] = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])

        lista_cores = []
        for vertice_cor in grafo.vs["cor"]:
            lista_cores.append(cores[vertice_cor])

        labels_final = [str(vertice)+":"+str(cor) for vertice,cor in zip(list(range(grafo.vcount())),grafo.vs["cor"])]

        return plot(grafo,
                    vertex_size=20,
                    vertex_color=lista_cores,
                    vertex_label=labels_final,
                    edge_width=2)
