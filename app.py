"""
Diagnóstico DIAN / RNDC — Interfaz web Streamlit (v2)
Sistema Basado en Conocimiento — Actividad 4
Autores: Galarza, Solano — Fundación Universitaria Los Libertadores
"""
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# LÓGICA DEL SBC
# ─────────────────────────────────────────────────────────────────────────────

PREDICADOS_SINTOMA = {
    "Documento", "Factura", "NotaCredito", "Remesa", "Manifiesto",
    "EnvioDian", "EnvioRNDC",
    "TerceroOk", "PropietarioOk", "ClienteOk",
    "DestinatarioOk", "RemitenteOk", "VehiculoOk", "FacturableOk",
    "CertificadoVigente", "ResolucionVigente", "NumeroEnRango",
    "ErrorConexion", "TimeoutEnvio", "FallaSOAP",
    "DocumentoDuplicado", "DocumentoRechazado",
    "TieneInternet", "CoordenadasCoherentes", "DestinoExisteRNDC",
    "FacturaAceptadaCliente", "DocumentoTipo12", "FacturableConsistente",
}
TIPOS_DOCUMENTO = {"Factura", "NotaCredito", "Remesa", "Manifiesto"}
CONFLICTOS_DIAGNOSTICO = [
    frozenset({"DianCaida", "DocumentoYaProcesado"}),
    frozenset({"RndcCaida", "DocumentoYaProcesado"}),
    frozenset({"ProblemaInternet", "DianCaida"}),
    frozenset({"ProblemaInternet", "RndcCaida"}),
    frozenset({"ProblemaInternet", "ErrorAPI"}),
    frozenset({"EnvioExitosoRNDC", "RndcCaida"}),
    frozenset({"EnvioExitosoRNDC", "TerceroMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "PropietarioMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "ClienteMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "VehiculoMalDiligenciado"}),
    frozenset({"EnvioExitosoRNDC", "FacturableMalDiligenciado"}),
    frozenset({"CufeGenerado", "DianCaida"}),
    frozenset({"CufeGenerado", "ErrorCertificado"}),
    frozenset({"TipoXML10", "TipoXML12"}),
]
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

DESCRIPCIONES_DIAGNOSTICO = {
    "DianCaida":                   ("La DIAN no está disponible",
                                    "Revise el estado del portal DIAN e intente más tarde. Si persiste, contacte soporte."),
    "RndcCaida":                   ("El RNDC no está disponible — falla SOAP",
                                    "El servicio del RNDC está caído. Reintente en unos minutos o contacte soporte técnico."),
    "ErrorAPI":                    ("Error en la integración con la API",
                                    "Verifique la configuración del conector con el servicio externo en los parámetros del sistema."),
    "ErrorCertificado":            ("El certificado digital no está vigente",
                                    "Renueve el certificado digital con su entidad certificadora antes de volver a enviar."),
    "ErrorResolucionNumeracion":   ("La resolución de numeración no está vigente",
                                    "Gestione ante la DIAN la renovación de la resolución de facturación electrónica."),
    "ErrorNumeroFueraRango":       ("El número de documento está fuera del rango autorizado",
                                    "El número asignado supera el rango de la resolución vigente. Revise la numeración en el sistema."),
    "DocumentoYaProcesado":        ("Este documento ya fue registrado antes",
                                    "No es necesario reenviarlo. Si cree que es un error, verifique en el historial de envíos."),
    "ProblemaInternet":            ("Sin conexión a internet",
                                    "Verifique la conexión del equipo. Si el problema persiste, contacte al área de TI."),
    "TerceroMalDiligenciado":      ("Datos del tercero incorrectos o incompletos",
                                    "Revise y corrija el NIT, razón social y datos del tercero en el maestro del sistema."),
    "PropietarioMalDiligenciado":  ("Datos del propietario del vehículo incorrectos",
                                    "Verifique el NIT, nombre y documentos del propietario registrados en el sistema."),
    "ClienteMalDiligenciado":      ("Datos del cliente incorrectos o incompletos",
                                    "Revise el NIT, razón social, dirección y demás datos del cliente en el sistema."),
    "DestinatarioMalDiligenciado": ("Datos del destinatario incorrectos",
                                    "Corrija la información del destinatario en el documento antes de reenviar."),
    "VehiculoMalDiligenciado":     ("Datos del vehículo incorrectos o incompletos",
                                    "Verifique la placa, SOAT, cilindraje y demás datos del vehículo en el sistema."),
    "FacturableMalDiligenciado":   ("Datos del facturable incorrectos o incompletos",
                                    "Revise el NIT, razón social, dirección y código CIIU del facturado en el sistema."),
    "ErrorCoordenadasRemesa":      ("Coordenadas incoherentes con la ciudad de destino",
                                    "Las coordenadas GPS registradas no corresponden al municipio de origen o destino del viaje."),
    "DestinoNoExisteRNDC":         ("El municipio de destino no existe en el catálogo del RNDC",
                                    "Verifique que el municipio esté correctamente escrito según el catálogo oficial del RNDC."),
    "ErrorFacturaYaAceptada":      ("La factura ya fue aceptada — no se puede anular",
                                    "Una vez aceptada la factura por el cliente, no es posible emitir una nota crédito sobre ella."),
    "ErrorDocumentoNoTipo12":      ("El documento no es de tipo 12 (transporte)",
                                    "Solo documentos de tipo 12 pueden enviarse por este flujo al RNDC. Verifique el tipo de documento."),
    "ErrorFacturableInconsistente":("Los datos del facturable en el XML no coinciden con la remesa",
                                    "El XML generado contiene datos distintos a los de la remesa. Revise la configuración del sistema."),
    "EnvioExitosoRNDC":            ("✅ Envío al RNDC exitoso",
                                    "El RNDC aceptó el manifiesto y generó el número de autorización correctamente."),
    "CufeGenerado":                ("✅ CUFE generado — envío a la DIAN exitoso",
                                    "La DIAN procesó el documento y generó el Código Único de Factura Electrónica (CUFE)."),
    "TipoXML12":                   ("✅ XML tipo 12 generado (transporte)",
                                    "La DIAN respondió con XML tipo 12 — documento de transporte procesado correctamente."),
    "TipoXML10":                   ("✅ XML tipo 10 generado (otros conceptos)",
                                    "La DIAN respondió con XML tipo 10 — documento procesado correctamente."),
}

DESCRIPCIONES_REGLAS = {
    "R1a": "Factura rechazada con todo correcto → DIAN caída",
    "R1b": "Nota crédito rechazada con todo correcto → DIAN caída",
    "R2a": "Manifiesto al RNDC con falla SOAP → RNDC caído",
    "R2b": "Remesa al RNDC con falla SOAP → RNDC caído",
    "R3a": "Error de conexión enviando a DIAN con internet activo → Error API",
    "R3b": "Error de conexión enviando a RNDC con internet activo → Error API",
    "R7a": "Envío a DIAN sin internet → Problema de conectividad",
    "R7b": "Envío a RNDC sin internet → Problema de conectividad",
    "R4a": "Factura a DIAN con certificado no vigente → Error certificado",
    "R4b": "Nota crédito a DIAN con certificado no vigente → Error certificado",
    "R5a": "Factura a DIAN con resolución de numeración vencida → Error resolución",
    "R5b": "Factura a DIAN con número fuera del rango → Error número",
    "R6":  "Documento duplicado → Ya procesado anteriormente",
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
    "R17a": "Factura con CUFE, tipo 12 → XML tipo 12",
    "R17b": "Factura con CUFE, no tipo 12 → XML tipo 10",
    "R17c": "Nota crédito con CUFE, tipo 12 → XML tipo 12",
    "R17d": "Nota crédito con CUFE, no tipo 12 → XML tipo 10",
}


def _r(n, conds, conc, cert=1.0):
    return {"nombre": n, "condiciones": conds, "conclusion": conc, "certeza": cert}


def crear_base_conocimiento():
    return [
        _r("R1a",[("Factura",True),("EnvioDian",True),("FacturableOk",True),("ErrorConexion",False),
                  ("TieneInternet",True),("CertificadoVigente",True),("ResolucionVigente",True),
                  ("NumeroEnRango",True),("DocumentoRechazado",True),("TimeoutEnvio",False),("FallaSOAP",False)],
           ("DianCaida",True),0.90),
        _r("R1b",[("NotaCredito",True),("EnvioDian",True),("FacturableOk",True),("ErrorConexion",False),
                  ("TieneInternet",True),("CertificadoVigente",True),("FacturaAceptadaCliente",False),
                  ("DocumentoRechazado",True),("TimeoutEnvio",False),("FallaSOAP",False)],
           ("DianCaida",True),0.90),
        _r("R2a",[("Manifiesto",True),("EnvioRNDC",True),("FallaSOAP",True)],("RndcCaida",True),0.98),
        _r("R2b",[("Remesa",True),("EnvioRNDC",True),("FallaSOAP",True)],("RndcCaida",True),0.98),
        _r("R3a",[("Documento",True),("EnvioDian",True),("ErrorConexion",True),("TieneInternet",True),
                  ("TimeoutEnvio",False)],("ErrorAPI",True),0.90),
        _r("R3b",[("Documento",True),("EnvioRNDC",True),("ErrorConexion",True),("TieneInternet",True),
                  ("TimeoutEnvio",False)],("ErrorAPI",True),0.90),
        _r("R7a",[("EnvioDian",True),("TieneInternet",False)],("ProblemaInternet",True),1.0),
        _r("R7b",[("EnvioRNDC",True),("TieneInternet",False)],("ProblemaInternet",True),1.0),
        _r("R4a",[("Factura",True),("EnvioDian",True),("CertificadoVigente",False)],("ErrorCertificado",True),1.0),
        _r("R4b",[("NotaCredito",True),("EnvioDian",True),("CertificadoVigente",False)],("ErrorCertificado",True),1.0),
        _r("R5a",[("Factura",True),("EnvioDian",True),("ResolucionVigente",False)],("ErrorResolucionNumeracion",True),1.0),
        _r("R5b",[("Factura",True),("EnvioDian",True),("NumeroEnRango",False)],("ErrorNumeroFueraRango",True),1.0),
        _r("R6",[("Documento",True),("DocumentoDuplicado",True)],("DocumentoYaProcesado",True),1.0),
        _r("R10a",[("Manifiesto",True),("EnvioRNDC",True),("TerceroOk",False)],("TerceroMalDiligenciado",True),1.0),
        _r("R10b",[("Manifiesto",True),("EnvioRNDC",True),("PropietarioOk",False)],("PropietarioMalDiligenciado",True),1.0),
        _r("R10c",[("Manifiesto",True),("EnvioRNDC",True),("ClienteOk",False)],("ClienteMalDiligenciado",True),1.0),
        _r("R10d",[("Manifiesto",True),("EnvioRNDC",True),("VehiculoOk",False)],("VehiculoMalDiligenciado",True),1.0),
        _r("R10e",[("Manifiesto",True),("EnvioRNDC",True),("FacturableOk",False)],("FacturableMalDiligenciado",True),1.0),
        _r("R11a",[("Remesa",True),("EnvioRNDC",True),("TerceroOk",False)],("TerceroMalDiligenciado",True),1.0),
        _r("R11b",[("Remesa",True),("EnvioRNDC",True),("DestinatarioOk",False)],("DestinatarioMalDiligenciado",True),1.0),
        _r("R11c",[("Remesa",True),("EnvioRNDC",True),("DestinoExisteRNDC",False)],("DestinoNoExisteRNDC",True),1.0),
        _r("R11d",[("Remesa",True),("EnvioRNDC",True),("CoordenadasCoherentes",False)],("ErrorCoordenadasRemesa",True),1.0),
        _r("R12",[("Factura",True),("EnvioDian",True),("FacturableOk",False)],("FacturableMalDiligenciado",True),1.0),
        _r("R13a",[("NotaCredito",True),("EnvioDian",True),("FacturableOk",False)],("FacturableMalDiligenciado",True),1.0),
        _r("R13b",[("NotaCredito",True),("EnvioDian",True),("FacturaAceptadaCliente",True)],("ErrorFacturaYaAceptada",True),1.0),
        _r("R14a",[("Factura",True),("EnvioRNDC",True),("DocumentoTipo12",False)],("ErrorDocumentoNoTipo12",True),1.0),
        _r("R14b",[("NotaCredito",True),("EnvioRNDC",True),("DocumentoTipo12",False)],("ErrorDocumentoNoTipo12",True),1.0),
        _r("R14c",[("Factura",True),("EnvioRNDC",True),("DocumentoTipo12",True),("FacturableConsistente",False)],("ErrorFacturableInconsistente",True),1.0),
        _r("R14d",[("NotaCredito",True),("EnvioRNDC",True),("DocumentoTipo12",True),("FacturableConsistente",False)],("ErrorFacturableInconsistente",True),1.0),
        _r("R15",[("Manifiesto",True),("EnvioRNDC",True),("TerceroOk",True),("FacturableOk",True),
                  ("PropietarioOk",True),("ClienteOk",True),("DestinatarioOk",True),("RemitenteOk",True),
                  ("VehiculoOk",True),("TieneInternet",True),("FallaSOAP",False)],
           ("EnvioExitosoRNDC",True),0.98),
        _r("R16a",[("Factura",True),("EnvioDian",True),("CertificadoVigente",True),("ResolucionVigente",True),
                   ("NumeroEnRango",True),("FacturableOk",True)],("CufeGenerado",True),0.98),
        _r("R16b",[("NotaCredito",True),("EnvioDian",True),("CertificadoVigente",True),
                   ("FacturableOk",True),("FacturaAceptadaCliente",False)],("CufeGenerado",True),0.98),
        _r("R17a",[("Factura",True),("CufeGenerado",True),("DocumentoTipo12",True)],("TipoXML12",True),1.0),
        _r("R17b",[("Factura",True),("CufeGenerado",True),("DocumentoTipo12",False)],("TipoXML10",True),1.0),
        _r("R17c",[("NotaCredito",True),("CufeGenerado",True),("DocumentoTipo12",True)],("TipoXML12",True),1.0),
        _r("R17d",[("NotaCredito",True),("CufeGenerado",True),("DocumentoTipo12",False)],("TipoXML10",True),1.0),
    ]


def validar_hechos(hechos):
    vistos = {}
    for p, v in hechos:
        if p in vistos and vistos[p] != v:
            raise ValueError(f"Contradicción: '{p}' está marcado como verdadero y falso al mismo tiempo.")
        vistos[p] = v
    activos = [t for t in TIPOS_DOCUMENTO if vistos.get(t)]
    if len(activos) > 1:
        raise ValueError(f"Solo puede seleccionarse un tipo de documento ({', '.join(activos)}).")


def aplicar_cwa(hechos):
    presentes = {h[0] for h in hechos}
    return list(hechos) + [(p, False) for p in PREDICADOS_SINTOMA if p not in presentes]


def detectar_conflictos(diagnosticos):
    nombres = {d[0] for d in diagnosticos if d[1]}
    return [g for g in CONFLICTOS_DIAGNOSTICO if g.issubset(nombres)]


def encadenamiento_adelante(reglas, hechos):
    unicos = list(dict.fromkeys(hechos))
    validar_hechos(unicos)
    nuevos = aplicar_cwa(unicos)
    aplicadas, certezas, cambio = [], {}, True
    while cambio:
        cambio = False
        for r in reglas:
            if r["nombre"] in aplicadas:
                continue
            if all(c in nuevos for c in r["condiciones"]):
                aplicadas.append(r["nombre"])
                if r["conclusion"] not in nuevos:
                    nuevos.append(r["conclusion"])
                    certezas[r["conclusion"]] = r["certeza"]
                    cambio = True
                else:
                    prev = certezas.get(r["conclusion"], 0)
                    certezas[r["conclusion"]] = round(1-(1-prev)*(1-r["certeza"]), 4)
    return nuevos, aplicadas, certezas


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES UI
# ─────────────────────────────────────────────────────────────────────────────

TIPOS_MAP = {
    "📄  Factura electrónica": "Factura",
    "📝  Nota crédito":        "NotaCredito",
    "🚛  Remesa":              "Remesa",
    "📦  Manifiesto de carga": "Manifiesto",
}

# Ejemplos rápidos — clave: valores de session_state
EJEMPLOS = {
    "🔴  DIAN caída": dict(
        ej_tipo="📄  Factura electrónica", ej_dian=True, ej_rndc=False,
        ej_internet=True, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=True, ej_dup=False, ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "📶  Sin internet": dict(
        ej_tipo="📄  Factura electrónica", ej_dian=True, ej_rndc=False,
        ej_internet=False, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False, ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "🔏  Certificado vencido": dict(
        ej_tipo="📄  Factura electrónica", ej_dian=True, ej_rndc=False,
        ej_internet=True, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False, ej_cert=False, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "✅  Manifiesto exitoso": dict(
        ej_tipo="📦  Manifiesto de carga", ej_dian=False, ej_rndc=True,
        ej_internet=True, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False, ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "🚛  Remesa — tercero inválido": dict(
        ej_tipo="🚛  Remesa", ej_dian=False, ej_rndc=True,
        ej_internet=True, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False, ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=["Tercero"], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "🔁  Documento duplicado": dict(
        ej_tipo="🚛  Remesa", ej_dian=False, ej_rndc=True,
        ej_internet=True, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=True, ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
}

DEFAULT_STATE = dict(
    ej_tipo=None, ej_dian=False, ej_rndc=False,
    ej_internet=True, ej_errorcon=False, ej_timeout=False, ej_soap=False,
    ej_rechazado=False, ej_dup=False, ej_cert=True, ej_resol=True, ej_rango=True,
    ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
    ej_fconsist=True, ej_coord=True, ej_destrndc=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE ESTADO
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def get_reglas():
    return crear_base_conocimiento()


def _init():
    for k, v in DEFAULT_STATE.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "resultado" not in st.session_state:
        st.session_state.resultado = None


def _cargar_ejemplo(nombre):
    for k, v in EJEMPLOS[nombre].items():
        st.session_state[k] = v
    st.session_state.resultado = None


def _reset():
    for k, v in DEFAULT_STATE.items():
        st.session_state[k] = v
    st.session_state.resultado = None


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
<style>
/* ── Globals ── */
[data-testid="stAppViewContainer"] { background: #f1f5f9; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
[data-testid="stSidebar"] { background: #0f172a !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] div:not([data-testid="stExpander"]),
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown p { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: #334155 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #1e3a5f !important; color: #e2e8f0 !important;
    border: 1px solid #334155 !important; border-radius: 8px !important;
    font-size: 0.85rem !important; margin-bottom: 4px !important;
    transition: background 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2563eb !important; border-color: #2563eb !important;
    color: white !important;
}

/* ── Hero header ── */
.hero {
    background: linear-gradient(120deg, #0f172a 0%, #1e3a5f 50%, #1d4ed8 100%);
    padding: 1.6rem 2rem 1.4rem;
    border-radius: 14px;
    margin: 0 0 1.2rem 0;
    box-shadow: 0 6px 24px rgba(15,23,42,0.22);
}
.hero h1        { color: #ffffff !important; font-size: 1.55rem; font-weight: 800; margin: 0 0 0.3rem; letter-spacing: -0.3px; }
.hero p         { color: #93c5fd !important; margin: 0; font-size: 0.87rem; }
.hero span      { color: #bfdbfe !important; }
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #bfdbfe !important; font-size: 0.73rem; font-weight: 600;
    padding: 0.18rem 0.65rem; border-radius: 999px;
    margin-bottom: 0.6rem; letter-spacing: 0.3px;
}

/* ── Step bar ── */
.step-bar {
    display: flex; align-items: center; justify-content: center;
    background: white; border-radius: 14px;
    padding: 0.9rem 1.5rem; margin-bottom: 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    gap: 0;
}
.step-item  { display: flex; flex-direction: column; align-items: center; min-width: 72px; }
.step-num   {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; margin-bottom: 0.25rem;
}
.step-done    { background: #dcfce7; color: #15803d; }
.step-active  { background: #1d4ed8; color: white; box-shadow: 0 0 0 4px #bfdbfe; }
.step-pending { background: #f1f5f9; color: #94a3b8; }
.step-lbl   { font-size: 0.7rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px; }
.step-line  { flex: 1; height: 2px; margin: 0 0.3rem 1.4rem; min-width: 30px; }
.line-done  { background: linear-gradient(90deg, #22c55e, #22c55e); }
.line-active{ background: linear-gradient(90deg, #22c55e, #bfdbfe); }
.line-pend  { background: #e2e8f0; }

/* ── Form sections ── */
.form-section {
    background: white; border-radius: 14px;
    padding: 1.1rem 1.3rem; margin-bottom: 0.8rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    border: 1px solid #f1f5f9;
    transition: box-shadow 0.2s;
}
.form-section:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.09); }
.section-tag {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.6px; color: #64748b; margin-bottom: 0.6rem;
}
.step-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

/* ── Result panel ── */
.res-header {
    background: white; border-radius: 14px;
    padding: 1.1rem 1.3rem; margin-bottom: 0.8rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
}
.res-big-ok  { border-left: 5px solid #22c55e; background: #f0fdf4; }
.res-big-err { border-left: 5px solid #ef4444; background: #fef2f2; }
.res-big-warn{ border-left: 5px solid #f59e0b; background: #fffbeb; }
.res-big-neu { border-left: 5px solid #94a3b8; background: #f8fafc; }

/* ── Diagnosis cards ── */
.dcard {
    border-radius: 12px; padding: 1rem 1.2rem; margin: 0.55rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    animation: fadeUp 0.3s ease;
}
.dcard-ok   { background: #f0fdf4; border-left: 4px solid #22c55e; }
.dcard-err  { background: #fef2f2; border-left: 4px solid #ef4444; }
.dcard-warn { background: #fffbeb; border-left: 4px solid #f59e0b; }

.dcard-title  { font-weight: 700; font-size: 0.96rem; color: #1e293b; margin: 0 0 0.25rem; }
.dcard-desc   { font-size: 0.85rem; color: #475569; margin: 0 0 0.55rem; line-height: 1.5; }
.dcard-action {
    font-size: 0.82rem; color: #1d4ed8;
    background: #eff6ff; padding: 0.3rem 0.65rem;
    border-radius: 6px; display: inline-block;
}
.dcard-action-warn {
    font-size: 0.82rem; color: #92400e;
    background: #fef3c7; padding: 0.3rem 0.65rem;
    border-radius: 6px; display: inline-block;
}

/* ── Confidence badge ── */
.cbadge {
    display: inline-block; font-size: 0.73rem; font-weight: 700;
    padding: 0.12rem 0.55rem; border-radius: 999px; margin-left: 0.5rem;
    vertical-align: middle;
}
.cbadge-high { background: #dcfce7; color: #15803d; }
.cbadge-med  { background: #fef9c3; color: #854d0e; }
.cbadge-low  { background: #fee2e2; color: #991b1b; }

/* ── Summary (before diagnosis) ── */
.summary-wrap {
    background: white; border-radius: 14px;
    padding: 1.6rem; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    border: 2px dashed #e2e8f0;
}
.summary-icon { font-size: 2.8rem; margin-bottom: 0.5rem; }
.summary-row  {
    display: flex; align-items: center; gap: 0.6rem;
    background: #f8fafc; border-radius: 9px;
    padding: 0.55rem 0.9rem; margin: 0.4rem 0;
    font-size: 0.88rem; color: #334155;
    border: 1px solid #e2e8f0;
}
.summary-lbl { font-weight: 600; min-width: 90px; color: #64748b; font-size: 0.8rem; }

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Forzar texto oscuro en todo el contenido principal ── */
[data-testid="stMain"] p,
[data-testid="stMain"] span,
[data-testid="stMain"] label,
[data-testid="stMain"] div,
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] li {
    color: #1e293b;
}
/* Widget labels específicos */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label span,
[data-testid="stRadio"]    label,
[data-testid="stRadio"]    label p,
[data-testid="stRadio"]    label span,
[data-testid="stMultiSelect"] label,
[data-testid="stMultiSelect"] label p,
[data-testid="stMultiSelect"] p,
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
.stCheckbox, .stRadio, .stCaption,
[data-baseweb="checkbox"] ~ div,
[data-baseweb="radio"]    ~ div {
    color: #1e293b !important;
}
/* Caption / hint texts */
[data-testid="stCaptionContainer"] p,
small, .stCaption p { color: #64748b !important; }

/* ── Expanders: fondo blanco y texto oscuro ── */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    overflow: hidden;
    background: #ffffff !important;
}
[data-testid="stExpander"] summary {
    background: #f8fafc !important;
    font-weight: 600;
    color: #1e293b !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary svg {
    color: #1e293b !important;
    fill: #475569 !important;
}
[data-testid="stExpander"] > div {
    background: #ffffff !important;
}
[data-testid="stExpander"] [data-testid="stVerticalBlock"] {
    background: #ffffff !important;
}

/* ── Métricas ── */
[data-testid="stMetricLabel"] p  { color: #64748b !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] div { color: #1e293b !important; font-weight: 700 !important; }

/* ── Hero: override final (máxima precedencia de cascada) ── */
.hero, .hero *, .hero h1, .hero p, .hero span, .hero div {
    color: #ffffff !important;
}
.hero p { color: #93c5fd !important; }
.hero .hero-badge { color: #bfdbfe !important; }

/* ── Step bar: texto siempre visible ── */
.step-lbl { color: #64748b !important; }
.step-done  { color: #15803d !important; }
.step-active { color: #ffffff !important; }
.step-pending { color: #94a3b8 !important; }

/* ── Primary button ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    border: none !important; border-radius: 10px !important;
    font-size: 1rem !important; font-weight: 700 !important;
    padding: 0.7rem 1.2rem !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
    letter-spacing: 0.2px !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Metric cards (st.metric) ── */
[data-testid="metric-container"] {
    background: white; border-radius: 10px;
    padding: 0.8rem 1rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    border: 1px solid #f1f5f9;
}
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# HTML HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _step_bar(step: int) -> str:
    def circle(n, label):
        if n < step:
            cls = "step-done"
            icon = "✓"
        elif n == step:
            cls = "step-active"
            icon = str(n)
        else:
            cls = "step-pending"
            icon = str(n)
        return f"""
        <div class="step-item">
            <div class="step-num {cls}">{icon}</div>
            <div class="step-lbl">{label}</div>
        </div>"""

    def line(n):
        if n < step:
            cls = "line-done"
        elif n == step:
            cls = "line-active"
        else:
            cls = "line-pend"
        return f'<div class="step-line {cls}"></div>'

    steps = [
        (1, "Documento"),
        (2, "Destino"),
        (3, "Síntomas"),
        (4, "Resultado"),
    ]
    html = '<div class="step-bar">'
    for i, (n, label) in enumerate(steps):
        html += circle(n, label)
        if i < len(steps) - 1:
            html += line(n)
    html += "</div>"
    return html


def _badge(cert: float) -> str:
    if cert >= 0.95:
        cls = "cbadge-high"
    elif cert >= 0.80:
        cls = "cbadge-med"
    else:
        cls = "cbadge-low"
    return f'<span class="cbadge {cls}">{cert:.0%}</span>'


def _dcard(kind, titulo, desc, accion, cert):
    action_cls = "dcard-action" if kind in ("ok", "err") else "dcard-action-warn"
    return f"""
    <div class="dcard dcard-{kind}">
        <p class="dcard-title">{titulo} {_badge(cert)}</p>
        <p class="dcard-desc">{desc}</p>
        <span class="{action_cls}">💡 {accion}</span>
    </div>"""


# ─────────────────────────────────────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Diagnóstico DIAN / RNDC",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)
_init()
REGLAS = get_reglas()
st.markdown(CSS, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Diagnóstico DIAN/RNDC")
    st.caption("Sistema Basado en Conocimiento · IA II · Los Libertadores")
    st.divider()

    st.markdown("### ⚡ Ejemplos rápidos")
    st.caption("Cargue un escenario de prueba para explorar el sistema:")
    for nombre in EJEMPLOS:
        if st.button(nombre, use_container_width=True, key=f"btn_{nombre}"):
            _cargar_ejemplo(nombre)
            st.rerun()

    st.divider()
    if st.button("🔄  Reiniciar formulario", use_container_width=True):
        _reset()
        st.rerun()

    st.divider()
    with st.expander("ℹ️  Cómo funciona"):
        st.markdown("""
**Motor de inferencia:**
Encadenamiento hacia adelante con supuesto de mundo cerrado (CWA).

**Certeza:**
Cada regla tiene un factor de certeza. Si varias reglas derivan el mismo diagnóstico, se combina con:
`P(A∨B) = 1 − (1−P(A))·(1−P(B))`

**Reglas:** 35 reglas en 10 grupos.
**Diagnósticos posibles:** 20 tipos.
        """)

    st.divider()
    st.caption("Galarza & Solano · 2026")

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">SISTEMA BASADO EN CONOCIMIENTO · ACTIVIDAD 4</div>
    <h1>🔍 Diagnóstico de Envíos DIAN / RNDC</h1>
    <p>Responda las preguntas paso a paso · El sistema identificará automáticamente la causa del problema</p>
</div>
""", unsafe_allow_html=True)

# ── Calcular paso actual ──────────────────────────────────────────────────────
tipo_label = st.session_state.get("ej_tipo")
env_dian   = st.session_state.get("ej_dian", False)
env_rndc   = st.session_state.get("ej_rndc", False)
tiene_dest = env_dian or env_rndc
tiene_res  = st.session_state.resultado is not None

if not tipo_label:
    paso_actual = 1
elif not tiene_dest:
    paso_actual = 2
elif not tiene_res:
    paso_actual = 3
else:
    paso_actual = 4

st.markdown(_step_bar(paso_actual), unsafe_allow_html=True)

# ── Columnas principales ──────────────────────────────────────────────────────
col_form, col_res = st.columns([1, 1], gap="large")

# ════════════════════════════════════════════════════════════════════════════
# COLUMNA IZQUIERDA — Formulario
# ════════════════════════════════════════════════════════════════════════════
with col_form:

    # ── Paso 1: Tipo de documento ─────────────────────────────────────────────
    st.markdown(
        '<p style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.6px;color:#64748b;margin:0 0 .4rem">🔵 PASO 1 — TIPO DE DOCUMENTO</p>',
        unsafe_allow_html=True,
    )
    idx = list(TIPOS_MAP.keys()).index(tipo_label) if tipo_label in TIPOS_MAP else None
    tipo_label = st.radio(
        "¿Qué tipo de documento estaba enviando?",
        list(TIPOS_MAP.keys()),
        index=idx,
        label_visibility="collapsed",
        help="Seleccione el tipo de documento electrónico que generó el error al enviarse.",
        key="ej_tipo",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    tipo = TIPOS_MAP.get(tipo_label) if tipo_label else None

    if not tipo:
        st.info("👆 Seleccione el tipo de documento para continuar.")
        st.stop()

    # ── Paso 2: Destino ────────────────────────────────────────────────────────
    st.markdown(
        '<p style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.6px;color:#64748b;margin:0 0 .4rem">🟣 PASO 2 — DESTINO DEL ENVÍO</p>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    env_dian = c1.checkbox("🏛️  Enviando a la DIAN", key="ej_dian",
                           help="La DIAN procesa facturas electrónicas y notas crédito.")
    env_rndc = c2.checkbox("🗂️  Enviando al RNDC",  key="ej_rndc",
                           help="El RNDC procesa manifiestos de carga y remesas de transporte.")
    st.markdown("<br>", unsafe_allow_html=True)

    if not env_dian and not env_rndc:
        st.warning("Seleccione al menos un destino para continuar.")
        st.stop()

    # ── Paso 3: Síntomas ───────────────────────────────────────────────────────
    st.markdown(
        '<p style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:.6px;color:#64748b;margin:0 0 .4rem">🔷 PASO 3 — SÍNTOMAS OBSERVADOS</p>',
        unsafe_allow_html=True,
    )

    # 3a · Conectividad
    with st.expander("🌐  Conectividad e internet", expanded=True):
        internet  = st.checkbox("Tiene conexión a internet", key="ej_internet", value=True,
                                help="¿Puede abrir páginas web desde este equipo en este momento?")
        errorcon  = st.checkbox("Hubo error de conexión al servicio", key="ej_errorcon",
                                help="El sistema mostró un mensaje de error al intentar comunicarse con la DIAN o el RNDC.")
        timeout   = st.checkbox("El envío no respondió — venció el tiempo de espera (timeout)", key="ej_timeout",
                                help="El envío se inició pero el servidor no respondió en el tiempo esperado.")
        falla_soap = False
        if env_rndc:
            falla_soap = st.checkbox("El servicio RNDC respondió con una falla SOAP", key="ej_soap",
                                     help="El RNDC devolvió un error de protocolo SOAP, indicando que el servicio puede estar caído.")

    # 3b · Estado del envío
    with st.expander("📬  Estado del envío", expanded=True):
        rechazado = st.checkbox("El servicio rechazó el documento", key="ej_rechazado",
                                help="El servicio externo (DIAN/RNDC) recibió el documento pero lo rechazó explícitamente.")
        duplicado = st.checkbox("Este documento ya había sido enviado antes", key="ej_dup",
                                help="Usted o alguien más ya envió este mismo documento anteriormente y quedó registrado.")

    # 3c · Certificado y numeración (solo DIAN)
    cert_vigente = res_vigente = num_rango = True
    if env_dian and tipo in ("Factura", "NotaCredito"):
        with st.expander("🔏  Certificado y numeración DIAN", expanded=True):
            cert_vigente = st.checkbox("El certificado digital está vigente", key="ej_cert", value=True,
                                       help="El certificado digital usado para firmar el documento no ha expirado.")
            if tipo == "Factura":
                res_vigente = st.checkbox("La resolución de numeración está vigente", key="ej_resol", value=True,
                                          help="La resolución DIAN que autoriza el rango de numeración no ha vencido.")
                num_rango   = st.checkbox("El número del documento está dentro del rango autorizado", key="ej_rango", value=True,
                                          help="El número asignado a la factura cae dentro del rango de la resolución vigente.")

    # 3d · Entidades (multiselect: ¿cuáles tienen problemas?)
    tercero_ok = propietario_ok = cliente_ok = True
    destinatario_ok = remitente_ok = vehiculo_ok = facturable_ok = True

    opciones_entidades: list = []
    if tipo == "Manifiesto" and env_rndc:
        opciones_entidades = ["Tercero", "Propietario del vehículo", "Cliente",
                              "Destinatario", "Remitente", "Vehículo", "Facturable"]
    elif tipo == "Remesa" and env_rndc:
        opciones_entidades = ["Tercero", "Destinatario", "Facturable"]
    elif tipo in ("Factura", "NotaCredito") and env_dian:
        opciones_entidades = ["Facturable", "Tercero"]
    elif tipo in ("Factura", "NotaCredito") and env_rndc:
        opciones_entidades = ["Facturable"]

    if opciones_entidades:
        with st.expander("👥  Datos de entidades", expanded=True):
            st.caption("Seleccione las entidades que tienen datos incorrectos o incompletos en el sistema. "
                       "Si todo está bien, deje vacío.")
            ent_mal = st.multiselect(
                "Entidades con problemas",
                opciones_entidades,
                default=st.session_state.get("ej_ent_mal", []),
                key="ej_ent_mal",
                help="Marque únicamente las entidades cuya información está mal diligenciada.",
                placeholder="Ninguna — todo está correcto",
            )
            tercero_ok      = "Tercero"              not in ent_mal
            propietario_ok  = "Propietario del vehículo" not in ent_mal
            cliente_ok      = "Cliente"              not in ent_mal
            destinatario_ok = "Destinatario"         not in ent_mal
            remitente_ok    = "Remitente"            not in ent_mal
            vehiculo_ok     = "Vehículo"             not in ent_mal
            facturable_ok   = "Facturable"           not in ent_mal

    # 3e · Condiciones especiales
    fact_aceptada = tipo12 = False
    fact_consist = coord_ok = destino_rndc_ok = True

    conds_especiales = any([
        tipo == "NotaCredito" and env_dian,
        tipo in ("Factura", "NotaCredito") and env_rndc,
        tipo == "Remesa" and env_rndc,
    ])
    if conds_especiales:
        with st.expander("🔧  Condiciones especiales", expanded=False):
            if tipo == "NotaCredito" and env_dian:
                fact_aceptada = st.checkbox(
                    "La factura asociada ya fue aceptada por el cliente", key="ej_factaceptada",
                    help="El cliente ya respondió con aceptación a la factura original sobre la que recae esta nota crédito.")
            if tipo in ("Factura", "NotaCredito") and env_rndc:
                tipo12 = st.checkbox(
                    "El documento es de tipo 12 (transporte)", key="ej_tipo12",
                    help="El código de tipo de documento registrado en el XML es 12, correspondiente a documentos de transporte.")
                fact_consist = st.checkbox(
                    "Los datos del facturable en el XML coinciden con la remesa", key="ej_fconsist", value=True,
                    help="Los datos del facturado en el XML generado son idénticos a los registrados en la remesa.")
            if tipo == "Remesa" and env_rndc:
                coord_ok       = st.checkbox("Las coordenadas del destino son coherentes con la ciudad", key="ej_coord", value=True,
                                             help="Las coordenadas GPS registradas corresponden al municipio de origen/destino del viaje.")
                destino_rndc_ok = st.checkbox("El municipio de destino existe en el catálogo del RNDC", key="ej_destrndc", value=True,
                                              help="El municipio de destino está correctamente registrado en el catálogo oficial del RNDC.")

    st.markdown("")

    # ── Botón diagnosticar ────────────────────────────────────────────────────
    if st.button("🔍  Diagnosticar ahora", type="primary", use_container_width=True):

        hechos = [(tipo, True), ("Documento", True)]
        if env_dian:  hechos.append(("EnvioDian", True))
        if env_rndc:  hechos.append(("EnvioRNDC", True))
        for pred, val in [
            ("TieneInternet", internet), ("ErrorConexion", errorcon),
            ("TimeoutEnvio", timeout),   ("FallaSOAP", falla_soap),
            ("DocumentoRechazado", rechazado), ("DocumentoDuplicado", duplicado),
            ("CertificadoVigente", cert_vigente), ("ResolucionVigente", res_vigente),
            ("NumeroEnRango", num_rango),
            ("TerceroOk", tercero_ok), ("PropietarioOk", propietario_ok),
            ("ClienteOk", cliente_ok), ("DestinatarioOk", destinatario_ok),
            ("RemitenteOk", remitente_ok), ("VehiculoOk", vehiculo_ok),
            ("FacturableOk", facturable_ok),
            ("FacturaAceptadaCliente", fact_aceptada), ("DocumentoTipo12", tipo12),
            ("FacturableConsistente", fact_consist),
            ("CoordenadasCoherentes", coord_ok), ("DestinoExisteRNDC", destino_rndc_ok),
        ]:
            hechos.append((pred, val))

        with st.spinner("Analizando síntomas…"):
            try:
                finales, aplicadas, certezas = encadenamiento_adelante(REGLAS, hechos)
                diagnosticos = [
                    h for h in finales
                    if h not in hechos and h[1] and h[0] in PREDICADOS_DIAGNOSTICO
                ]
                st.session_state.resultado = {
                    "ok": True,
                    "diagnosticos": diagnosticos,
                    "aplicadas": aplicadas,
                    "certezas": certezas,
                    "hechos": hechos,
                    "tipo_label": tipo_label,
                    "env_dian": env_dian,
                    "env_rndc": env_rndc,
                }
            except ValueError as e:
                st.session_state.resultado = {"ok": False, "error": str(e)}
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# COLUMNA DERECHA — Resultados / Resumen
# ════════════════════════════════════════════════════════════════════════════
with col_res:
    res = st.session_state.resultado

    # ── Sin diagnóstico aún: mostrar resumen de lo seleccionado ──────────────
    if res is None:
        tipo_txt = tipo_label.strip() if tipo_label else None
        dest_txt = " + ".join(filter(None, [
            "🏛️ DIAN" if env_dian else "",
            "🗂️ RNDC"  if env_rndc  else "",
        ]))

        if not tipo_txt:
            st.markdown("""
            <div class="summary-wrap">
                <div class="summary-icon">📋</div>
                <h3 style="color:#1e293b;margin:0.3rem 0">Configura tu consulta</h3>
                <p style="color:#64748b;font-size:0.88rem;margin:0.5rem 0 1rem">
                    Completa los pasos del formulario y presiona<br>
                    <strong>Diagnosticar ahora</strong> para obtener el resultado.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            rows = ""
            if tipo_txt:
                rows += f'<div class="summary-row"><span class="summary-lbl">Documento</span>{tipo_txt}</div>'
            if dest_txt:
                rows += f'<div class="summary-row"><span class="summary-lbl">Destino</span>{dest_txt}</div>'
            if not internet:
                rows += '<div class="summary-row" style="border-color:#fca5a5;background:#fef2f2"><span class="summary-lbl">⚠️ Internet</span>Sin conexión</div>'
            if rechazado:
                rows += '<div class="summary-row" style="border-color:#fca5a5;background:#fef2f2"><span class="summary-lbl">⚠️ Estado</span>Documento rechazado</div>'
            if duplicado:
                rows += '<div class="summary-row" style="border-color:#fca5a5;background:#fef2f2"><span class="summary-lbl">⚠️ Estado</span>Documento duplicado</div>'
            if opciones_entidades:
                ent_estado = "Todos correctos ✓" if not st.session_state.get("ej_ent_mal") else \
                             f"Con errores: {', '.join(st.session_state.get('ej_ent_mal',[]))}"
                rows += f'<div class="summary-row"><span class="summary-lbl">Entidades</span>{ent_estado}</div>'

            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:1.3rem;
                        box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:0.8rem;">
                <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:.6px;color:#64748b;margin-bottom:.8rem">
                    📋 RESUMEN DE TU CONSULTA
                </div>
                {rows}
                <p style="font-size:0.82rem;color:#94a3b8;margin:0.9rem 0 0;text-align:center">
                    👆 Presiona <strong style="color:#1d4ed8">Diagnosticar ahora</strong> para obtener el resultado
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.stop()

    # ── Error de validación ───────────────────────────────────────────────────
    if not res["ok"]:
        st.error(f"**Error:** {res['error']}")
        st.stop()

    # ── Resultados ────────────────────────────────────────────────────────────
    diagnosticos = res["diagnosticos"]
    aplicadas    = res["aplicadas"]
    certezas     = res["certezas"]
    errores      = [d for d in diagnosticos if d[0] not in EXITOS]
    exitos       = [d for d in diagnosticos if d[0] in EXITOS]
    conflictos   = detectar_conflictos(diagnosticos)

    tipo_txt = res["tipo_label"].strip()
    dest_txt = " + ".join(filter(None, [
        "DIAN" if res["env_dian"] else "",
        "RNDC" if res["env_rndc"] else "",
    ]))

    # ── Banner resumen ────────────────────────────────────────────────────────
    if errores:
        n = len(errores)
        st.markdown(f"""
        <div class="res-header res-big-err">
            <div style="font-size:1.7rem">❌</div>
            <div style="font-weight:800;font-size:1.1rem;color:#1e293b;margin:.2rem 0">
                {n} problema{"s" if n>1 else ""} detectado{"s" if n>1 else ""}
            </div>
            <div style="font-size:.85rem;color:#64748b">{tipo_txt} → {dest_txt}</div>
        </div>
        """, unsafe_allow_html=True)
    elif exitos:
        st.markdown(f"""
        <div class="res-header res-big-ok">
            <div style="font-size:1.7rem">✅</div>
            <div style="font-weight:800;font-size:1.1rem;color:#1e293b;margin:.2rem 0">
                Envío procesado correctamente
            </div>
            <div style="font-size:.85rem;color:#64748b">{tipo_txt} → {dest_txt}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="res-header res-big-neu">
            <div style="font-size:1.7rem">⚠️</div>
            <div style="font-weight:700;font-size:1rem;color:#1e293b;margin:.2rem 0">
                Sin diagnóstico concluyente
            </div>
            <div style="font-size:.85rem;color:#64748b">Revise que los síntomas ingresados sean completos.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Métricas rápidas ──────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.metric("Problemas", len(errores))
    m2.metric("Reglas disparadas", len(aplicadas))
    m3.metric("Éxitos", len(exitos))

    # ── Resultados exitosos ───────────────────────────────────────────────────
    if exitos:
        st.markdown("#### ✅ Resultados exitosos")
        for d in exitos:
            cert = certezas.get(d, 1.0)
            titulo, accion = DESCRIPCIONES_DIAGNOSTICO.get(d[0], (d[0], ""))
            st.markdown(_dcard("ok", titulo, "", accion, cert), unsafe_allow_html=True)

    # ── Diagnósticos de error ─────────────────────────────────────────────────
    if errores:
        st.markdown("#### ❌ Problemas detectados")
        for d in errores:
            cert = certezas.get(d, 1.0)
            titulo, accion = DESCRIPCIONES_DIAGNOSTICO.get(d[0], (d[0], ""))
            st.markdown(_dcard("err", titulo, "", accion, cert), unsafe_allow_html=True)

    # ── Conflictos ────────────────────────────────────────────────────────────
    if conflictos:
        st.markdown("#### ⚠️ Advertencia")
        for grupo in conflictos:
            nombres = " vs ".join(grupo)
            st.markdown(_dcard("warn", "Diagnósticos contradictorios",
                               f"Se detectaron dos diagnósticos que se excluyen mutuamente: **{nombres}**.",
                               "Revise los síntomas ingresados — puede haber información inconsistente.", 1.0),
                        unsafe_allow_html=True)

    if not errores and not exitos:
        st.info("No se disparó ninguna regla. Verifique que haya completado todos los síntomas relevantes.")

    # ── Detalle técnico ───────────────────────────────────────────────────────
    with st.expander(f"🔧  Detalle técnico — {len(aplicadas)} regla(s) disparada(s)"):
        if aplicadas:
            for nombre in aplicadas:
                cert_r = next((r["certeza"] for r in REGLAS if r["nombre"] == nombre), 1.0)
                desc = DESCRIPCIONES_REGLAS.get(nombre, nombre)
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:.5rem;margin:.3rem 0;'
                    f'font-size:.85rem;"><code style="background:#f1f5f9;padding:.1rem .4rem;'
                    f'border-radius:5px;font-size:.8rem">{nombre}</code>'
                    f'<span style="color:#475569">{desc}</span>'
                    f'{_badge(cert_r)}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.caption("Ninguna regla fue disparada con los síntomas ingresados.")

    st.divider()
    st.caption("SBC · Actividad 4 · IA II · Fundación Universitaria Los Libertadores · Galarza & Solano · 2026")
