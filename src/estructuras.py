"""
Tres estrategias de almacenamiento/búsqueda: Lista Enlazada, ABB y B+.
Cada una expone: insertar(estudiante), buscar(id) y listar_en_orden().
ABB y B+ además exponen altura().
"""

# -----------------------------------------------------------------------------
# LISTA ENLAZADA
# -----------------------------------------------------------------------------
class NodoLista:
    def __init__(self, estudiante):
        self.id = estudiante["id"]
        self.nombre = estudiante["nombre"]
        self.edad = estudiante["edad"]
        self.promedio = estudiante["promedio"]
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def insertar(self, estudiante):
        nuevo = NodoLista(estudiante)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamano += 1

    def buscar(self, id_buscado):
        actual = self.cabeza
        while actual is not None:
            if actual.id == id_buscado:
                return actual
            actual = actual.siguiente
        return None

    def listar_en_orden(self):
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append((actual.id, actual.nombre, actual.edad, actual.promedio))
            actual = actual.siguiente
        return sorted(resultado, key=lambda x: x[0])


def construir_lista(datos):
    lista = ListaEnlazada()
    for est in datos:
        lista.insertar(est)
    return lista


# -----------------------------------------------------------------------------
# ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# -----------------------------------------------------------------------------
class NodoABB:
    def __init__(self, estudiante):
        self.id = estudiante["id"]
        self.nombre = estudiante["nombre"]
        self.edad = estudiante["edad"]
        self.promedio = estudiante["promedio"]
        self.izquierdo = None
        self.derecho = None


class ABB:
    def __init__(self):
        self.raiz = None
        self.tamano = 0

    def insertar(self, estudiante):
        self.tamano += 1
        if self.raiz is None:
            self.raiz = NodoABB(estudiante)
            return
        actual = self.raiz
        while True:
            if estudiante["id"] < actual.id:
                if actual.izquierdo is None:
                    actual.izquierdo = NodoABB(estudiante)
                    return
                actual = actual.izquierdo
            elif estudiante["id"] > actual.id:
                if actual.derecho is None:
                    actual.derecho = NodoABB(estudiante)
                    return
                actual = actual.derecho
            else:
                return  # id duplicado, se ignora

    def buscar(self, id_buscado):
        actual = self.raiz
        while actual is not None:
            if id_buscado == actual.id:
                return actual
            elif id_buscado < actual.id:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

    def listar_en_orden(self):
        """Recorrido in-order ITERATIVO (evita RecursionError en árboles
        degenerados, donde la profundidad puede ser igual a N)."""
        resultado = []
        pila = []
        actual = self.raiz
        while actual is not None or pila:
            while actual is not None:
                pila.append(actual)
                actual = actual.izquierdo
            actual = pila.pop()
            resultado.append((actual.id, actual.nombre, actual.edad, actual.promedio))
            actual = actual.derecho
        return resultado

    def altura(self):
        """Niveles desde la raíz hasta la hoja más profunda.
        Implementado por niveles (BFS) para evitar RecursionError
        cuando el árbol está degenerado (inserción ordenada)."""
        if self.raiz is None:
            return 0
        nivel_actual = [self.raiz]
        altura = 0
        while nivel_actual:
            altura += 1
            siguiente_nivel = []
            for nodo in nivel_actual:
                if nodo.izquierdo is not None:
                    siguiente_nivel.append(nodo.izquierdo)
                if nodo.derecho is not None:
                    siguiente_nivel.append(nodo.derecho)
            nivel_actual = siguiente_nivel
        return altura


def construir_abb(datos):
    arbol = ABB()
    for est in datos:
        arbol.insertar(est)
    return arbol


# -----------------------------------------------------------------------------
# ÁRBOL B+ (simplificado, orden configurable)
# -----------------------------------------------------------------------------
ORDEN_BPLUS = 4  # número máximo de hijos por nodo interno (ajustable)


class NodoBPlus:
    def __init__(self, hoja=True):
        self.hoja = hoja
        self.claves = []          # ids
        self.valores = []         # datos del estudiante (solo si es hoja)
        self.hijos = []           # sub-nodos (solo si NO es hoja)
        self.siguiente = None     # enlace entre hojas (solo si es hoja)


