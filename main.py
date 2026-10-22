# main.py
# Punto de entrada - Sistema Experto de Soporte Técnico (modo consola)

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_RELATIVA = os.path.join("conocimiento", "reglas.json")
KB_RUTA = os.path.join(BASE_DIR, KB_RELATIVA)


def main() -> int:
    # Asegurar imports desde el directorio del proyecto
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

    try:
        from interfaz import InterfazConsola
        from motor import MotorConversacional
    except Exception as exc:
        print(f"Error al importar módulos: {exc}")
        return 1

    try:
        motor = MotorConversacional(ruta_kb=KB_RUTA)
    except FileNotFoundError as exc:
        print("No se encontró la base de conocimiento.")
        print(f"Detalle: {exc}")
        print(f"Comprueba que existe: {KB_RELATIVA}")
        return 1
    except Exception as exc:
        print(f"Error al inicializar el motor: {exc}")
        return 1

    ui = InterfazConsola()
    ui.ejecutar(motor)
    return 0


if __name__ == "__main__":
    sys.exit(main())
