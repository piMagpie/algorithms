#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

class GrafoAbstracto(metaclass=ABCMeta):
    """Clase abstracta para trabajar con Grafos."""

    def __init__(self, dirigido = False):
        """Constructor. El argumento indica si el grafo es dirigido"""
        self._dirigido = dirigido

    def dirigido(self):
        """Indica si el grafo es o no dirigido"""
        return self._dirigido

    @abstractmethod
    def __len__( self ):
        """Número de nodos del grafo."""

    @abstractmethod
    def num_arcos(self):
        """Devuelve el número de arcos"""

    @abstractmethod       
    def inserta(self, nodo, destino = None, etiqueta = 1):
        """
        Inserta un nodo al grafo (si destino es None) o un arco.
        Si el arco ya existía se actualiza su etiqueta.
        Si alguno de los nodos del arco no está en el grafo, se inserta.
        Se supone que None no es una etiqueta válida.
        """

    @abstractmethod       
    def __contains__(self, nodo):
        """Indica si el nodo está en el grafo."""      
        
    @abstractmethod        
    def __getitem__(self, arco):
        """Dado un arco (un par de nodos) devuelve la etiqueta si el arco está
        en el grafo, en caso contrario devuelve None"""

    @abstractmethod        
    def __iter__(self):
        """Iterador sobre los nodos del grafo"""

    @abstractmethod
    def vecinos(self, origen):
        """Devuelve un iterable de los pares (destino,etiqueta) para un nodo 
        origen dado"""
##################################################################################

'''
@Author: DIEGO SANZ VILLAFRUELA
@Date: 22-02-2017

Práctica sobre la implementación de grafos mediante
matriz de adyacencia y listas de adyacencia.

    '''

