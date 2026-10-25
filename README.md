# Hundir la flota

Una versión de terminal del juego Hundir la flota, desarrollada en Python. Juegas contra una máquina que dispara a casillas aleatorias de tu tablero.

## Requisitos

- Python 3.10 o posterior.
- NumPy, instalado con `requirements.txt`.

## Instalación

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python -m venv .venv
```

Activa el entorno virtual:

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS o Linux:**

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Cómo jugar

Inicia el juego desde la carpeta que contiene `main.py`:

```bash
python main.py
```

Introduce tu nombre y luego dispara escribiendo una fila y una columna separadas por una coma, por ejemplo:

```text
5,0
```

También se acepta el formato `(5,0)`. Las filas y columnas empiezan en `0`, así que en un tablero de 10 × 10 los índices válidos van de `0` a `9`. Si la entrada no es válida o la casilla ya recibió un disparo, el juego explicará el error y permitirá intentarlo de nuevo.

La flota de cada jugador tiene seis barcos: tres de eslora 2, dos de eslora 3 y uno de eslora 4. Los barcos se colocan aleatoriamente al inicio. Gana quien hunda todos los barcos del oponente.

En los tableros, `O` representa un barco, `X` un impacto y `-` un disparo al agua. La máquina elige sus disparos al azar y no repite casillas.

## Estructura del proyecto

- `main.py`: inicia la partida, gestiona los turnos y muestra la interacción por terminal.
- `clases.py`: define los modelos `Barco`, `Jugador` y `Partida`.
- `funciones.py`: implementa la creación de tableros, colocación de barcos, disparos y visualización.
- `requirements.txt`: lista las dependencias externas del proyecto.