class BPlus:
    def __init__(self, orden=ORDEN_BPLUS):
        self.orden = orden
        self.raiz = NodoBPlus(hoja=True)
        self.tamano = 0

    def buscar(self, id_buscado):
        nodo = self.raiz
        while not nodo.hoja:
            i = 0
            while i < len(nodo.claves) and id_buscado >= nodo.claves[i]:
                i += 1
            nodo = nodo.hijos[i]
        for i, clave in enumerate(nodo.claves):
            if clave == id_buscado:
                return nodo.valores[i]
        return None

    def insertar(self, estudiante):
        self.tamano += 1
        nueva_raiz = self._insertar_recursivo(self.raiz, estudiante)
        if nueva_raiz is not None:
            self.raiz = nueva_raiz

    def _insertar_recursivo(self, nodo, estudiante):
        if nodo.hoja:
            i = 0
            while i < len(nodo.claves) and estudiante["id"] > nodo.claves[i]:
                i += 1
            if i < len(nodo.claves) and nodo.claves[i] == estudiante["id"]:
                return None  # id duplicado
            nodo.claves.insert(i, estudiante["id"])
            nodo.valores.insert(i, estudiante)
            if len(nodo.claves) < self.orden:
                return None
            return self._dividir_hoja(nodo)
        else:
            i = 0
            while i < len(nodo.claves) and estudiante["id"] >= nodo.claves[i]:
                i += 1
            resultado = self._insertar_recursivo(nodo.hijos[i], estudiante)
            if resultado is None:
                return None
            clave_subida, nuevo_hijo = resultado
            nodo.claves.insert(i, clave_subida)
            nodo.hijos.insert(i + 1, nuevo_hijo)
            if len(nodo.hijos) <= self.orden:
                return None
            return self._dividir_interno(nodo)

    def _dividir_hoja(self, nodo):
        mitad = len(nodo.claves) // 2
        nueva = NodoBPlus(hoja=True)
        nueva.claves = nodo.claves[mitad:]
        nueva.valores = nodo.valores[mitad:]
        nodo.claves = nodo.claves[:mitad]
        nodo.valores = nodo.valores[:mitad]
        nueva.siguiente = nodo.siguiente
        nodo.siguiente = nueva

        if nodo is self.raiz:
            nueva_raiz = NodoBPlus(hoja=False)
            nueva_raiz.claves = [nueva.claves[0]]
            nueva_raiz.hijos = [nodo, nueva]
            return nueva_raiz
        return (nueva.claves[0], nueva)

    def _dividir_interno(self, nodo):
        mitad = len(nodo.claves) // 2
        clave_subida = nodo.claves[mitad]

        nueva = NodoBPlus(hoja=False)
        nueva.claves = nodo.claves[mitad + 1:]
        nueva.hijos = nodo.hijos[mitad + 1:]
        nodo.claves = nodo.claves[:mitad]
        nodo.hijos = nodo.hijos[:mitad + 1]

        if nodo is self.raiz:
            nueva_raiz = NodoBPlus(hoja=False)
            nueva_raiz.claves = [clave_subida]
            nueva_raiz.hijos = [nodo, nueva]
            return nueva_raiz
        return (clave_subida, nueva)

    def listar_en_orden(self):
        """Recorre las hojas encadenadas de izquierda a derecha."""
        resultado = []
        nodo = self.raiz
        while not nodo.hoja:
            nodo = nodo.hijos[0]
        while nodo is not None:
            for est in nodo.valores:
                resultado.append((est["id"], est["nombre"], est["edad"], est["promedio"]))
            nodo = nodo.siguiente
        return resultado

    def altura(self):
        altura = 1
        nodo = self.raiz
        while not nodo.hoja:
            altura += 1
            nodo = nodo.hijos[0]
        return altura


def construir_bplus(datos, orden=ORDEN_BPLUS):
    arbol = BPlus(orden=orden)
    for est in datos:
        arbol.insertar(est)
    return arbol