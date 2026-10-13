from clases import Jugador, Partida
from funciones import (
    FLOTA,
    colocar_barcos,
    crear_tablero,
    disparar,
    elegir_disparo_aleatorio,
    mostrar_tablero,
)


TAMANO_TABLERO = 10
MENSAJES_HUMANO = {
    "agua": "*** MISS: WATER ***",
    "tocado": "*** HIT: YOU HIT A BOAT ***",
    "hundido": "*** SUNK: YOU SUNK A BOAT ***",
}
MENSAJES_MAQUINA = {
    "agua": "*** COMPUTER MISS: WATER ***",
    "tocado": "*** COMPUTER HIT YOUR BOAT ***",
    "hundido": "*** COMPUTER SUNK YOUR BOAT ***",
}


def crear_jugador(nombre: str, es_maquina: bool = False) -> Jugador:
    tablero = crear_tablero(TAMANO_TABLERO)
    barcos = colocar_barcos(tablero)
    return Jugador(
        nombre=nombre,
        tablero=tablero,
        barcos=barcos,
        es_maquina=es_maquina,
    )


def pedir_coordenadas() -> tuple[int, int]:
    try:
        entrada = input("Coordinates (row,column; e.g. 5,0): ").strip()
        if entrada.startswith("(") and entrada.endswith(")"):
            entrada = entrada[1:-1]
        partes = entrada.split(",")
        if len(partes) != 2:
            raise ValueError
        fila, columna = (int(parte.strip()) for parte in partes)
    except ValueError as error:
        raise ValueError("Enter two whole numbers separated by a comma, e.g. 5,0") from error
    return fila, columna


def realizar_disparo(
    atacante: Jugador, objetivo: Jugador, fila: int, columna: int
) -> str:
    resultado = disparar(fila, columna, objetivo.tablero, objetivo.barcos)
    atacante.tablero_disparos[fila, columna] = (
        "-" if resultado == "agua" else "X"
    )
    return resultado


def mostrar_estado(jugador: Jugador) -> None:
    print("\nYour board:")
    mostrar_tablero(jugador.tablero)
    print("\nYour shot history:")
    mostrar_tablero(jugador.tablero_disparos)


def turno_humano(partida: Partida) -> None:
    jugador = partida.jugador_actual
    mostrar_estado(jugador)
    while True:
        try:
            fila, columna = pedir_coordenadas()
            resultado = realizar_disparo(
                jugador, partida.oponente, fila, columna
            )
        except ValueError as error:
            print(f"Invalid shot: {error}. Try again.")
            continue
        print(
            f"\nYOUR SHOT RESULT: row {fila}, column {columna} -> "
            f"{MENSAJES_HUMANO[resultado]}",
            flush=True,
        )
        print("\nYour shot history:", flush=True)
        mostrar_tablero(jugador.tablero_disparos)
        return


def turno_maquina(partida: Partida) -> None:
    maquina = partida.jugador_actual
    print("\nComputer's turn. Choosing a target...", flush=True)
    fila, columna = elegir_disparo_aleatorio(maquina.tablero_disparos)
    resultado = realizar_disparo(maquina, partida.oponente, fila, columna)
    print(
        f"COMPUTER SHOT RESULT: row {fila}, column {columna} -> "
        f"{MENSAJES_MAQUINA[resultado]}",
        flush=True,
    )
    print("\nYour board after the computer's shot:", flush=True)
    mostrar_tablero(partida.oponente.tablero)


def main() -> None:
    nombre = input("Your name: ").strip() or "Player"
    partida = Partida(
        [
            crear_jugador(nombre),
            crear_jugador("Máquina", es_maquina=True),
        ]
    )

    print("\nBattleship!")
    print(f"Each board is {TAMANO_TABLERO}x{TAMANO_TABLERO}.")
    print(f"Fleet: {', '.join(map(str, FLOTA))}.")
    print("O = ship, X = hit, - = missed shot.")

    while not partida.terminada:
        if partida.jugador_actual.es_maquina:
            turno_maquina(partida)
        else:
            print(f"\n{partida.jugador_actual.nombre}'s turn:", flush=True)
            turno_humano(partida)

        if partida.terminada:
            print(f"\n{partida.ganador.nombre} wins!")
            break
        partida.cambiar_turno()


if __name__ == "__main__":
    main()
