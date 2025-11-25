import random
from src.terreno import Camino, Muro, Liana, Tunel

CAMINO = 0
MURO   = 1
LIANA  = 2
TUNEL  = 3

class GeneradorMapa:
    def __init__(self):
        
        self.filas = 15
        self.columnas = 20
        self.inicio = (1,1)
        self.numero_salidas = 2
        self.conectar_todas_salidas = False
        self.probabilidad_tunel_en_camino = 0.10
        self.prob_camino, self.prob_muro, self.prob_liana, self.prob_tunel = (0.45, 0.10, 0.15, 0.10)
        self.excluir_salidas_esquinas = True
        self.porcentaje_conversion_camino = 0.30

        # matriz inicial: todo muro
        self.matriz = [[MURO for _ in range(self.columnas)] for _ in range(self.filas)]
        self.salidas = []

    # retorna vecinos en 4 direcciones (arriba, abajo, izquierda, derecha)
    def obtener_vecinos_4_direcciones(self, fila, columna):
        for delta_fila, delta_columna in ((1,0), (-1,0), (0,1), (0,-1)):
            nueva_fila, nueva_columna = fila + delta_fila, columna + delta_columna
            if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas: yield nueva_fila, nueva_columna

    # obtener todas las coordenadas del borde del mapa
    def obtener_coordenadas_borde(self):
        coordenadas = []

        # superior e inferior (excluye esquinas si se pide)
        for columna in range(self.columnas):
            if self.excluir_salidas_esquinas and (columna in (0, self.columnas-1)): continue
            coordenadas.append((0, columna))
            coordenadas.append((self.filas-1, columna))

        # izquierda y derecha
        for fila in range(self.filas):
            if self.excluir_salidas_esquinas and (fila in (0, self.filas-1)): continue
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

    # elegir y abrir salidas en el borde del mapa
    def elegir_salidas(self):
        borde = self.obtener_coordenadas_borde()
        random.shuffle(borde)
        elegidas = borde[:self.numero_salidas] if len(borde) >= self.numero_salidas else borde
        self.salidas = elegidas
        # abrir las salidas como CAMINO
        for (fila_salida, columna_salida) in self.salidas:
            self.matriz[fila_salida][columna_salida] = CAMINO
            # asegurar que haya al menos un camino adyacente interior a la salida
            for vecino_x, vecino_y in self.obtener_vecinos_4_direcciones(fila_salida, columna_salida):
                # el vecino debe ser interior (no borde)
                es_borde_vecino = (vecino_x in (0, self.filas-1)) or (vecino_y in (0, self.columnas-1))
                if not es_borde_vecino:
                    self.matriz[vecino_x][vecino_y] = CAMINO
                    break  # solo necesitamos asegurar un vecino como camino

    # BFS para encontrar camino entre origen y destino usando solo tipos permitidos
    def buscar_camino(self, origen, destino, tipos_permitidos):
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

            for nueva_fila, nueva_columna in self.obtener_vecinos_4_direcciones(fila, columna):
                if not visitados[nueva_fila][nueva_columna] and self.matriz[nueva_fila][nueva_columna] in tipos_permitidos:
                    visitados[nueva_fila][nueva_columna] = True
                    padres[nueva_fila][nueva_columna] = (fila, columna)
                    cola.append((nueva_fila, nueva_columna))
        return None

    # BFS para conectar origen y destino ignorando tipos (usa CAMINO y TUNEL)
    def conectar_ignorando_tipos(self, origen, destino):
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

            for nueva_fila, nueva_columna in self.obtener_vecinos_4_direcciones(fila, columna):
                if not visitados[nueva_fila][nueva_columna]:
                    visitados[nueva_fila][nueva_columna] = True
                    padres[nueva_fila][nueva_columna] = (fila, columna)
                    cola.append((nueva_fila, nueva_columna))

        # reconstruir y tallar el camino sólo si destino fue alcanzado (o es el origen)
        actual = destino
        ar, ac = actual
        if not encontrado and actual != origen and padres[ar][ac] is None: return  # no hay camino encontrado; no se modifica el mapa

        while actual is not None:
            fila, columna = actual
            self.matriz[fila][columna] = CAMINO
            pr = padres[fila][columna]
            actual = pr

    # tallar camino aleatorio entre origen y destino
    def tallar_camino_aleatorio(self, origen, destino):
        pila = [origen]
        visitados = [] 

        while pila:
            fila, columna = pila.pop()
            if (fila, columna) in visitados: continue
            visitados.append((fila, columna))

            # el inicio siempre es camino
            if (fila, columna) == origen: self.matriz[fila][columna] = CAMINO
            # asegurar que la salida sea siempre CAMINO (nunca TUNEL
            elif (fila, columna) == destino: self.matriz[fila][columna] = CAMINO
            # decidir aleatoriamente si es túnel o camino
            else: self.matriz[fila][columna] = TUNEL if random.random() < self.probabilidad_tunel_en_camino else CAMINO

            if (fila, columna) == destino: return True

            vecinos = list(self.obtener_vecinos_4_direcciones(fila, columna))
            random.shuffle(vecinos)
            
            for nueva_fila, nueva_columna in vecinos:
                # impedir tocar el borde excepto la celda de salida
                es_borde = (nueva_fila in (0, self.filas-1)) or (nueva_columna in (0, self.columnas-1))
                if es_borde and (nueva_fila, nueva_columna) != destino: continue
                if (nueva_fila, nueva_columna) not in visitados: pila.append((nueva_fila, nueva_columna))
        return False

    # rellenar el mapa con mezcla aleatoria según probabilidades
    def rellenar_mapa_aleatorio(self):
        
        # normalizar probabilidades para evitar que sumas != 1 hagan inalcanzable alguna opción
        probs = [self.prob_muro, self.prob_camino, self.prob_liana, self.prob_tunel]
        total = sum(probs)
        # valores por defecto si la suma es 0 o negativa
        if total <= 0: p_muro, p_camino, p_liana, p_tunel = 0.40, 0.15, 0.25, 0.20
        else: p_muro, p_camino, p_liana, p_tunel = (p / total for p in probs)

        umbral_muro = p_muro
        umbral_camino = umbral_muro + p_camino
        umbral_liana = umbral_camino + p_liana
        # umbral_tunel implícito: resto hasta 1.0

        # recolectar vecinos interiores de salidas para protegerlos
        vecinos_salidas = set()
        for sx, sy in self.salidas:
            for vx, vy in self.obtener_vecinos_4_direcciones(sx, sy):
                es_borde_v = (vx in (0, self.filas-1)) or (vy in (0, self.columnas-1))
                if not es_borde_v: vecinos_salidas.add((vx, vy))

        for fila in range(self.filas):
            for columna in range(self.columnas):
                # el borde siempre es muro, salvo las salidas
                es_borde = (fila in (0, self.filas-1)) or (columna in (0, self.columnas-1))
                if es_borde and (fila, columna) not in self.salidas:
                    self.matriz[fila][columna] = MURO
                    continue

                # no tocar inicio, salidas, vecinos de salidas ni celdas ya talladas como CAMINO/TUNEL
                if (fila, columna) == self.inicio or (fila, columna) in self.salidas or (fila, columna) in vecinos_salidas or self.matriz[fila][columna] in (CAMINO, TUNEL): continue

                # asignar tipo aleatorio según probabilidades normalizadas
                valor_aleatorio = random.random()
                if valor_aleatorio < umbral_muro: self.matriz[fila][columna] = MURO
                elif valor_aleatorio < umbral_camino: self.matriz[fila][columna] = CAMINO
                elif valor_aleatorio < umbral_liana: self.matriz[fila][columna] = LIANA
                else: self.matriz[fila][columna] = TUNEL

        # convertir algunos CAMINO en obstáculos (lianas/túneles/muros) sin romper conectividad
        self._convertir_caminos_a_obstaculos()

    # obtener componentes conexas de tipos permitidos
    def obtener_componentes_conexas(self, tipos_permitidos):
        visitados = [[False for _ in range(self.columnas)] for _ in range(self.filas)]
        componentes = []

        for fila in range(self.filas):
            for columna in range(self.columnas):
                if not visitados[fila][columna] and self.matriz[fila][columna] in tipos_permitidos:
                    # BFS para encontrar toda la componente conexa
                    componente = []
                    cola = [(fila, columna)]
                    visitados[fila][columna] = True
                    indice = 0

                    while indice < len(cola):
                        f, c = cola[indice]
                        indice += 1
                        componente.append((f, c))

                        for nf, nc in self.obtener_vecinos_4_direcciones(f, c):
                            if not visitados[nf][nc] and self.matriz[nf][nc] in tipos_permitidos:
                                visitados[nf][nc] = True
                                cola.append((nf, nc))

                    componentes.append(componente)

        return componentes

    # conectar todas las componentes conexas usando CAMINO
    def conectar_componentes(self, componentes, tipos_permitidos):
        if len(componentes) <= 1: return

        # Conectar cada componente a la que contiene el inicio
        componente_principal = None
        for comp in componentes:
            if self.inicio in comp:
                componente_principal = comp
                break

        if componente_principal is None: componente_principal = componentes[0]

        for comp in componentes:
            if comp == componente_principal: continue

            # Buscar el punto más cercano entre esta componente y la principal
            min_dist = float('inf')
            mejor_origen = None
            mejor_destino = None

            for celda_comp in comp:
                for celda_principal in componente_principal:
                    dist = abs(celda_comp[0] - celda_principal[0]) + abs(celda_comp[1] - celda_principal[1])
                    if dist < min_dist:
                        min_dist = dist
                        mejor_origen = celda_principal
                        mejor_destino = celda_comp

            # Conectar usando CAMINO para que jugador y enemigos puedan usar el camino
            if mejor_origen and mejor_destino:
                self.conectar_ignorando_tipos_con_camino(mejor_origen, mejor_destino)

    # conectar ignorando tipos pero usando solo CAMINO
    def conectar_ignorando_tipos_con_camino(self, origen, destino):
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

            for nueva_fila, nueva_columna in self.obtener_vecinos_4_direcciones(fila, columna):
                if not visitados[nueva_fila][nueva_columna]:
                    visitados[nueva_fila][nueva_columna] = True
                    padres[nueva_fila][nueva_columna] = (fila, columna)
                    cola.append((nueva_fila, nueva_columna))

        actual = destino
        ar, ac = actual
        if not encontrado and actual != origen and padres[ar][ac] is None: return

        # Tallar con CAMINO en lugar de mezclar con TUNEL
        while actual is not None:
            fila, columna = actual
            # Solo usar CAMINO para que enemigos también puedan pasar
              # No modificar las salidas
            if (fila, columna) not in self.salidas: self.matriz[fila][columna] = CAMINO
            pr = padres[fila][columna]
            actual = pr

    # validar que todas las celdas transitables estén conectadas
    def validar_conectividad_completa(self):
        # Validar para el jugador (CAMINO + TUNEL)
        componentes_jugador = self.obtener_componentes_conexas({CAMINO, TUNEL})
        if len(componentes_jugador) > 1: self.conectar_componentes(componentes_jugador, {CAMINO, TUNEL})

        # Validar para enemigos (solo CAMINO)
        componentes_enemigos = self.obtener_componentes_conexas({CAMINO})
        if len(componentes_enemigos) > 1: self.conectar_componentes(componentes_enemigos, {CAMINO})

        # Verificar que inicio y todas las salidas estén en la componente principal
        for salida in self.salidas:
            if self.buscar_camino(self.inicio, salida, {CAMINO, TUNEL}) is None: self.conectar_ignorando_tipos_con_camino(self.inicio, salida)
            if self.buscar_camino(self.inicio, salida, {CAMINO}) is None: self.conectar_ignorando_tipos_con_camino(self.inicio, salida)

    # convertir un porcentaje de CAMINO en obstáculos sin romper conectividad
    def _convertir_caminos_a_obstaculos(self):
        
        # recolectar vecinos interiores de salidas para no convertirlos
        vecinos_salidas = set()
        for sx, sy in self.salidas:
            for vx, vy in self.obtener_vecinos_4_direcciones(sx, sy):
                es_borde_v = (vx in (0, self.filas-1)) or (vy in (0, self.columnas-1))
                if not es_borde_v:
                    vecinos_salidas.add((vx, vy))
        
        candidatos = []
        for x in range(self.filas):
            for y in range(self.columnas):
                # excluir inicio, salidas y vecinos inmediatos de salidas
                if self.matriz[x][y] == CAMINO and (x, y) != self.inicio and (x, y) not in self.salidas and (x, y) not in vecinos_salidas: candidatos.append((x, y))

        # barajar y tomar porcentaje para convertir
        random.shuffle(candidatos)
        num_convertir = int(len(candidatos) * self.porcentaje_conversion_camino)
        a_convertir = candidatos[:num_convertir]

        # distribuir conversiones entre LIANA, TUNEL, MURO (33% cada uno aprox)
        tipos_obstaculo = [LIANA, TUNEL, MURO]
        convertidos = 0
        for x, y in a_convertir:
            # verificar si esta celda es crítica para conectividad
            # contar vecinos transitables (CAMINO o TUNEL)
            vecinos_transitables = 0
            for nx, ny in self.obtener_vecinos_4_direcciones(x, y):
                if self.matriz[nx][ny] in (CAMINO, TUNEL):
                    vecinos_transitables += 1
            
            # solo convertir si tiene más de 2 vecinos transitables (no es cuello de botella)
            if vecinos_transitables > 2:
                tipo_nuevo = random.choice(tipos_obstaculo)
                valor_original = self.matriz[x][y]
                self.matriz[x][y] = tipo_nuevo
                
                # verificar que sigue existiendo camino tanto para jugador como para enemigos
                camino_valido_jugador = True
                camino_valido_enemigos = True
                
                for salida in self.salidas:
                    # Validar camino para jugador (CAMINO + TUNEL)
                    if self.buscar_camino(self.inicio, salida, {CAMINO, TUNEL}) is None:
                        camino_valido_jugador = False
                        break
                    # Validar camino para enemigos (solo CAMINO)
                    if self.buscar_camino(self.inicio, salida, {CAMINO}) is None:
                        camino_valido_enemigos = False
                        break
                
                # Solo mantener la conversión si ambos tipos de entidades mantienen conectividad
                if camino_valido_jugador and camino_valido_enemigos:
                    convertidos += 1
                else:
                    # revertir conversión si rompió la conectividad
                    self.matriz[x][y] = valor_original
            
            # limitar conversiones para mantener jugabilidad
            if convertidos >= num_convertir:
                break

    # generar el mapa completo, the main attraction
    def generar(self):
        
        #limpiar todo a MURO
        for fila in range(self.filas):
            for columna in range(self.columnas): self.matriz[fila][columna] = MURO

        # elegir y abrir salidas
        self.elegir_salidas()
        # asegurar que exista una salida principal antes de usarla
        if not self.salidas: self.elegir_salidas()
        salida_principal = self.salidas[0]

        tallado_exitoso = self.tallar_camino_aleatorio(self.inicio, salida_principal)
        
        # si no talló correctamente, conectar ignorando tipos
        if not tallado_exitoso or self.buscar_camino(self.inicio, salida_principal, {CAMINO, TUNEL}) is None: self.conectar_ignorando_tipos(self.inicio, salida_principal)

        # opcional: conectar a todas las salidas restantes
        if self.conectar_todas_salidas and len(self.salidas) > 1:
            for salida_extra in self.salidas[1:]:
                if self.buscar_camino(self.inicio, salida_extra, {CAMINO, TUNEL}) is None:
                    # intentar tallar camino aleatorio primero
                    tallado_ok = self.tallar_camino_aleatorio(self.inicio, salida_extra)
                    if not tallado_ok or self.buscar_camino(self.inicio, salida_extra, {CAMINO, TUNEL}) is None:
                        self.conectar_ignorando_tipos(self.inicio, salida_extra)
        # rellenar el resto del mapa con mezcla aleatoria
        self.rellenar_mapa_aleatorio()

        # validar conectividad completa para jugador y enemigos
        self.validar_conectividad_completa()

        # validación final de la salida principal
        if self.buscar_camino(self.inicio, salida_principal, {CAMINO, TUNEL}) is None:
            self.conectar_ignorando_tipos(self.inicio, salida_principal)

        # validación final: asegurar que cada salida tenga al menos un vecino CAMINO
        for sx, sy in self.salidas:
            tiene_vecino_camino = False
            for vx, vy in self.obtener_vecinos_4_direcciones(sx, sy):
                es_borde_v = (vx in (0, self.filas-1)) or (vy in (0, self.columnas-1))
                if not es_borde_v and self.matriz[vx][vy] == CAMINO:
                    tiene_vecino_camino = True
                    break
            if not tiene_vecino_camino:
                for vx, vy in self.obtener_vecinos_4_direcciones(sx, sy):
                    es_borde_v = (vx in (0, self.filas-1)) or (vy in (0, self.columnas-1))
                    if not es_borde_v:
                        self.matriz[vx][vy] = CAMINO
                        break

        # validación final de conectividad para enemigos
        for salida in self.salidas:
            if self.buscar_camino(self.inicio, salida, {CAMINO}) is None: self.conectar_ignorando_tipos_con_camino(self.inicio, salida)

        return self._convertir_a_terrenos(), self.inicio, self.salidas
    
    #E: None
    #S: list of list of Terreno objects
    def _convertir_a_terrenos(self):
        mapa_terrenos = []
        for fila_idx in range(self.filas):
            fila_terrenos = []
            for col_idx in range(self.columnas):
                celda = self.matriz[fila_idx][col_idx]
                if celda == CAMINO: terreno = Camino(fila_idx, col_idx)
                elif celda == MURO: terreno = Muro(fila_idx, col_idx)
                elif celda == LIANA: terreno = Liana(fila_idx, col_idx)
                elif celda == TUNEL: terreno = Tunel(fila_idx, col_idx)
                else: terreno = Muro(fila_idx, col_idx)
                fila_terrenos.append(terreno)
            mapa_terrenos.append(fila_terrenos)
        return mapa_terrenos

# ----------------- Ejemplo de uso -----------------
if __name__ == "__main__":
    # Configura a tu gusto:
    
    generador = GeneradorMapa()
    mapa = generador.generar()
    for fila in mapa:
        print(fila)

