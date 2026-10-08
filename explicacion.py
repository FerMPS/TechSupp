# explicacion.py
# Explicación del razonamiento conversacional

class Explicador:
    def explicar(self, estado: dict, plan: dict) -> str:
        lineas = []
        lineas.append("\nEXPLICACIÓN DEL RAZONAMIENTO")
        lineas.append("-" * 50)
        desc = estado.get("descripcion") or "(No proporcionada)"
        lineas.append(f"Descripción inicial: {desc}")
        hip = estado.get("hipotesis_activa") or "(Sin hipótesis activa)"
        lineas.append(f"Hipótesis activa: {hip}")
        hechos = estado.get("hechos", {}) or {}
        if hechos:
            lineas.append("Hechos inferidos/confirmados:")
            for k, v in hechos.items():
                lineas.append(f"  - {k}: {v}")
        else:
            lineas.append("Hechos: (Ninguno confirmado aún)")
        if plan:
            lineas.append(f"Causa orientativa: {plan.get('titulo', '')}")
            exp = plan.get("explicacion") or "Basado en coincidencia de síntomas + preguntas mínimas."
            lineas.append(f"Justificación: {exp}")
        lineas.append("-" * 50)
        return "\n".join(lineas)