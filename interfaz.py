# interfaz.py
# Interfaz conversacional por consola

class InterfazConsola:
    def mostrar_bienvenida(self) -> None:
        print("=" * 72)
        print("ASISTENTE CONVERSACIONAL DE SOPORTE TÉCNICO")
        print("Diagnóstico guiado paso a paso • Laptops y PCs • Solo consola")
        print("=" * 72)
        print("Habla con naturalidad. Puedes responder en tus propias palabras.")
        print("También acepta: si | no | no_sabe")
        print("Comandos: salir | reiniciar | ayuda")
        print("=" * 72 + "\n")

    def mostrar_ayuda(self) -> None:
        print("\n--- COMANDOS ---")
        print("salir / q   -> Salir")
        print("reiniciar/r -> Empezar de nuevo")
        print("ayuda / h   -> Mostrar ayuda")
        print("si / no / no_sabe también válidos")
        print("----------------\n")

    def pedir_descripcion(self) -> str:
        print("[ASISTENTE] Vamos paso a paso.")
        print("Describe el problema que tienes ahora mismo (qué ocurre, cuándo empezó, síntomas):")
        try:
            resp = input("> ").strip()
            return resp
        except (EOFError, KeyboardInterrupt):
            return "salir"

    def preguntar_abierta(self, texto: str) -> str:
        print(f"\n[ASISTENTE] {texto}")
        try:
            resp = input("> ").strip()
            return resp
        except (EOFError, KeyboardInterrupt):
            return "salir"

    def mostrar_resumen_hechos(self, hechos: dict) -> None:
        if not hechos:
            return
        print("\n[RESUMEN HASTA AHORA]")
        mapa = {
            "es_laptop": "Portátil",
            "es_pc": "PC",
            "enciende": "Enciende",
            "tiene_imagen": "Hay imagen",
            "se_ve_logo_bios": "Llega a logo/BIOS",
            "llega_a_so": "Llega a SO",
            "aparece_bsod": "BSOD",
            "calienta": "Se calienta",
            "hay_ruidos": "Hay ruidos",
            "sospecha_disco": "Sospecha disco",
            "lento": "Lento",
            "problema_wifi": "WiFi",
            "problema_audio": "Audio",
            "carga_bateria": "Carga batería",
            "conectado_a_corriente": "Conectado a corriente",
            "encienden_leds": "LEDs",
            "gira_ventilador": "Ventilador",
            "arranca_so": "Arranca SO",
        }
        for k, v in hechos.items():
            if k in mapa:
                print(f"  • {mapa[k]}: {v}")
        print()

    def mostrar_diagnostico(self, hip: str, plan: dict, hechos: dict) -> None:
        print("\n" + "=" * 72)
        print("DIAGNÓSTICO ORIENTATIVO + PASOS A SEGUIR")
        print("=" * 72)
        titulo = plan.get("titulo", "Sin título")
        print(f"\nPOSIBLE CAUSA: {titulo}")
        if plan.get("explicacion"):
            print(f"\nEXPLICACIÓN: {plan['explicacion']}")
        pasos = plan.get("pasos", [])
        if pasos:
            print("\nPASOS PRÁCTICOS (en orden):")
            for i, p in enumerate(pasos, 1):
                print(f"  {i}. {p}")
        print("\nRECOMENDACIONES:")
        print("  - Ve probando paso a paso. Cuando avances, dime qué has hecho y si funcionó.")
        print("  - Si no estás seguro, responde 'no_sabe' y seguimos lo esencial.")
        print("  - En caso de ruidos con clics + datos importantes: NO fuerces el uso.")
        print("=" * 72 + "\n")

    def preguntar_continuar(self) -> str:
        print("¿Quieres que siga guiándote, o prefieres describirme qué has probado/qué ha ocurrido?")
        print("(describe / seguir / reiniciar / salir)")
        try:
            return input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            return "salir"