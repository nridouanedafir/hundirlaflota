import random

import numpy as np

from clases import Barco, Coordenada


AGUA = " "
BARCO = "O"
TOCADO = "X"
FALLO = "-"
FLOTA = (2, 2, 2, 3, 3, 4)
ORIENTACIONES = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "O": (0, -1),
}


def crear_tablero(tamano: int = 10) -> np.ndarray:
    """Crea un tablero cuadrado vacío."""
    if not isinstance(tamano, int) or isinstance(tamano, bool) or tamano <= 0:
        raise ValueError("El tamaño del tablero debe ser un entero positivo.")
    return np.full((tamano, tamano), AGUA, dtype="<U1")


def _posiciones_barco(
    fila: int, columna: int, eslora: int, orientacion: str
) -> list[Coordenada]:
    delta_fila, delta_columna = ORIENTACIONES[orientacion]
    return [
        (fila + delta_fila * paso, columna + delta_columna * paso)
        for paso in range(eslora)
    ]


def crear_barco(eslora: int, tablero: np.ndarray) -> Barco:
    """Busca aleatoriamente un inicio y orientación donde quepa el barco."""
    if not isinstance(eslora, int) or isinstance(eslora, bool) or eslora <= 0:
        raise ValueError("La eslora debe ser un entero positivo.")
    if tablero.ndim != 2 or tablero.shape[0] != tablero.shape[1]:
        raise ValueError("El tablero debe ser una matriz cuadrada.")
    tamano = tablero.shape[0]
    if eslora > tamano:
        raise ValueError("La eslora no puede superar el tamaño del tablero.")

    candidatos = [
        (fila, columna, orientacion)
        for fila in range(tamano)
        for columna in range(tamano)
        for orientacion in ORIENTACIONES
    ]
    while candidatos:
        indice = random.randrange(len(candidatos))
        fila, columna, orientacion = candidatos.pop(indice)
        posiciones = _posiciones_barco(fila, columna, eslora, orientacion)
        if all(
            0 <= f < tamano
            and 0 <= c < tamano
            and tablero[f, c] == AGUA
            for f, c in posiciones
        ):
            return Barco(eslora=eslora, posiciones=posiciones)

    raise ValueError(f"No hay espacio disponible para un barco de eslora {eslora}.")


def colocar_barco(barco: Barco, tablero: np.ndarray) -> np.ndarray:
    """Coloca un barco si sus posiciones son contiguas y están libres."""
    if tablero.ndim != 2 or tablero.shape[0] != tablero.shape[1]:
        raise ValueError("El tablero debe ser una matriz cuadrada.")
    if barco.eslora <= 0 or len(barco.posiciones) != barco.eslora:
        raise ValueError("El número de posiciones debe coincidir con la eslora.")
    if len(set(barco.posiciones)) != len(barco.posiciones):
        raise ValueError("El barco no puede ocupar una casilla más de una vez.")

    filas = {fila for fila, _ in barco.posiciones}
    columnas = {columna for _, columna in barco.posiciones}
    if len(filas) == 1:
        ordenadas = sorted(columnas)
        contiguo = ordenadas == list(
            range(ordenadas[0], ordenadas[0] + barco.eslora)
        )
    elif len(columnas) == 1:
        ordenadas = sorted(filas)
        contiguo = ordenadas == list(
            range(ordenadas[0], ordenadas[0] + barco.eslora)
        )
    else:
        contiguo = False
    if not contiguo:
        raise ValueError("Las posiciones del barco deben formar una línea contigua.")

    tamano = tablero.shape[0]
    for fila, columna in barco.posiciones:
        if not (0 <= fila < tamano and 0 <= columna < tamano):
            raise ValueError("El barco queda fuera del tablero.")
        if tablero[fila, columna] != AGUA:
            raise ValueError("El barco se solapa con otro.")

    for fila, columna in barco.posiciones:
        tablero[fila, columna] = BARCO
    return tablero


def colocar_barcos(tablero: np.ndarray) -> list[Barco]:
    """Coloca aleatoriamente la flota indicada en el enunciado HLF."""
    barcos = []
    for eslora in FLOTA:
        barco = crear_barco(eslora, tablero)
        colocar_barco(barco, tablero)
        barcos.append(barco)
    return barcos


def disparar(
    fila: int,
    columna: int,
    tablero: np.ndarray,
    barcos: list[Barco] | None = None,
) -> str:
    """Dispara y devuelve 'agua', 'tocado' o 'hundido'."""
    if tablero.ndim != 2:
        raise ValueError("El tablero debe ser una matriz de dos dimensiones.")
    if not (
        isinstance(fila, int)
        and not isinstance(fila, bool)
        and isinstance(columna, int)
        and not isinstance(columna, bool)
    ):
        raise ValueError("Las coordenadas deben ser números enteros.")
    if not (0 <= fila < tablero.shape[0] and 0 <= columna < tablero.shape[1]):
        raise ValueError("El disparo queda fuera del tablero.")

    casilla = tablero[fila, columna]
    if casilla in (TOCADO, FALLO):
        raise ValueError("Ya se había disparado a esa casilla.")
    if casilla == AGUA:
        tablero[fila, columna] = FALLO
        return "agua"
    if casilla != BARCO:
        raise ValueError("La casilla del tablero tiene un estado desconocido.")

    barco_impactado = next(
        (
            barco
            for barco in barcos or []
            if (fila, columna) in barco.posiciones
        ),
        None,
    )
    if barcos is not None and barco_impactado is None:
        raise ValueError("El tablero marca un barco que no está registrado.")

    tablero[fila, columna] = TOCADO
    if barco_impactado is not None:
        barco_impactado.impactos.add((fila, columna))
        if barco_impactado.hundido:
            return "hundido"
    return "tocado"


def elegir_disparo_aleatorio(tablero_disparos: np.ndarray) -> Coordenada:
    """Elige al azar una casilla que todavía no haya recibido disparos."""
    pendientes = [
        (fila, columna)
        for fila in range(tablero_disparos.shape[0])
        for columna in range(tablero_disparos.shape[1])
        if tablero_disparos[fila, columna] == AGUA
    ]
    if not pendientes:
        raise ValueError("No quedan casillas disponibles para disparar.")
    return random.choice(pendientes)


def mostrar_tablero(tablero: np.ndarray, ocultar_barcos: bool = False) -> None:
    """Imprime el tablero con índices; puede ocultar los barcos intactos."""
    filas, columnas = tablero.shape
    print("   " + " ".join(f"{columna:2}" for columna in range(columnas)))
    for fila in range(filas):
        casillas = []
        for columna in range(columnas):
            valor = tablero[fila, columna]
            if ocultar_barcos and valor == BARCO:
                valor = AGUA
            casillas.append(f"{valor:2}")
        print(f"{fila:2} " + " ".join(casillas))