class GrafoMatriz(GrafoAbstracto):
    """
    Implementación del tipo Grafo utilizando una matriz de adyacencia para 
    almacenar la información de los arcos.
    La matriz podría ser una lista de lista.
    """
    
    
    def __init__(self,dirigido=False):
        GrafoAbstracto.__init__(self,dirigido)
        # numero de nodos
        self._elements = 0
        # numero de arcos
        self._arrows = 0
        # indice donde añadimos un nodo
        self._index = -1
        # matriz para almacenar las etiquetas
        self._matrix = []
        
        # mapa para almacenar los nodos y su index en la matriz.
        # mejorando la eficiencia
        self._indexMap = {}
        self._current = None
    
    def getFirstNode(self):
    	iterador = iter(self)
    	return next(iterador)

    """Número de nodos del grafo."""
    def __len__( self ):
        return len(self._indexMap)
    
    """Devuelve el número de arcos"""
    def num_arcos( self ):
        return self._arrows
    
    """Metodo privado que añade casillas vacias de los nuevos nodos
        en los elementos antiguos de la matriz
    """
    def _addNodeInColumn(self,num):
        for fila in self._matrix:
            fila.append(None)
            if num == 2:
                fila.append(None)
    
    """ Metodo que añade elementos nulos en las filas de los nuevos nodos creados.
    """
    def _addNodeInRow(self,num):
        entrada = []
        
        for i in range(0,len(self._indexMap)):
            entrada.append(None)
        self._matrix.append(entrada)
        if num ==  2:
            self._addNodeInRow(0)
    
    "Cada vez que se añade un nuevo nodo a la matriz el indice se incrementa"
    def _getIncrementIndex(self):
        self._index += 1
        return self._index;
    
    """
        Inserta un nodo al grafo (si destino es None) o un arco.
        Si el arco ya existía se actualiza su etiqueta.
        Si alguno de los nodos del arco no está en el grafo, se inserta.
        Se supone que None no es una etiqueta válida.
        """
    def inserta(self, nodo, destino = None, etiqueta = 1):
       
        # obtenemos los indices de los nodos en el matriz, que se guardan
        # en un mapa para ahorrarnos recorrer la matriz. Muy eficiente
        indexOrigen = self._indexMap.get(nodo,None)
        indexDestin = self._indexMap.get(destino,None)
        nuevos = 0
		        
        # si el elemento es nuevo
        if indexOrigen is None:
            # nuevos indica el num de nodos nuevos
            nuevos = 1
            # guardamos en el mapa el indice en el que se guardo en la matriz
            indexOrigen = self._indexMap[nodo] = self._getIncrementIndex();
            # si el nodo destino es nuevo y no nulo
            if indexDestin is None and destino is not None:
                indexDestin = self._indexMap[destino] = self._getIncrementIndex();
                nuevos = 2

            # anadir el nodo a las columnas de la matriz
            self._addNodeInColumn(nuevos)
            # añadir el nodo-s a la fila
            self._addNodeInRow(nuevos)
            
        # si el elemento es antiguo
        else:
            # la entrada esta creada, no hace falta []
            if indexDestin is None and destino is not None:
                # guardamos en el mapa el indice en el que se guardo en la matriz
                indexDestin = self._indexMap[destino] = self._getIncrementIndex();
                nuevos = 1

                # anadir el nodo a las columnas de la matriz
                self._addNodeInColumn(nuevos)
                # añadir el nodo a la fila
                self._addNodeInRow(nuevos)

        # vamos a la matriz y actualizamos los valores de la nueva etiqueta
        if destino is not None:
            etiquetaOld = self._matrix[indexOrigen][indexDestin]
            self._matrix[indexOrigen][indexDestin] = etiqueta
            # si la etiqueta tenía un valor null, era que no estaba formando un arco
            if etiquetaOld is None:
                self._arrows +=1
            # si el grafo es no dirigido hacemos otro arco del destino al origen ( reves )
            if not self.dirigido():
                self._matrix[indexDestin][indexOrigen] = etiqueta

    """Indica si el nodo está en el grafo."""
    def __contains__(self, nodo):
        # si existe una entrada en el mapa
        return self._indexMap.get(nodo,None) is not None
    
    """Dado un arco (un par de nodos) devuelve la etiqueta si el arco está
        en el grafo, en caso contrario devuelve None""" 
    def __getitem__(self, arco):
        origen, destino = arco
        indexOrigen = self._indexMap.get(origen,None)
        indexDestin = self._indexMap.get(destino,None)
        if indexOrigen is None or indexDestin is None:
            return None

        return self._matrix[indexOrigen][indexDestin]

    """Iterador sobre los nodos del grafo"""
    def __iter__(self):
        # recorremos el mapa
        for nodo in self._indexMap:
            yield nodo

    """Devuelve un iterable de los pares (destino,etiqueta) para un nodo 
        origen dado.
        Construir un generador"""
    def vecinos(self, origen):
        indexOrigen = self._indexMap.get(origen,None)
        if indexOrigen is None:
            yield None

        it = iter(self._indexMap.keys())
        for i in range(0,len(self._matrix)):
            nodo = next(it)
            etiqueta = self._matrix[indexOrigen][i]
            if etiqueta is not None:
                yield (nodo,etiqueta)
    
    """Metodo para pintar el contenido del grafo. Para que se vea su estructura.
    """
    def pintarGrafo(self):
        print ("\n\nNum nodos: ",self.__len__()," Num arcos:",self.num_arcos() )
        print ("", end = "\t")
        for nodo,etiq in self._indexMap.items():
            print (nodo,etiq, end = "\t")
        print ()
        it = iter(self._indexMap)
        for fila in self._matrix:
            nodo = next(it)
            print (nodo, end = "\t")
            for etiqueta in fila:
                print(etiqueta, end = "\t")
            print ()

##################################################################################

'''
@Author: DIEGO SANZ VILLAFRUELA
@Date: 22-02-2017

Práctica sobre la implementación de grafos mediante
matriz de adyacencia y listas de adyacencia.

    '''

