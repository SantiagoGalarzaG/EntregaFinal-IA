"""
motor_inferencia.py — Motor de inferencia con encadenamiento hacia adelante
Sistema Basado en Conocimiento: Diagnóstico de envíos DIAN / RNDC
Autores: Galarza, Solano — Fundación Universitaria Los Libertadores, 2026
"""

import logging
from base_conocimiento import (
    PREDICADOS_SINTOMA, TIPOS_DOCUMENTO, CONFLICTOS_DIAGNOSTICO,
    PREDICADOS_DIAGNOSTICO, DESCRIPCIONES_REGLAS,
)

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("motor_inferencia")


# ─────────────────────────────────────────────────────────────────────────────
# VALIDACIÓN Y PRE-PROCESAMIENTO
# ─────────────────────────────────────────────────────────────────────────────

def validar_hechos(hechos: list) -> None:
    """
    Valida que los hechos no contengan contradicciones ni tipos de documento
    mutuamente excluyentes. Lanza ValueError si hay problemas.
    """
    vistos = {}
    for pred, valor in hechos:
        if pred in vistos and vistos[pred] != valor:
            raise ValueError(
                f"Contradicción detectada: '{pred}' aparece como True y False al mismo tiempo."
            )
        vistos[pred] = valor

    activos = [t for t in TIPOS_DOCUMENTO if vistos.get(t) is True]
    if len(activos) > 1:
        raise ValueError(
            f"Tipos de documento mutuamente excluyentes seleccionados: {', '.join(activos)}. "
            "Un documento solo puede ser de un tipo a la vez."
        )


def aplicar_cwa(hechos: list) -> list:
    """
    Aplica el Supuesto de Mundo Cerrado (CWA): todo predicado de síntoma
    no mencionado explícitamente se asume False.
    """
    presentes = {h[0] for h in hechos}
    cwa_hechos = [(p, False) for p in PREDICADOS_SINTOMA if p not in presentes]
    logger.info("CWA aplicada: %d predicados completados como False.", len(cwa_hechos))
    return list(hechos) + cwa_hechos


# ─────────────────────────────────────────────────────────────────────────────
# MOTOR DE INFERENCIA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def encadenamiento_adelante(reglas: list, hechos: list) -> tuple:
    """
    Aplica encadenamiento hacia adelante sobre la base de conocimiento.

    Ciclos infinitos: prevenidos porque cada regla se aplica como máximo una vez.
    El bucle termina cuando no hay nuevas conclusiones que derivar.
    Salvaguarda adicional: máximo len(reglas) iteraciones.

    Args:
        reglas: lista de reglas de la base de conocimiento.
        hechos: lista de (predicado, valor) conocidos.

    Returns:
        (hechos_finales, reglas_aplicadas, certezas_derivadas)
    """
    hechos_unicos = list(dict.fromkeys(hechos))
    validar_hechos(hechos_unicos)
    nuevos = aplicar_cwa(hechos_unicos)

    aplicadas: list = []
    certezas: dict = {}
    cambio = True
    iteracion = 0
    max_iter = len(reglas) + 1  # Salvaguarda anti-ciclo

    logger.info("Inicio inferencia. Hechos iniciales: %d", len(hechos_unicos))

    while cambio and iteracion < max_iter:
        cambio = False
        iteracion += 1
        logger.debug("Iteración %d del bucle de inferencia.", iteracion)

        for regla in reglas:
            nombre = regla["nombre"]
            if nombre in aplicadas:
                continue

            if all(c in nuevos for c in regla["condiciones"]):
                aplicadas.append(nombre)
                conclusion = regla["conclusion"]
                certeza_nueva = regla["certeza"]

                if conclusion not in nuevos:
                    nuevos.append(conclusion)
                    certezas[conclusion] = certeza_nueva
                    cambio = True
                    logger.info(
                        "Regla %s disparada → %s=True (certeza: %.0f%%)",
                        nombre, conclusion[0], certeza_nueva * 100,
                    )
                else:
                    # Combinación de certezas: P(A∨B) = 1 − (1−P(A))·(1−P(B))
                    c_prev = certezas.get(conclusion, 0)
                    certezas[conclusion] = round(
                        1 - (1 - c_prev) * (1 - certeza_nueva), 4
                    )
                    logger.debug(
                        "Regla %s: conclusión %s ya existía. Certeza combinada: %.0f%%",
                        nombre, conclusion[0], certezas[conclusion] * 100,
                    )

    if iteracion >= max_iter:
        logger.warning("Se alcanzó el límite de iteraciones (%d). Posible ciclo evitado.", max_iter)

    logger.info(
        "Inferencia completada. Reglas aplicadas: %d. Conclusiones derivadas: %d.",
        len(aplicadas), len(certezas),
    )
    return nuevos, aplicadas, certezas


