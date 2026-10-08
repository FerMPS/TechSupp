# main.py
# Punto de entrada - Sistema experto conversacional

import sys
from interfaz import InterfazConsola
from motor import MotorConversacional
from explicacion import Explicador


def norm(r: str) -> str:
    if not r:
        return ""
    t = r.lower().strip()
    return t


def main():
    try:
        inter = InterfazConsola()
        mot = MotorConversacional()
        exp = Explicador()

        inter.mostrar_bienvenida()

        while True:
            mot.limpiar()
            desc = inter.pedir_descripcion()
            nd = norm(desc)
            if nd in ("salir", "q", "exit", "fin"):
                print("\nHasta luego. ¡Suerte con la reparación!")
                return
            if nd in ("reiniciar", "r", "reset"):
                continue
            if nd in ("ayuda", "h", "help"):
                inter.mostrar_ayuda()
                continue

            mot.establecer_descripcion(desc)

            while True:
                acc = mot.siguiente_accion()

                if acc["tipo"] == "pedir_descripcion":
                    desc2 = inter.preguntar_abierta(acc["texto"])
                    nd2 = norm(desc2)
                    if nd2 in ("salir", "q"):
                        print("\nHasta luego. ¡Suerte con la reparación!")
                        return
                    if nd2 in ("reiniciar", "r"):
                        break
                    if nd2 in ("ayuda", "h"):
                        inter.mostrar_ayuda()
                        continue
                    mot.establecer_descripcion(desc2)
                    inter.mostrar_resumen_hechos(mot.estado.get("hechos", {}))
                    continue

                if acc["tipo"] == "preguntar_minima":
                    preguntas = acc.get("preguntas", [])
                    # Hacer solo la primera pregunta mínima para no abrumar
                    if preguntas:
                        p = preguntas[0]
                        r = inter.preguntar_abierta(p["texto"])
                        nr = norm(r)
                        if nr in ("salir", "q"):
                            print("\nHasta luego. ¡Suerte con la reparación!")
                            return
                        if nr in ("reiniciar", "r"):
                            break
                        if nr in ("ayuda", "h"):
                            inter.mostrar_ayuda()
                            continue
                        # Si es respuesta abierta distinta a comandos, intentar extraer
                        if nr in ("si", "s", "sí", "y"):
                            mot.establecer_hecho(p["id"], "si")
                        elif nr in ("no", "n"):
                            mot.establecer_hecho(p["id"], "no")
                        elif nr in ("no_sabe", "ns", "nose", "no se"):
                            mot.establecer_hecho(p["id"], "no_sabe")
                        else:
                            mot.establecer_descripcion(r)
                    inter.mostrar_resumen_hechos(mot.estado.get("hechos", {}))
                    continue

                if acc["tipo"] == "preguntar":
                    pid = acc.get("pregunta_id")
                    texto_p = acc.get("texto", "Cuéntame más...")
                    r = inter.preguntar_abierta(texto_p)
                    nr = norm(r)
                    if nr in ("salir", "q"):
                        print("\nHasta luego. ¡Suerte con la reparación!")
                        return
                    if nr in ("reiniciar", "r"):
                        break
                    if nr in ("ayuda", "h"):
                        inter.mostrar_ayuda()
                        continue
                    if nr in ("si", "s", "sí", "y"):
                        mot.establecer_hecho(pid, "si")
                    elif nr in ("no", "n"):
                        mot.establecer_hecho(pid, "no")
                    elif nr in ("no_sabe", "ns", "nose", "no se"):
                        mot.establecer_hecho(pid, "no_sabe")
                    else:
                        mot.establecer_descripcion(r)
                    inter.mostrar_resumen_hechos(mot.estado.get("hechos", {}))
                    continue

                if acc["tipo"] == "diagnostico":
                    inter.mostrar_diagnostico(
                        acc.get("hipotesis"),
                        acc.get("plan", {}),
                        mot.estado.get("hechos", {}),
                    )
                    print(exp.explicar(mot.estado, acc.get("plan", {})))
                    op = inter.preguntar_continuar()
                    nop = norm(op)
                    if nop in ("salir", "q"):
                        print("\nHasta luego. ¡Suerte con la reparación!")
                        return
                    if nop in ("reiniciar", "r"):
                        break
                    if nop in ("seguir", "s"):
                        print("\n[ASISTENTE] Sigue con el siguiente paso que aún no hayas probado.")
                        print("Cuando avances, dime: 'probé paso X: sí funcionó / no funcionó / ya lo hice'")
                        s = inter.preguntar_abierta("¿Qué me dices ahora?")
                        ns = norm(s)
                        if ns in ("salir", "q"):
                            return
                        if ns in ("reiniciar", "r"):
                            break
                        mot.establecer_descripcion(s)
                        continue
                    # Si responde con descripción de lo probado
                    mot.establecer_descripcion(op)
                    continue

            # Fin bucle interno
            continue

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Verifica que existe 'conocimiento/reglas.json'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()