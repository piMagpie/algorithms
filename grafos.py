
# coding: utf-8

# ## Algoritmia
# ### Práctica 2
# El objetivo de esta práctica es definir clases y realizar implementaciones básicas del tipo grafo.

# Se pide la implementación de las clases y/o funciones que aparecen a continuación. 
# 
# Las instrucción "pass" que aparecen en el cuerdo de las clases o funciones, se debe sustituir por la implementación adecuada. 
# 
# Para cada clase o función que se pide se proporciona una o más funciones con algunos tests. 
# 
# Al llamar a las funciones de test no debería saltar ninguna aserción.

# ### Clase abstracta para Grafos

# In[1]:

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


# ### Implementación basada en matrices de adyacencia
# Realizamos una implementación basada en [matrices de adyacencia](https://youtu.be/t-FHxHnUEoc)

# In[2]:

class GrafoMatriz(GrafoAbstracto):
    """
    Implementación del tipo Grafo utilizando una matriz de adyacencia para 
    almacenar la información de los arcos.
    La matriz podría ser una lista de lista.
    """

    def __init__(self, dirigido = False):
        super().__init__(dirigido)
        self._lista_nodos = []
        self._nodos = {}
        self._matriz = []
        self._num_arcos = 0

    def __len__(self):
        """Número de nodos del grafo."""

        return len(self._nodos)

    def num_arcos(self):
        """Devuelve el número de arcos"""
        
        return self._num_arcos;

    def __contains__(self, nodo):
        """Indica si el nodo está en el grafo."""
        
        return nodo in self._nodos
    
    def _indices(self, origen, destino = None):
        
        n1 = self._nodos.get(origen, None)
        n2 = self._nodos.get(destino, None)
        return n1, n2

    def __getitem__(self, arco):
        
        origen, destino = arco
        n1, n2 = self._indices(origen, destino)
        if n1 == None or n2 == None:
            return None
        return self._matriz[n1][n2]
        
    def inserta(self, nodo, destino = None, etiqueta = 1):
        """Añade un nodo al grafo."""
               
        if nodo not in self._nodos:
            self._nodos[nodo] = len(self._nodos)
            self._lista_nodos.append(nodo)
            for fila in self._matriz:
                fila += [None]
            self._matriz.append([None] * len(self._nodos))
        if destino != None:
            if destino not in self._nodos:
                self.inserta(destino)
            n1, n2 = self._indices(nodo, destino)
            if self._matriz[n1][n2] == None:
                self._num_arcos += 1
            self._matriz[n1][n2] = etiqueta
            if not self.dirigido():
                self._matriz[n2][n1] = etiqueta
        return self

    def __iter__(self):
        
        return iter(self._lista_nodos)

    def vecinos(self, origen):
        
        n, m = self._indices(origen)
        l = []
        i = 0
        for i, v in enumerate(self._matriz[n]):
            if v != None:
                yield self._lista_nodos[i], v

    def __str__(self):
        return str(self._lista_nodos) + " -- " + str(self._matriz)


# ### Implementación basada en listas de adyacencia
# Realizamos una implementación basada en [listas de adyacencia](https://youtu.be/7cXY3ztIGjs)

# In[3]:

