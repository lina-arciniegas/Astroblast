# AstroBlast

¡Bienvenido a AstroBlast, un emocionante juego de disparos espacial desarrollado con PyGame! Pilota tu nave a través de un campo de asteroides y oleadas de enemigos alienígenas, ¡intentando conseguir la puntuación más alta posible!

## Características

*   **Nave Jugador Controlable:** Mueve tu nave espacial y dispara proyectiles para defenderte.
*   **Enemigos Variados:** Enfrenta diferentes tipos de naves enemigas con distintos patrones de movimiento y resistencia.
*   **Sistema de Puntuación:** Cada enemigo destruido te otorga puntos. ¡Intenta superar tu récord!
*   **Menú Principal:** Inicia el juego o sal desde una pantalla de inicio intuitiva.
*   **Pantalla de Game Over:** Visualiza tu puntuación final y decide si quieres volver a intentarlo.
*   **Gráficos y Sonidos Simples:** Disfruta de una experiencia de juego básica pero funcional con efectos visuales y de audio.

## Cómo Jugar

1.  **Clonar el repositorio:** `git clone [URL_DEL_REPOSITORIO]`
2.  **Instalar Pygame:** `pip install pygame`
3.  **Ejecutar el juego:** `python main.py` o `py main.py`

**Nota:** Si tienes problema al ejecutarlo, asegúrate de verifficar la ruta del proyecto, ejecuta el comando `py -m pip install pygame` y vuelve a ingresar el comando de ejecutarlo.

### Controles

*   **Flechas Izquierda/Derecha o A/D:** Mover la nave del jugador horizontalmente.
*   **Barra Espaciadora:** Disparar proyectiles.

## Estructura del Proyecto

*   `main.py`: El archivo principal del juego que contiene el bucle principal y maneja el flujo del juego.
*   `settings.py`: Almacena todas las constantes del juego, como dimensiones de pantalla, velocidades y colores.
*   `sprites.py`: Define las clases para los objetos del juego (jugador, enemigos, proyectiles).
*   `game_functions.py`: Contiene funciones auxiliares para la lógica del juego, como el manejo de eventos, actualización de elementos y dibujo en pantalla.
*   `assets/`: Carpeta para imágenes (nave, enemigos, proyectiles, fondo) y sonidos (disparo, explosión, música).

## Créditos

*   Desarrollado como un proyecto práctico de PyGame.