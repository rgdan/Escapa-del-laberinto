import random

# Códigos de celdas
CAMINO = 0
MURO   = 1
LIANA  = 2
TUNEL  = 3

class GeneradorMapa:
    def __init__(self):
        
        self.filas = 15
        self.columnas = 20
        self.inicio = (1,1)
        self.numero_salidas = 1
        self.conectar_todas_salidas = False
        self.probabilidad_tunel_en_camino = 0.35
        self.prob_camino, self.prob_muro, self.prob_liana, self.prob_tunel = (0.35, 0.35, 0.35, 0.15)
        self.excluir_salidas_esquinas = True

        # matriz inicial: todo muro
        self.matriz = [[MURO for _ in range(self.columnas)] for _ in range(self.filas)]
        self.salidas = []

    # ----------------- utilidades internas -----------------
    def _obtener_vecinos_4_direcciones(self, fila, columna):
        """Retorna los 4 vecinos adyacentes (arriba, abajo, izquierda, derecha)."""
        for delta_fila, delta_columna in ((1,0), (-1,0), (0,1), (0,-1)):
            nueva_fila, nueva_columna = fila + delta_fila, columna + delta_columna
            if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas:
                yield nueva_fila, nueva_columna

    def _obtener_coordenadas_borde(self):
        """Retorna todas las coordenadas del borde del mapa."""
        coordenadas = []
        # superior e inferior (excluye esquinas si se pide)
        for columna in range(self.columnas):
            if self.excluir_salidas_esquinas and (columna in (0, self.columnas-1)):
                continue
            coordenadas.append((0, columna))
            coordenadas.append((self.filas-1, columna))
        # izquierda y derecha
        for fila in range(self.filas):
            if self.excluir_salidas_esquinas and (fila in (0, self.filas-1)):
                continue
            coordenadas.append((fila, 0))
            coordenadas.append((fila, self.columnas-1))
        # quitar duplicados (en caso de filas/columnas pequeñas)
        coordenadas_unicas = []
        ya_vistas = []
        for coord in coordenadas:
            if coord not in ya_vistas:
                coordenadas_unicas.append(coord)
                ya_vistas.append(coord)
        return coordenadas_unicas

    def _elegir_salidas(self):
        """Selecciona aleatoriamente las posiciones de las salidas en el borde."""
        borde = self._obtener_coordenadas_borde()
        random.shuffle(borde)
        elegidas = borde[:self.numero_salidas] if len(borde) >= self.numero_salidas else borde
        self.salidas = elegidas
        # abrir las salidas como CAMINO
        for (fila_salida, columna_salida) in self.salidas:
            self.matriz[fila_salida][columna_salida] = CAMINO

    def _buscar_camino_bfs(self, origen, destino, tipos_permitidos):
        """
        Búsqueda en anchura (BFS) para encontrar un camino entre origen y destino.
        Retorna la lista de coordenadas del camino o None si no existe.
        Implementación sin diccionarios: usa matrices para padres y visitados.
        """
        # matriz de visitados y padres (None = sin padre)
        visitados = [[False for _ in range(self.columnas)] for _ in range(self.filas)]
        padres = [[None for _ in range(self.columnas)] for _ in range(self.filas)]

        cola = [origen]
        indice_lectura = 0
        fr, fc = origen
        visitados[fr][fc] = True
        padres[fr][fc] = None

        while indice_lectura < len(cola):
            fila, columna = cola[indice_lectura]
            indice_lectura += 1

            if (fila, columna) == destino:
                # reconstruir camino usando la matriz padres
                camino = []
                actual = destino
                while actual is not None:
                    camino.append(actual)
                    ar, ac = actual
                    actual = padres[ar][ac]
                camino.reverse()
                return camino

            for nueva_fila, nueva_columna in self._obtener_vecinos_4_direcciones(fila, columna):
                if not visitados[nueva_fila][nueva_columna] and self.matriz[nueva_fila][nueva_columna] in tipos_permitidos:
                    visitados[nueva_fila][nueva_columna] = True
                    padres[nueva_fila][nueva_columna] = (fila, columna)
                    cola.append((nueva_fila, nueva_columna))
        return None

    def _conectar_ignorando_tipos(self, origen, destino):
        """
        Encuentra un camino ignorando los tipos de celda y lo marca como CAMINO.
        """
        # matriz de visitados y padres
        visitados = [[False for _ in range(self.columnas)] for _ in range(self.filas)]
        padres = [[None for _ in range(self.columnas)] for _ in range(self.filas)]

        cola = [origen]
        indice_lectura = 0
        fr, fc = origen
        visitados[fr][fc] = True
        padres[fr][fc] = None

        encontrado = False
        while indice_lectura < len(cola):
            fila, columna = cola[indice_lectura]
            indice_lectura += 1

            if (fila, columna) == destino:
                encontrado = True
                break

            for nueva_fila, nueva_columna in self._obtener_vecinos_4_direcciones(fila, columna):
                if not visitados[nueva_fila][nueva_columna]:
                    visitados[nueva_fila][nueva_columna] = True
                    padres[nueva_fila][nueva_columna] = (fila, columna)
                    cola.append((nueva_fila, nueva_columna))

        # reconstruir y tallar el camino sólo si destino fue alcanzado (o es el origen)
        actual = destino
        ar, ac = actual
        if not encontrado and actual != origen and padres[ar][ac] is None:
            return  # no hay camino encontrado; no se modifica el mapa

        while actual is not None:
            fila, columna = actual
            self.matriz[fila][columna] = CAMINO
            pr = padres[fila][columna]
            actual = pr

    def _tallar_camino_aleatorio_dfs(self, origen, destino):
        """
        Intenta tallar un camino aleatorio usando búsqueda en profundidad (DFS).
        Marca celdas como CAMINO o TUNEL, evitando tocar el borde excepto en la salida.
        """
        pila = [origen]
        visitados = [] 

        while pila:
            fila, columna = pila.pop()
            if (fila, columna) in visitados:
                continue
            visitados.append((fila, columna))

            # el inicio siempre es camino
            if (fila, columna) == origen:
                self.matriz[fila][columna] = CAMINO
            elif (fila, columna) == destino:
                # asegurar que la salida sea siempre CAMINO (nunca TUNEL)
                self.matriz[fila][columna] = CAMINO
            else:
                # decidir aleatoriamente si es túnel o camino
                self.matriz[fila][columna] = TUNEL if random.random() < self.probabilidad_tunel_en_camino else CAMINO

            if (fila, columna) == destino:
                return True

            vecinos = list(self._obtener_vecinos_4_direcciones(fila, columna))
            random.shuffle(vecinos)
            
            for nueva_fila, nueva_columna in vecinos:
                # impedir tocar el borde excepto la celda de salida
                es_borde = (nueva_fila in (0, self.filas-1)) or (nueva_columna in (0, self.columnas-1))
                if es_borde and (nueva_fila, nueva_columna) != destino:
                    continue
                if (nueva_fila, nueva_columna) not in visitados:
                    pila.append((nueva_fila, nueva_columna))
        return False

    def _rellenar_mapa_aleatorio(self):
        """
        Rellena el resto del mapa con tipos de celda aleatorios según las probabilidades.
        No modifica bordes, inicio, salidas ni caminos ya tallados.
        """
        for fila in range(self.filas):
            for columna in range(self.columnas):
                # el borde siempre es muro, salvo las salidas
                es_borde = (fila in (0, self.filas-1)) or (columna in (0, self.columnas-1))
                if es_borde and (fila, columna) not in self.salidas:
                    self.matriz[fila][columna] = MURO
                    continue
                
                # no tocar inicio, salidas ni celdas ya talladas como CAMINO/TUNEL
                if (fila, columna) == self.inicio or (fila, columna) in self.salidas or self.matriz[fila][columna] in (CAMINO, TUNEL):
                    continue
                
                # asignar tipo aleatorio según probabilidades
                valor_aleatorio = random.random()
                if valor_aleatorio < self.prob_muro:
                    self.matriz[fila][columna] = MURO
                elif valor_aleatorio < self.prob_muro + self.prob_camino:
                    self.matriz[fila][columna] = CAMINO
                elif valor_aleatorio < self.prob_muro + self.prob_camino + self.prob_liana:
                    self.matriz[fila][columna] = LIANA
                else:
                    self.matriz[fila][columna] = TUNEL

    # ----------------- API principal -----------------
    def generar(self):
        """
        Genera el mapa completo y garantiza conexión al menos a una salida.
        Retorna: (matriz, inicio, salidas)
        """
        # 1) limpiar todo a MURO
        for fila in range(self.filas):
            for columna in range(self.columnas):
                self.matriz[fila][columna] = MURO

        # 3) elegir y abrir salidas
        self._elegir_salidas()
        # asegurar que exista una salida principal antes de usarla
        if not self.salidas:
            self._elegir_salidas()
        salida_principal = self.salidas[0]

       
        tallado_exitoso = self._tallar_camino_aleatorio_dfs(self.inicio, salida_principal)
        
        # si no talló correctamente, conectar ignorando tipos
        if not tallado_exitoso or self._buscar_camino_bfs(self.inicio, salida_principal, {CAMINO, TUNEL}) is None:
            self._conectar_ignorando_tipos(self.inicio, salida_principal)

        # 5) opcional: conectar a todas las salidas restantes
        if self.conectar_todas_salidas and len(self.salidas) > 1:
            for salida_extra in self.salidas[1:]:
                if self._buscar_camino_bfs(self.inicio, salida_extra, {CAMINO, TUNEL}) is None:
                    # intentar tallar camino aleatorio primero
                    tallado_ok = self._tallar_camino_aleatorio_dfs(self.inicio, salida_extra)
                    if not tallado_ok or self._buscar_camino_bfs(self.inicio, salida_extra, {CAMINO, TUNEL}) is None:
                        self._conectar_ignorando_tipos(self.inicio, salida_extra)

        # 6) rellenar el resto del mapa con mezcla aleatoria
        self._rellenar_mapa_aleatorio()

        # 7) validación final de la salida principal
        if self._buscar_camino_bfs(self.inicio, salida_principal, {CAMINO, TUNEL}) is None:
            self._conectar_ignorando_tipos(self.inicio, salida_principal)

        return self.matriz, self.inicio, self.salidas

"""
# ----------------- Ejemplo de uso -----------------
if __name__ == "__main__":
    # Configura a tu gusto:
    
    generador = GeneradorMapa()
    mapa, inicio, salidas = generador.generar()
    print("Inicio:", inicio)
    print("Salidas:", salidas)
    for fila in mapa:
        print(fila)
"""