# ─────────────────────────────────────────────────────────────────────────────
# EXPLICACIÓN DEL RAZONAMIENTO
# ─────────────────────────────────────────────────────────────────────────────

def porque(conclusion: str, reglas: list, reglas_aplicadas: list,
           hechos_finales: list) -> list:
    """
    Explica por qué se llegó a una conclusión específica.

    Args:
        conclusion:       nombre del predicado de diagnóstico (e.g. "DianCaida").
        reglas:           lista completa de reglas de la base de conocimiento.
        reglas_aplicadas: nombres de reglas que se dispararon en la inferencia.
        hechos_finales:   lista de todos los hechos al finalizar la inferencia.

    Returns:
        Lista de dicts con la información de cada regla que derivó la conclusión:
        [{"regla": str, "certeza": float, "descripcion": str,
          "condiciones": [{"predicado": str, "valor_esperado": bool}]}]
    """
    resultados = []
    for regla in reglas:
        if regla["nombre"] not in reglas_aplicadas:
            continue
        if regla["conclusion"][0] != conclusion:
            continue

        condiciones_info = [
            {"predicado": pred, "valor_esperado": val_esp}
            for pred, val_esp in regla["condiciones"]
        ]
        resultados.append({
            "regla":       regla["nombre"],
            "certeza":     regla["certeza"],
            "descripcion": DESCRIPCIONES_REGLAS.get(regla["nombre"], regla["nombre"]),
            "condiciones": condiciones_info,
        })

    logger.debug("porque('%s'): %d regla(s) encontrada(s).", conclusion, len(resultados))
    return resultados


def detectar_conflictos(diagnosticos: list) -> list:
    """
    Detecta diagnósticos mutuamente excluyentes que coexisten.
    Retorna lista de frozensets con los grupos conflictivos presentes.
    """
    nombres = {d[0] for d in diagnosticos if d[1]}
    return [g for g in CONFLICTOS_DIAGNOSTICO if g.issubset(nombres)]


def explicar_razonamiento(hechos_iniciales: list, hechos_finales: list,
                          reglas_aplicadas: list, certezas: dict) -> str:
    """
    Genera un resumen en texto del proceso de inferencia.

    Returns:
        Cadena de texto con el diagnóstico completo.
    """
    lineas = ["=" * 55, "DIAGNÓSTICO DEL SISTEMA", "=" * 55]

    lineas.append("\nHechos ingresados:")
    for pred, val in hechos_iniciales:
        estado = "SÍ" if val else "NO"
        lineas.append(f"  {estado:3}  {pred}")

    lineas.append(f"\nReglas aplicadas ({len(reglas_aplicadas)}):")
    for nombre in reglas_aplicadas:
        desc = DESCRIPCIONES_REGLAS.get(nombre, "")
        lineas.append(f"  [{nombre}] {desc}")

    diagnosticos = [
        h for h in hechos_finales
        if h not in hechos_iniciales and h[1] and h[0] in PREDICADOS_DIAGNOSTICO
    ]
    errores = [d for d in diagnosticos if d[0] not in {"EnvioExitosoRNDC", "CufeGenerado", "TipoXML12", "TipoXML10"}]
    exitos  = [d for d in diagnosticos if d[0] in {"EnvioExitosoRNDC", "CufeGenerado", "TipoXML12", "TipoXML10"}]

    if exitos:
        lineas.append("\nResultados exitosos:")
        for d in exitos:
            cert = certezas.get(d, 1.0)
            lineas.append(f"  ✓  {d[0]}  (certeza: {cert:.0%})")

    lineas.append("\nDiagnósticos de error:")
    if errores:
        for d in errores:
            cert = certezas.get(d, 1.0)
            lineas.append(f"  >>>  {d[0]}  (certeza: {cert:.0%})")
        conflictos = detectar_conflictos(diagnosticos)
        if conflictos:
            lineas.append("\n  ADVERTENCIA — diagnósticos mutuamente excluyentes:")
            for grupo in conflictos:
                lineas.append(f"    {' vs '.join(grupo)}")
    else:
        if not exitos:
            lineas.append("  No se detectaron problemas con los síntomas proporcionados.")
        else:
            lineas.append("  Ningún error detectado.")

    lineas.append("=" * 55)
    return "\n".join(lineas)