class GrafoListas(GrafoAbstracto):
    """
    Implementación del tipo Grafo utilizando listas de adyacencia.
    Cada nodo tiene asociada una 'lista' con la información de los arcos que
    salen del nodo. 
    Dicha lista no tinene que ser necesariamente del tipo 'list' de Python.
    """
    
    def __init__(self,dirigido=False):
        GrafoAbstracto.__init__(self,dirigido)
        # numero de arcos
        self._arrows = 0
        
        # Ej nodo 1 : {nodo2 : 10, nodo3 : 15}
        self._mapa = {}
        # controlar recursividad ( solo 2), en insertar
        self._bandera = True
    
    def getFirstNode(self):
    	iterador = iter(self)
    	return next(iterador)

    """Número de nodos del grafo."""
    def __len__( self ):
        return len(self._mapa)
    
    """Devuelve el número de arcos"""
    def num_arcos( self ):
        return self._arrows

    """
        Inserta un nodo al grafo (si destino es None) o un arco.
        Si el arco ya existía se actualiza su etiqueta.
        Si alguno de los nodos del arco no está en el grafo, se inserta.
        Se supone que None no es una etiqueta válida.
        """
    def inserta(self, nodo, destino = None, etiqueta = 1):
        # consultar si el nodo y destino existen en el mapa
        # obteniendo el valor asociado, otro mapa
        listaMapOrigen = self._mapa.get(nodo,None)
        listaMapDestin = self._mapa.get(destino,None)
        # si el nodo origen es nuevo
        if listaMapOrigen is None:
            # si el modo destino no es None
            if destino is not None:
                self._mapa[nodo] = {destino:etiqueta}
                # añadimos una entrada vacia para el nodo destino
                if listaMapDestin is None:
                     self._mapa[destino] = {}
                # incrementamos numero de arcos si no es la segunda vez que se llama ( recursivo )
                if self._bandera:
                    self._arrows +=1
                    
            # si el nodo es nuevo y el destino es None, vacio
            else:
                self._mapa[nodo] = {}

        # si el nodo origen no es nuevo
        else:
            # si el nodo destino no es nulo, acualizamos
            if destino is not None :
                etiquetaOld = listaMapOrigen.get(destino,None)
                listaMapOrigen[destino] = etiqueta
                # si la etiqueta que había no había creado un arco antes, y control recursivo
                if etiquetaOld is None and self._bandera:
                    self._arrows +=1

        # Llamada recursiva si no es dirigido, cambiando el orden Del destino al origen
        if not self.dirigido() and self._bandera and destino != None and destino != nodo:
            # bandera = false para que solo se ejecute otra vez mas
            self._bandera = False
            # del destino al origen
            self.inserta(destino, nodo, etiqueta)
            self._bandera = True
            
    """Indica si el nodo está en el grafo."""
    def __contains__(self, nodo):
        return self._mapa.get(nodo,None) is not None
        
    """Dado un arco (un par de nodos) devuelve la etiqueta si el arco está
        en el grafo, en caso contrario devuelve None"""
    def __getitem__(self, arco):
        origen, destino = arco
        listMap = self._mapa.get(origen,None)
        if listMap is not None:
            elemento = listMap.get(destino,None)
            if elemento is not None:
                return elemento
        return None

    """Iterador sobre los nodos del grafo"""
    def __iter__(self):
        for nodo in self._mapa:
            yield nodo

    """Devuelve un iterable de los pares (destino,etiqueta) para un nodo 
    origen dado.
    Construir un generador"""
    def vecinos(self, origen):
        for nodo in self._mapa[origen].items():
            yield nodo

    """Metodo para pintar el contenido del grafo. Para que se vea su estructura.
    """
    def pintarGrafo(self):
        print ("\n\nNum nodos: ",self.__len__()," Num arcos:",self.num_arcos() )

        for listaMap in self._mapa.items():
            print (listaMap[0],listaMap[1])

### END grafos.py

