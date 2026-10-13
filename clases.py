from dataclasses import dataclass, field

import numpy as np


Coordenada = tuple[int, int]


@dataclass
class Barco:
    eslora: int
    posiciones: list[Coordenada]
    impactos: set[Coordenada] = field(default_factory=set)

    @property
    def hundido(self) -> bool:
        return bool(self.posiciones) and all(
            posicion in self.impactos for posicion in self.posiciones
        )


@dataclass
class Jugador:
    nombre: str
    tablero: np.ndarray
    barcos: list[Barco]
    es_maquina: bool = False
    tablero_disparos: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        self.tablero_disparos = np.full(self.tablero.shape, " ", dtype="<U1")


@dataclass
class Partida:
    jugadores: list[Jugador]
    indice_turno: int = 0

    def __post_init__(self) -> None:
        if len(self.jugadores) != 2:
            raise ValueError("La partida necesita exactamente dos jugadores.")
        if self.jugadores[0].es_maquina == self.jugadores[1].es_maquina:
            raise ValueError("La partida necesita un jugador y una máquina.")

    @property
    def jugador_actual(self) -> Jugador:
        return self.jugadores[self.indice_turno]

    @property
    def oponente(self) -> Jugador:
        return self.jugadores[1 - self.indice_turno]

    @property
    def ganador(self) -> Jugador | None:
        if all(barco.hundido for barco in self.oponente.barcos):
            return self.jugador_actual
        if all(barco.hundido for barco in self.jugador_actual.barcos):
            return self.oponente
        return None

    @property
    def terminada(self) -> bool:
        return self.ganador is not None

    def cambiar_turno(self) -> None:
        self.indice_turno = 1 - self.indice_turno
