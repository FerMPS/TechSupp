# interfaz.py
# Interfaz conversacional por consola - Modo ventana con Rich

import os
import sys
from typing import Any, Dict, Optional

from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text


class InterfazConsola:
    def __init__(self) -> None:
        self.console = Console()
        self._ancho = 80

    def _mostrar_cabecera(self) -> None:
        titulo = Text("Asistente de Soporte Técnico", style="bold cyan", justify="center")
        subtitulo = Text("Diagnóstico guiado paso a paso • Laptops y PCs • Modo Consola", style="bright_white", justify="center")
        contenido = Text.assemble(titulo, "\n", subtitulo)
        panel = Panel(
            contenido,
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(Align.center(panel))

    def mostrar_bienvenida(self) -> None:
        self.console.clear()
        self._mostrar_cabecera()
        self.console.print()
        info = Panel(
            "[bold bright_white]Bienvenido al sistema experto de soporte técnico[/bold bright_white]\n\n"
            "[green]•[/green] Responde con naturalidad o usa comandos\n"
            "[green]•[/green] Acepta: [bold]si | no | no_sabe[/bold]\n"
            "[green]•[/green] Comandos: [bold]salir | reiniciar | ayuda[/bold]",
            title="[bold cyan]Información[/bold cyan]",
            box=box.ROUNDED,
            border_style="bright_blue",
            padding=(1, 2),
        )
        self.console.print(info)
        self.console.print()

    def mostrar_ayuda(self) -> None:
        tabla = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        tabla.add_column("Comando", style="bold green")
        tabla.add_column("Descripción", style="bright_white")
        tabla.add_row("salir / q", "Salir de la aplicación")
        tabla.add_row("reiniciar / r", "Empezar diagnóstico de nuevo")
        tabla.add_row("ayuda / h", "Mostrar esta ayuda")
        tabla.add_row("si / no / no_sabe", "Respuestas válidas")
        panel = Panel(
            tabla,
            title="[bold cyan]COMANDOS[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(panel)
        self.console.print()

    def _pedir_numero(self, opciones_max: int, prompt_text: str = "Selecciona una opción") -> Optional[int]:
        while True:
            try:
                resp = Prompt.ask(f"[bold cyan]{prompt_text}[/bold cyan]", console=self.console)
                resp = resp.strip().lower()
                if resp in ("salir", "q", "exit"):
                    return -1
                if resp in ("ayuda", "h"):
                    self.mostrar_ayuda()
                    continue
                if resp in ("reiniciar", "r"):
                    return -2
                # Intentar convertir a número
                try:
                    num = int(resp)
                    if 1 <= num <= opciones_max:
                        return num
                    else:
                        self.console.print(f"[bold red]Error:[/bold red] Debes introducir un número entre 1 y {opciones_max}.", style="red")
                        continue
                except ValueError:
                    self.console.print("[bold red]Error:[/bold red] Debes introducir un número válido.", style="red")
                    continue
            except (EOFError, KeyboardInterrupt):
                return -1

    def mostrar_menu_principal(self) -> Optional[int]:
        self.console.clear()
        self._mostrar_cabecera()
        self.console.print()
        
        tabla = Table(show_header=False, box=box.ROUNDED, padding=(0, 2))
        tabla.add_column("Nº", style="bold green", justify="center", width=4)
        tabla.add_column("Opción", style="bold bright_white")
        tabla.add_column("Descripción", style="bright_white")
        
        opciones = [
            ("1", "Iniciar diagnóstico", "Empezar nuevo diagnóstico guiado"),
            ("2", "Ayuda", "Ver comandos disponibles"),
            ("3", "Salir", "Cerrar la aplicación"),
        ]
        
        for num, op, desc in opciones:
            tabla.add_row(num, op, desc)
        
        panel = Panel(
            tabla,
            title="[bold cyan]MENÚ PRINCIPAL[/bold cyan]",
            subtitle="[bright_white]Escribe el número de la opción[/bright_white]",
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(panel)
        self.console.print()
        
        return self._pedir_numero(3, "Opción")

    def mostrar_menu_diagnostico(self) -> Optional[int]:
        self.console.clear()
        self._mostrar_cabecera()
        self.console.print()
        
        tabla = Table(show_header=False, box=box.ROUNDED, padding=(0, 2))
        tabla.add_column("Nº", style="bold green", justify="center", width=4)
        tabla.add_column("Síntoma", style="bold bright_white")
        tabla.add_column("Descripción", style="bright_white")
        
        opciones = [
            ("1", "No enciende", "Sin luces ni respuesta al botón"),
            ("2", "Pantalla negra", "Enciende pero no se ve imagen"),
            ("3", "Va lento", "Tarda mucho o se cuelga"),
            ("4", "WiFi", "Problemas de conexión inalámbrica"),
            ("5", "Otro / General", "Cuéntame el problema con tus palabras"),
            ("6", "Volver al menú principal", "Regresar"),
        ]
        
        for num, op, desc in opciones:
            tabla.add_row(num, op, desc)
        
        panel = Panel(
            tabla,
            title="[bold cyan]DIAGNÓSTICO POR SÍNTOMA[/bold cyan]",
            subtitle="[bright_white]Selecciona el síntoma principal[/bright_white]",
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(panel)
        self.console.print()
        
        return self._pedir_numero(6, "Opción")

    def pedir_descripcion(self) -> str:
        self.console.print()
        panel = Panel(
            "[bold bright_white]Describe el problema que tienes ahora mismo[/bold bright_white]\n\n"
            "¿Qué ocurre? ¿Cuándo empezó? ¿Qué síntomas notas?",
            title="[bold cyan]DESCRIPCIÓN DEL PROBLEMA[/bold cyan]",
            box=box.ROUNDED,
            border_style="bright_blue",
            padding=(1, 2),
        )
        self.console.print(panel)
        try:
            resp = Prompt.ask("[bold cyan]>[/bold cyan]", console=self.console)
            return resp.strip()
        except (EOFError, KeyboardInterrupt):
            return "salir"

    def preguntar_abierta(self, texto: str) -> str:
        self.console.print()
        panel = Panel(
            f"[bold bright_white]{texto}[/bold bright_white]",
            title="[bold cyan]PREGUNTA[/bold cyan]",
            box=box.ROUNDED,
            border_style="bright_blue",
            padding=(1, 2),
        )
        self.console.print(panel)
        try:
            resp = Prompt.ask("[bold cyan]>[/bold cyan]", console=self.console)
            return resp.strip()
        except (EOFError, KeyboardInterrupt):
            return "salir"

    def mostrar_resumen_hechos(self, hechos: dict) -> None:
        if not hechos:
            return
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
        tabla = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
        tabla.add_column("Dato", style="bright_white")
        tabla.add_column("Valor", style="green")
        for k, v in hechos.items():
            if k in mapa:
                tabla.add_row(mapa[k], str(v))
        if tabla.row_count > 0:
            panel = Panel(
                tabla,
                title="[bold cyan]RESUMEN HASTA AHORA[/bold cyan]",
                box=box.ROUNDED,
                border_style="bright_blue",
                padding=(1, 2),
            )
            self.console.print(panel)
            self.console.print()

    def mostrar_diagnostico(self, hip: str, plan: dict, hechos: dict) -> None:
        self.console.print()
        titulo = plan.get("titulo", "Sin título")
        panel_titulo = Panel(
            f"[bold green]{titulo}[/bold green]",
            title="[bold cyan]DIAGNÓSTICO ORIENTATIVO[/bold cyan]",
            box=box.DOUBLE,
            border_style="green",
            padding=(1, 2),
        )
        self.console.print(panel_titulo)
        self.console.print()
        
        if plan.get("explicacion"):
            panel_exp = Panel(
                f"[bright_white]{plan['explicacion']}[/bright_white]",
                title="[bold cyan]EXPLICACIÓN[/bold cyan]",
                box=box.ROUNDED,
                border_style="bright_blue",
                padding=(1, 2),
            )
            self.console.print(panel_exp)
            self.console.print()
        
        pasos = plan.get("pasos", [])
        if pasos:
            tabla = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
            tabla.add_column("Nº", style="bold green", justify="center", width=4)
            tabla.add_column("Paso", style="bright_white")
            for i, p in enumerate(pasos, 1):
                tabla.add_row(str(i), p)
            panel_pasos = Panel(
                tabla,
                title="[bold cyan]PASOS PRÁCTICOS (en orden)[/bold cyan]",
                box=box.ROUNDED,
                border_style="cyan",
                padding=(1, 2),
            )
            self.console.print(panel_pasos)
            self.console.print()
        
        rec_panel = Panel(
            "[bright_white]• Ve probando paso a paso. Dime qué has hecho y si funcionó.\n"
            "• Si no estás seguro, responde [bold]'no_sabe'[/bold] y seguimos lo esencial.\n"
            "• En caso de ruidos con clics + datos importantes: NO fuerces el uso.[/bright_white]",
            title="[bold cyan]RECOMENDACIONES[/bold cyan]",
            box=box.ROUNDED,
            border_style="bright_blue",
            padding=(1, 2),
        )
        self.console.print(rec_panel)
        self.console.print()

    def preguntar_continuar(self) -> str:
        self.console.print()
        panel = Panel(
            "[bold bright_white]¿Qué deseas hacer ahora?[/bold bright_white]",
            title="[bold cyan]CONTINUAR[/bold cyan]",
            box=box.ROUNDED,
            border_style="bright_blue",
            padding=(1, 2),
        )
        self.console.print(panel)
        tabla = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        tabla.add_column("Opción", style="bold green")
        tabla.add_column("Descripción", style="bright_white")
        tabla.add_row("seguir", "Seguir guiándote")
        tabla.add_row("describir", "Describir qué has probado/qué ha ocurrido")
        tabla.add_row("reiniciar", "Empezar de nuevo")
        tabla.add_row("salir", "Salir")
        self.console.print(tabla)
        try:
            resp = Prompt.ask("[bold cyan]>[/bold cyan]", console=self.console)
            return resp.strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "salir"

    def ejecutar(self, motor) -> None:
        while True:
            self.mostrar_bienvenida()
            opcion = self.mostrar_menu_principal()
            if opcion == -1 or opcion == 3:
                self.console.print("\n[bold cyan]¡Hasta luego![/bold cyan]\n")
                break
            elif opcion == 2:
                self.mostrar_ayuda()
                Prompt.ask("\n[bold cyan]Presiona Enter para continuar[/bold cyan]", console=self.console)
                continue
            elif opcion == 1:
                self._ejecutar_diagnostico(motor)
                continue

    def _ejecutar_diagnostico(self, motor) -> None:
        motor.limpiar()
        while True:
            opcion = self.mostrar_menu_diagnostico()
            if opcion == -1:
                return
            elif opcion == -2 or opcion == 6:
                return
            elif opcion == 1:
                motor.establecer_descripcion("no enciende")
                self._flujo_diagnostico(motor)
                return
            elif opcion == 2:
                motor.establecer_descripcion("pantalla negra")
                self._flujo_diagnostico(motor)
                return
            elif opcion == 3:
                motor.establecer_descripcion("va lento")
                self._flujo_diagnostico(motor)
                return
            elif opcion == 4:
                motor.establecer_descripcion("problemas de wifi")
                self._flujo_diagnostico(motor)
                return
            elif opcion == 5:
                desc = self.pedir_descripcion()
                if desc.lower() in ("salir", "q"):
                    return
                if desc.lower() in ("reiniciar", "r"):
                    continue
                motor.establecer_descripcion(desc)
                self._flujo_diagnostico(motor)
                return

    def _flujo_diagnostico(self, motor) -> None:
        while True:
            try:
                accion = motor.siguiente_accion()
            except Exception as exc:
                self.console.print(f"[bold red]Error:[/bold red] {exc}")
                break

            tipo = accion.get("tipo")

            if tipo == "pedir_descripcion":
                desc = self.pedir_descripcion()
                if desc.lower() in ("salir", "q"):
                    break
                if desc.lower() in ("reiniciar", "r"):
                    return
                if desc.lower() in ("ayuda", "h"):
                    self.mostrar_ayuda()
                    continue
                motor.establecer_descripcion(desc)
                continue

            elif tipo == "preguntar" or tipo == "preguntar_minima":
                pregunta_id = accion.get("pregunta_id")
                texto = accion.get("texto", "Cuéntame más.")
                resp = self.preguntar_abierta(texto)
                if resp.lower() in ("salir", "q"):
                    break
                if resp.lower() in ("reiniciar", "r"):
                    return
                if resp.lower() in ("ayuda", "h"):
                    self.mostrar_ayuda()
                    continue
                if pregunta_id:
                    motor.responder_pregunta(pregunta_id, resp, modo="libre")
                else:
                    motor.establecer_descripcion(resp)
                self.mostrar_resumen_hechos(motor.estado.get("hechos", {}))
                continue

            elif tipo == "diagnostico":
                hip = motor.estado.get("hipotesis_activa")
                plan = accion.get("plan", {})
                self.mostrar_diagnostico(hip or "", plan, motor.estado.get("hechos", {}))
                while True:
                    cont = self.preguntar_continuar()
                    if cont in ("salir", "q"):
                        return
                    elif cont in ("reiniciar", "r"):
                        return
                    elif cont in ("seguir", "s"):
                        break
                    elif cont in ("describir", "d"):
                        desc = self.preguntar_abierta("Dime qué has probado y qué ha ocurrido:")
                        if desc.lower() in ("salir", "q"):
                            return
                        if desc.lower() in ("reiniciar", "r"):
                            return
                        motor.registrar_texto_libre(desc)
                        break
                    else:
                        self.console.print("[bold red]Error:[/bold red] Opción no válida. Inténtalo de nuevo.")
                        continue
                continue

            elif tipo == "sin_informacion":
                resp = self.preguntar_abierta(accion.get("texto", "Necesito más información."))
                if resp.lower() in ("salir", "q"):
                    break
                if resp.lower() in ("reiniciar", "r"):
                    return
                if resp.lower() in ("ayuda", "h"):
                    self.mostrar_ayuda()
                    continue
                motor.establecer_descripcion(resp)
                continue
            else:
                break
        return