class GrafoListas(GrafoAbstracto):
    """
    Implementación del tipo Grafo utilizando listas de adyacencia.
    Cada nodo tiene asociada una 'lista' con la información de los arcos que
    salen del nodo. 
    Dicha lista no tinene que ser necesariamente del tipo 'list' de Python.
    """

    def __init__(self, dirigido = False):
        super().__init__(dirigido)
        self._nodos = {}
        self._num_arcos = 0

    def __len__(self):
        """Número de nodos del grafo."""

        return len(self._nodos)

    def num_arcos(self):
        """Devuelve el número de arcos"""
        
        return self._num_arcos;

    def __contains__(self, nodo):
        """Indica si el nodo está en el grafo."""
        
        return nodo in self._nodos
    
    def __getitem__(self, arco):
        origen, destino = arco
        destinos = self._nodos.get(origen)
        if destinos != None:
            return destinos.get(destino)
        return None
        
    def inserta(self, nodo, destino = None, etiqueta = 1):
        """Añade un nodo al grafo."""
                      
        if nodo not in self._nodos:
            self._nodos[nodo] = {}
        if destino != None:
            if destino not in self._nodos:
                self.inserta(destino)
            destinos = self._nodos[nodo]
            if destino not in destinos:
                self._num_arcos += 1                
            destinos[destino] = etiqueta
            if not self.dirigido():
                self._nodos[destino][nodo] = etiqueta
        return self

    def __iter__(self):
        
        return iter(self._nodos)

    def vecinos(self, origen):
        destinos = self._nodos.get(origen)
        if destinos != None:
            for destino, valor in destinos.items():
                yield destino, valor

    def __str__(self):
        return str(self._nodos)


# ### Casos de prueba

# In[4]:

def test_grafo(grafo):
    """Función que prueba las funciones sobre grafos. Espera un grafo vacío."""

    num_final = 10  # número de nodos del grafo final
    num_arcos = 0
    conjunto_nodos = set()  # nodos que debería tener el grafo
    conjunto_arcos = set()  # arcos que debería tener el grafo
    
    # Insertamos nodos y arcos en el grafo, comprobando que la información es 
    # coherente con lo que tenemos en conjunto_nodos y conjunto_arcos
    for n in range(num_final):
        assert len(grafo) == n
        nodo_n = "n" + str(n)
        grafo.inserta(nodo_n)
        conjunto_nodos.add(nodo_n)
        assert nodo_n in grafo 
        assert n not in grafo
        for m in range(n):
            nodo_m = "n" + str(m)
            etiqueta = num_final * n + m
            grafo.inserta(nodo_m, nodo_n, etiqueta)
            conjunto_arcos.add((nodo_m, nodo_n, etiqueta))
            num_arcos += 1
            assert num_arcos == grafo.num_arcos()
            assert grafo[nodo_m, nodo_n] == etiqueta
            if grafo.dirigido():
                assert grafo[nodo_n, nodo_m] == None
            else:
                assert grafo[nodo_n, nodo_m] == etiqueta
                conjunto_arcos.add((nodo_n, nodo_m, etiqueta))
    
    # Recorremos comproabando los nodos y para cada nodo sus vecinos
    for nodo_n in grafo:
        assert nodo_n in conjunto_nodos
        conjunto_nodos.remove(nodo_n)
        for nodo_m, etiqueta in grafo.vecinos(nodo_n):
            assert (nodo_n, nodo_m, etiqueta) in conjunto_arcos
            conjunto_arcos.remove((nodo_n, nodo_m, etiqueta))
            
    # Comprobamos que hemos recorrido todos los nodos y arcos
    assert len(conjunto_nodos) == 0
    assert len(conjunto_arcos) == 0


# In[5]:

if __name__ == "__main__":     
    test_grafo(GrafoMatriz(False))
    test_grafo(GrafoMatriz(True))
    print("OK")


# In[6]:

if __name__ == "__main__":     
    test_grafo(GrafoListas(False))
    test_grafo(GrafoListas(True))
    print("OK")


# In[5]:

"""
Con %timeit podemos ver el tiempo necesario para ejecutar una línea.
Puede ejecutarla múltiples veces para tener una mejor estimación.
Con %%timeit obtenemos el tiempo de ejecución de una celda.
"""
if __name__ == "__main__":  
    get_ipython().magic('timeit test_grafo(GrafoMatriz(False))')
    get_ipython().magic('timeit test_grafo(GrafoMatriz(True))')
    get_ipython().magic('timeit test_grafo(GrafoListas(False))')
    get_ipython().magic('timeit test_grafo(GrafoListas(True))')


# In[ ]:



