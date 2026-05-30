"""
base_conocimiento.py — Predicados, reglas y descripciones del dominio
Sistema Basado en Conocimiento: Diagnóstico de envíos DIAN / RNDC
Autores: Galarza, Solano — Fundación Universitaria Los Libertadores, 2026
"""

# ─────────────────────────────────────────────────────────────────────────────
# PREDICADOS DEL DOMINIO
# Cada predicado es unario con rango {True, False}
# ─────────────────────────────────────────────────────────────────────────────

PREDICADOS = {
    # Clasificación del documento
    "Documento":            "x es un documento electrónico enviado al sistema",
    "Factura":              "x es una factura electrónica",
    "NotaCredito":          "x es una nota crédito electrónica",
    "Remesa":               "x es una remesa de transporte",
    "Manifiesto":           "x es un manifiesto de carga",
    # Destino del envío
    "EnvioDian":            "El documento x se está enviando a la DIAN",
    "EnvioRNDC":            "El documento x se está enviando al RNDC",
    # Validez de entidades
    "TerceroOk":            "Los datos del tercero involucrado en x son correctos",
    "PropietarioOk":        "Los datos del propietario del vehículo en x son correctos",
    "ClienteOk":            "Los datos del cliente en x son correctos",
    "DestinatarioOk":       "Los datos del destinatario en x son correctos",
    "RemitenteOk":          "Los datos del remitente en x son correctos",
    "VehiculoOk":           "Los datos del vehículo en x son correctos",
    "FacturableOk":         "Los datos del facturable (NIT, razón social, CIIU) en x son correctos",
    # Condiciones DIAN
    "CertificadoVigente":   "El certificado digital para firmar x está vigente",
    "ResolucionVigente":    "La resolución de numeración DIAN para x está vigente",
    "NumeroEnRango":        "El número del documento x está dentro del rango autorizado",
    # Estado técnico del envío
    "ErrorConexion":        "Se presentó error de conexión al intentar enviar x",
    "TimeoutEnvio":         "El envío de x superó el tiempo de espera sin respuesta",
    "FallaSOAP":            "El servicio externo devolvió una falla SOAP al enviar x",
    "DocumentoDuplicado":   "x ya había sido enviado anteriormente al sistema externo",
    "DocumentoRechazado":   "El sistema externo rechazó explícitamente el documento x",
    # Conectividad
    "TieneInternet":        "El equipo tiene conexión activa a internet al momento del envío de x",
    # Condiciones RNDC — remesa
    "CoordenadasCoherentes":"Las coordenadas GPS del destino de x son coherentes con la ciudad",
    "DestinoExisteRNDC":    "El municipio de destino de x existe en el catálogo oficial del RNDC",
    # Condiciones nota crédito
    "FacturaAceptadaCliente":"La factura asociada a x ya fue aceptada por el cliente",
    # Condiciones Factura/NC → RNDC
    "DocumentoTipo12":      "x es un documento de tipo 12 (transporte) según el XML generado",
    "FacturableConsistente":"Los datos del facturable en el XML de x coinciden con los de la remesa",
}

# Predicados que son síntomas de entrada (observables por el usuario)
PREDICADOS_SINTOMA = set(PREDICADOS.keys())

# Tipos de documento — mutuamente excluyentes
TIPOS_DOCUMENTO = {"Factura", "NotaCredito", "Remesa", "Manifiesto"}

# ─────────────────────────────────────────────────────────────────────────────
# DIAGNÓSTICOS POSIBLES
# ─────────────────────────────────────────────────────────────────────────────

PREDICADOS_DIAGNOSTICO = {
    "DianCaida", "RndcCaida", "ErrorAPI", "ErrorCertificado",
    "ErrorResolucionNumeracion", "ErrorNumeroFueraRango", "DocumentoYaProcesado",
    "ProblemaInternet", "TerceroMalDiligenciado", "PropietarioMalDiligenciado",
    "ClienteMalDiligenciado", "DestinatarioMalDiligenciado", "VehiculoMalDiligenciado",
    "FacturableMalDiligenciado", "ErrorCoordenadasRemesa", "DestinoNoExisteRNDC",
    "ErrorFacturaYaAceptada", "ErrorDocumentoNoTipo12", "ErrorFacturableInconsistente",
    "EnvioExitosoRNDC", "CufeGenerado", "TipoXML12", "TipoXML10",
}

EXITOS = {"EnvioExitosoRNDC", "CufeGenerado", "TipoXML12", "TipoXML10"}

# ─────────────────────────────────────────────────────────────────────────────
# PARES DE DIAGNÓSTICOS MUTUAMENTE EXCLUYENTES
# ─────────────────────────────────────────────────────────────────────────────

CONFLICTOS_DIAGNOSTICO = [
    frozenset({"DianCaida",        "DocumentoYaProcesado"}),
    frozenset({"RndcCaida",        "DocumentoYaProcesado"}),
    frozenset({"ProblemaInternet", "DianCaida"}),
    frozenset({"ProblemaInternet", "RndcCaida"}),
    frozenset({"ProblemaInternet", "ErrorAPI"}),
    frozenset({"EnvioExitosoRNDC", "RndcCaida"}),
    frozenset({"EnvioExitosoRNDC", "TerceroMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "PropietarioMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "ClienteMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "VehiculoMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "FacturableMalDiligenciado"}),
    frozenset({"CufeGenerado",     "DianCaida"}),
    frozenset({"CufeGenerado",     "ErrorCertificado"}),
    frozenset({"TipoXML10",        "TipoXML12"}),
]

# ─────────────────────────────────────────────────────────────────────────────
# DESCRIPCIONES DE DIAGNÓSTICOS (título, acción recomendada)
# ─────────────────────────────────────────────────────────────────────────────

DESCRIPCIONES_DIAGNOSTICO = {
    "DianCaida":                   ("La DIAN no está disponible",
                                    "Revise el estado del portal DIAN e intente más tarde. Si persiste, contacte soporte."),
    "RndcCaida":                   ("El RNDC no está disponible — falla SOAP",
                                    "El servicio RNDC está caído. Reintente en unos minutos o contacte soporte técnico."),
    "ErrorAPI":                    ("Error en la integración con la API",
                                    "Verifique la configuración del conector con el servicio externo."),
    "ErrorCertificado":            ("El certificado digital no está vigente",
                                    "Renueve el certificado digital con su entidad certificadora."),
    "ErrorResolucionNumeracion":   ("La resolución de numeración no está vigente",
                                    "Gestione ante la DIAN la renovación de la resolución de facturación."),
    "ErrorNumeroFueraRango":       ("El número de documento está fuera del rango autorizado",
                                    "Revise la numeración en el sistema; el número supera el rango autorizado."),
    "DocumentoYaProcesado":        ("Este documento ya fue registrado previamente",
                                    "No es necesario reenviarlo. Verifique en el historial de envíos."),
    "ProblemaInternet":            ("Sin conexión a internet",
                                    "Verifique la conexión de red del equipo o contacte el área de TI."),
    "TerceroMalDiligenciado":      ("Datos del tercero incorrectos o incompletos",
                                    "Revise y corrija NIT, razón social y datos del tercero en el sistema."),
    "PropietarioMalDiligenciado":  ("Datos del propietario del vehículo incorrectos",
                                    "Verifique NIT, nombre y documentos del propietario en el sistema."),
    "ClienteMalDiligenciado":      ("Datos del cliente incorrectos o incompletos",
                                    "Revise NIT, razón social y dirección del cliente en el sistema."),
    "DestinatarioMalDiligenciado": ("Datos del destinatario incorrectos",
                                    "Corrija la información del destinatario en el documento."),
    "VehiculoMalDiligenciado":     ("Datos del vehículo incorrectos o incompletos",
                                    "Verifique placa, SOAT, cilindraje y demás datos del vehículo."),
    "FacturableMalDiligenciado":   ("Datos del facturable incorrectos o incompletos",
                                    "Revise NIT, razón social, dirección y código CIIU del facturado."),
    "ErrorCoordenadasRemesa":      ("Coordenadas incoherentes con la ciudad de destino",
                                    "Las coordenadas GPS no corresponden al municipio de origen/destino."),
    "DestinoNoExisteRNDC":         ("El municipio de destino no existe en el catálogo del RNDC",
                                    "Verifique que el municipio esté correctamente escrito según el catálogo oficial."),
    "ErrorFacturaYaAceptada":      ("La factura ya fue aceptada — no se puede anular",
                                    "Una vez aceptada por el cliente, no es posible emitir nota crédito sobre ella."),
    "ErrorDocumentoNoTipo12":      ("El documento no es de tipo 12 (transporte)",
                                    "Solo documentos tipo 12 pueden enviarse por este flujo al RNDC."),
    "ErrorFacturableInconsistente":("Los datos del facturable en el XML no coinciden con la remesa",
                                    "El XML contiene datos distintos a los de la remesa. Revise la configuración."),
    "EnvioExitosoRNDC":            ("✅ Envío al RNDC exitoso",
                                    "El RNDC aceptó el manifiesto y generó el número de autorización."),
    "CufeGenerado":                ("✅ CUFE generado — envío a la DIAN exitoso",
                                    "La DIAN procesó el documento y generó el Código Único de Factura Electrónica."),
    "TipoXML12":                   ("✅ XML tipo 12 generado (transporte)",
                                    "La DIAN respondió con XML tipo 12 — documento de transporte procesado."),
    "TipoXML10":                   ("✅ XML tipo 10 generado (otros conceptos)",
                                    "La DIAN respondió con XML tipo 10 — documento procesado correctamente."),
}

# ─────────────────────────────────────────────────────────────────────────────
# DESCRIPCIONES DE REGLAS
# ─────────────────────────────────────────────────────────────────────────────

DESCRIPCIONES_REGLAS = {
    "R1a":  "Factura a DIAN con todo correcto pero rechazada → DIAN caída",
    "R1b":  "Nota crédito a DIAN con todo correcto pero rechazada → DIAN caída",
    "R2a":  "Manifiesto al RNDC con falla SOAP → RNDC caído",
    "R2b":  "Remesa al RNDC con falla SOAP → RNDC caído",
    "R3a":  "Error de conexión enviando a DIAN con internet activo → Error API",
    "R3b":  "Error de conexión enviando a RNDC con internet activo → Error API",
    "R7a":  "Envío a DIAN sin internet → Problema de conectividad",
    "R7b":  "Envío a RNDC sin internet → Problema de conectividad",
    "R4a":  "Factura a DIAN con certificado no vigente → Error certificado",
    "R4b":  "Nota crédito a DIAN con certificado no vigente → Error certificado",
    "R5a":  "Factura a DIAN con resolución de numeración vencida → Error resolución",
    "R5b":  "Factura a DIAN con número fuera del rango → Error número fuera de rango",
    "R6":   "Documento duplicado → Ya procesado anteriormente",
    "R10a": "Manifiesto al RNDC: tercero con datos incorrectos",
    "R10b": "Manifiesto al RNDC: propietario con datos incorrectos",
    "R10c": "Manifiesto al RNDC: cliente con datos incorrectos",
    "R10d": "Manifiesto al RNDC: vehículo con datos incorrectos",
    "R10e": "Manifiesto al RNDC: facturable con datos incorrectos",
    "R11a": "Remesa al RNDC: tercero con datos incorrectos",
    "R11b": "Remesa al RNDC: destinatario con datos incorrectos",
    "R11c": "Remesa al RNDC: destino no existe en el catálogo",
    "R11d": "Remesa al RNDC: coordenadas incoherentes con la ciudad",
    "R12":  "Factura a DIAN: facturable con datos incorrectos",
    "R13a": "Nota crédito a DIAN: facturable con datos incorrectos",
    "R13b": "Nota crédito a DIAN: factura ya aceptada por el cliente",
    "R14a": "Factura al RNDC que no es tipo 12",
    "R14b": "Nota crédito al RNDC que no es tipo 12",
    "R14c": "Factura tipo 12 al RNDC con facturable inconsistente",
    "R14d": "Nota crédito tipo 12 al RNDC con facturable inconsistente",
    "R15":  "Manifiesto al RNDC con todas las entidades correctas → Envío exitoso",
    "R16a": "Factura a DIAN con todo correcto → CUFE generado",
    "R16b": "Nota crédito a DIAN con todo correcto → CUFE generado",
    "R17a": "Factura con CUFE y tipo 12 → XML tipo 12",
    "R17b": "Factura con CUFE sin tipo 12 → XML tipo 10",
    "R17c": "Nota crédito con CUFE y tipo 12 → XML tipo 12",
    "R17d": "Nota crédito con CUFE sin tipo 12 → XML tipo 10",
}


# ─────────────────────────────────────────────────────────────────────────────
# CONSTRUCCIÓN DE LA BASE DE CONOCIMIENTO
# ─────────────────────────────────────────────────────────────────────────────

def _r(nombre, condiciones, conclusion, certeza=1.0):
    """Constructor de regla de producción."""
    return {
        "nombre":     nombre,
        "condiciones": condiciones,   # lista de (predicado, valor_esperado)
        "conclusion": conclusion,     # (predicado, valor)
        "certeza":    certeza,        # factor de certeza [0, 1]
    }


def crear_base_conocimiento():
    """
    Retorna la lista completa de 35 reglas de producción del dominio DIAN/RNDC.

    Organización:
        Grupo A — Conectividad y disponibilidad del servicio  (R1a-R7b)
        Grupo B — Certificado digital                         (R4a-R4b)
        Grupo C — Numeración DIAN                             (R5a-R5b)
        Grupo D — Documento duplicado                         (R6)
        Grupo E — Errores de entidades en Manifiesto → RNDC   (R10a-R10e)
        Grupo F — Errores en Remesa → RNDC                    (R11a-R11d)
        Grupo G — Errores en Factura → DIAN                   (R12)
        Grupo H — Errores en Nota crédito → DIAN              (R13a-R13b)
        Grupo I — Factura / NC → RNDC (tipo 12)               (R14a-R14d)
        Grupo J — Casos de éxito                              (R15-R17d)
    """
    return [
        # ── Grupo A — Conectividad ──────────────────────────────────────────
        # R1a: Factura correcta pero rechazada sin falla técnica → DIAN caída
        _r("R1a", [
            ("Factura", True), ("EnvioDian", True), ("FacturableOk", True),
            ("ErrorConexion", False), ("TieneInternet", True),
            ("CertificadoVigente", True), ("ResolucionVigente", True),
            ("NumeroEnRango", True), ("DocumentoRechazado", True),
            ("TimeoutEnvio", False), ("FallaSOAP", False),
        ], ("DianCaida", True), 0.90),

        # R1b: Nota crédito correcta pero rechazada → DIAN caída
        _r("R1b", [
            ("NotaCredito", True), ("EnvioDian", True), ("FacturableOk", True),
            ("ErrorConexion", False), ("TieneInternet", True),
            ("CertificadoVigente", True), ("FacturaAceptadaCliente", False),
            ("DocumentoRechazado", True), ("TimeoutEnvio", False), ("FallaSOAP", False),
        ], ("DianCaida", True), 0.90),

        # R2a: Manifiesto al RNDC con falla SOAP → RNDC caído
        _r("R2a", [("Manifiesto", True), ("EnvioRNDC", True), ("FallaSOAP", True)],
           ("RndcCaida", True), 0.98),

        # R2b: Remesa al RNDC con falla SOAP → RNDC caído
        _r("R2b", [("Remesa", True), ("EnvioRNDC", True), ("FallaSOAP", True)],
           ("RndcCaida", True), 0.98),

        # R3a: Error conexión a DIAN con internet activo y sin timeout → Error API
        _r("R3a", [
            ("Documento", True), ("EnvioDian", True),
            ("ErrorConexion", True), ("TieneInternet", True), ("TimeoutEnvio", False),
        ], ("ErrorAPI", True), 0.90),

        # R3b: Error conexión al RNDC con internet activo y sin timeout → Error API
        _r("R3b", [
            ("Documento", True), ("EnvioRNDC", True),
            ("ErrorConexion", True), ("TieneInternet", True), ("TimeoutEnvio", False),
        ], ("ErrorAPI", True), 0.90),

        # R7a: Sin internet intentando enviar a DIAN → Problema de conectividad
        _r("R7a", [("EnvioDian", True), ("TieneInternet", False)],
           ("ProblemaInternet", True), 1.0),

        # R7b: Sin internet intentando enviar al RNDC → Problema de conectividad
        _r("R7b", [("EnvioRNDC", True), ("TieneInternet", False)],
           ("ProblemaInternet", True), 1.0),

        # ── Grupo B — Certificado digital ───────────────────────────────────
        # R4a: Factura a DIAN con certificado no vigente → Error certificado
        _r("R4a", [("Factura", True), ("EnvioDian", True), ("CertificadoVigente", False)],
           ("ErrorCertificado", True), 1.0),

        # R4b: NC a DIAN con certificado no vigente → Error certificado
        _r("R4b", [("NotaCredito", True), ("EnvioDian", True), ("CertificadoVigente", False)],
           ("ErrorCertificado", True), 1.0),

        # ── Grupo C — Numeración DIAN ────────────────────────────────────────
        # R5a: Factura con resolución de numeración no vigente
        _r("R5a", [("Factura", True), ("EnvioDian", True), ("ResolucionVigente", False)],
           ("ErrorResolucionNumeracion", True), 1.0),

        # R5b: Factura con número de documento fuera del rango autorizado
        _r("R5b", [("Factura", True), ("EnvioDian", True), ("NumeroEnRango", False)],
           ("ErrorNumeroFueraRango", True), 1.0),

        # ── Grupo D — Documento duplicado ────────────────────────────────────
        # R6: Documento enviado anteriormente → ya procesado
        _r("R6", [("Documento", True), ("DocumentoDuplicado", True)],
           ("DocumentoYaProcesado", True), 1.0),

        # ── Grupo E — Errores de entidades en Manifiesto → RNDC ─────────────
        _r("R10a", [("Manifiesto", True), ("EnvioRNDC", True), ("TerceroOk", False)],
           ("TerceroMalDiligenciado", True), 1.0),
        _r("R10b", [("Manifiesto", True), ("EnvioRNDC", True), ("PropietarioOk", False)],
           ("PropietarioMalDiligenciado", True), 1.0),
        _r("R10c", [("Manifiesto", True), ("EnvioRNDC", True), ("ClienteOk", False)],
           ("ClienteMalDiligenciado", True), 1.0),
        _r("R10d", [("Manifiesto", True), ("EnvioRNDC", True), ("VehiculoOk", False)],
           ("VehiculoMalDiligenciado", True), 1.0),
        _r("R10e", [("Manifiesto", True), ("EnvioRNDC", True), ("FacturableOk", False)],
           ("FacturableMalDiligenciado", True), 1.0),

        # ── Grupo F — Errores en Remesa → RNDC ──────────────────────────────
        _r("R11a", [("Remesa", True), ("EnvioRNDC", True), ("TerceroOk", False)],
           ("TerceroMalDiligenciado", True), 1.0),
        _r("R11b", [("Remesa", True), ("EnvioRNDC", True), ("DestinatarioOk", False)],
           ("DestinatarioMalDiligenciado", True), 1.0),
        _r("R11c", [("Remesa", True), ("EnvioRNDC", True), ("DestinoExisteRNDC", False)],
           ("DestinoNoExisteRNDC", True), 1.0),
        _r("R11d", [("Remesa", True), ("EnvioRNDC", True), ("CoordenadasCoherentes", False)],
           ("ErrorCoordenadasRemesa", True), 1.0),

        # ── Grupo G — Errores en Factura → DIAN ─────────────────────────────
        _r("R12", [("Factura", True), ("EnvioDian", True), ("FacturableOk", False)],
           ("FacturableMalDiligenciado", True), 1.0),

        # ── Grupo H — Errores en Nota crédito → DIAN ────────────────────────
        _r("R13a", [("NotaCredito", True), ("EnvioDian", True), ("FacturableOk", False)],
           ("FacturableMalDiligenciado", True), 1.0),
        _r("R13b", [("NotaCredito", True), ("EnvioDian", True), ("FacturaAceptadaCliente", True)],
           ("ErrorFacturaYaAceptada", True), 1.0),

        # ── Grupo I — Factura / NC → RNDC (tipo 12) ─────────────────────────
        _r("R14a", [("Factura", True), ("EnvioRNDC", True), ("DocumentoTipo12", False)],
           ("ErrorDocumentoNoTipo12", True), 1.0),
        _r("R14b", [("NotaCredito", True), ("EnvioRNDC", True), ("DocumentoTipo12", False)],
           ("ErrorDocumentoNoTipo12", True), 1.0),
        _r("R14c", [("Factura", True), ("EnvioRNDC", True),
                    ("DocumentoTipo12", True), ("FacturableConsistente", False)],
           ("ErrorFacturableInconsistente", True), 1.0),
        _r("R14d", [("NotaCredito", True), ("EnvioRNDC", True),
                    ("DocumentoTipo12", True), ("FacturableConsistente", False)],
           ("ErrorFacturableInconsistente", True), 1.0),

        # ── Grupo J — Casos de éxito ─────────────────────────────────────────
        # R15: Manifiesto con todas las entidades correctas → RNDC da número de autorización
        _r("R15", [
            ("Manifiesto", True), ("EnvioRNDC", True),
            ("TerceroOk", True), ("FacturableOk", True), ("PropietarioOk", True),
            ("ClienteOk", True), ("DestinatarioOk", True), ("RemitenteOk", True),
            ("VehiculoOk", True), ("TieneInternet", True), ("FallaSOAP", False),
        ], ("EnvioExitosoRNDC", True), 0.98),

        # R16a: Factura a DIAN con todo correcto → DIAN genera CUFE
        _r("R16a", [
            ("Factura", True), ("EnvioDian", True),
            ("CertificadoVigente", True), ("ResolucionVigente", True),
            ("NumeroEnRango", True), ("FacturableOk", True),
        ], ("CufeGenerado", True), 0.98),

        # R16b: NC a DIAN con todo correcto → DIAN genera CUFE
        _r("R16b", [
            ("NotaCredito", True), ("EnvioDian", True),
            ("CertificadoVigente", True), ("FacturableOk", True),
            ("FacturaAceptadaCliente", False),
        ], ("CufeGenerado", True), 0.98),

        # R17a / R17b: Factura con CUFE → XML tipo 12 o tipo 10
        _r("R17a", [("Factura", True), ("CufeGenerado", True), ("DocumentoTipo12", True)],
           ("TipoXML12", True), 1.0),
        _r("R17b", [("Factura", True), ("CufeGenerado", True), ("DocumentoTipo12", False)],
           ("TipoXML10", True), 1.0),

        # R17c / R17d: NC con CUFE → XML tipo 12 o tipo 10
        _r("R17c", [("NotaCredito", True), ("CufeGenerado", True), ("DocumentoTipo12", True)],
           ("TipoXML12", True), 1.0),
        _r("R17d", [("NotaCredito", True), ("CufeGenerado", True), ("DocumentoTipo12", False)],
           ("TipoXML10", True), 1.0),
    ]
