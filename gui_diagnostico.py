import tkinter as tk
from tkinter import ttk

# ─────────────────────────────────────────────────────────────────────────────
# LÓGICA DEL SISTEMA BASADO EN CONOCIMIENTO
# ─────────────────────────────────────────────────────────────────────────────

PREDICADOS_SINTOMA = {
    "Documento", "Factura", "NotaCredito", "Remesa", "Manifiesto",
    "EnvioDian", "EnvioRNDC",
    "TerceroOk", "PropietarioOk", "ClienteOk",
    "DestinatarioOk", "RemitenteOk", "VehiculoOk", "FacturableOk",
    "CertificadoVigente", "ResolucionVigente", "NumeroEnRango",
    "ErrorConexion", "TimeoutEnvio", "FallaSOAP",
    "DocumentoDuplicado", "DocumentoRechazado",
    "TieneInternet",
    "CoordenadasCoherentes", "DestinoExisteRNDC",
    "FacturaAceptadaCliente",
    "DocumentoTipo12", "FacturableConsistente",
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
    "DianCaida":                  "La DIAN no está disponible en este momento",
    "RndcCaida":                  "El RNDC no está disponible (falla SOAP)",
    "ErrorAPI":                   "Problema en la integración con la API",
    "ErrorCertificado":           "El certificado digital no está vigente",
    "ErrorResolucionNumeracion":  "La resolución de rango de numeración no está vigente",
    "ErrorNumeroFueraRango":      "El número de factura está fuera del rango autorizado",
    "DocumentoYaProcesado":       "El documento ya había sido registrado previamente",
    "ProblemaInternet":           "Existe un problema de conectividad a internet",
    "TerceroMalDiligenciado":     "Los datos del tercero están incorrectos o incompletos",
    "PropietarioMalDiligenciado": "Los datos del propietario están incorrectos o incompletos",
    "ClienteMalDiligenciado":     "Los datos del cliente están incorrectos o incompletos",
    "DestinatarioMalDiligenciado":"Los datos del destinatario están incorrectos o incompletos",
    "VehiculoMalDiligenciado":    "Los datos del vehículo están incorrectos o incompletos",
    "FacturableMalDiligenciado":  "Los datos del facturable están incorrectos o incompletos",
    "ErrorCoordenadasRemesa":     "Las coordenadas no son coherentes con la ciudad de origen/destino",
    "DestinoNoExisteRNDC":        "El destino de la remesa no existe registrado en el RNDC",
    "ErrorFacturaYaAceptada":     "No se puede emitir la nota crédito: la factura ya fue aceptada",
    "ErrorDocumentoNoTipo12":     "El documento enviado al RNDC no es de tipo 12 (transporte)",
    "ErrorFacturableInconsistente":"Los datos del facturable en el XML no coinciden con la remesa",
    "EnvioExitosoRNDC":           "El RNDC aceptó el manifiesto y devolvió número de autorización",
    "CufeGenerado":               "La DIAN aceptó el envío y generó el CUFE correctamente",
    "TipoXML12":                  "XML tipo 12 — documento de transporte",
    "TipoXML10":                  "XML tipo 10 — otros conceptos",
}

DESCRIPCIONES_REGLAS = {
    "R1a":  "Factura+DIAN+todo OK pero rechazada → DIAN caída",
    "R1b":  "NC+DIAN+todo OK pero rechazada → DIAN caída",
    "R2a":  "Manifiesto+RNDC+FallaSOAP → RNDC caído",
    "R2b":  "Remesa+RNDC+FallaSOAP → RNDC caído",
    "R3a":  "Doc+DIAN+ErrorConexion+Internet+SinTimeout → Error API",
    "R3b":  "Doc+RNDC+ErrorConexion+Internet+SinTimeout → Error API",
    "R7a":  "EnvioDIAN+SinInternet → Problema internet",
    "R7b":  "EnvioRNDC+SinInternet → Problema internet",
    "R4a":  "Factura+DIAN+CertificadoNoVigente → Error certificado",
    "R4b":  "NC+DIAN+CertificadoNoVigente → Error certificado",
    "R5a":  "Factura+DIAN+ResolucionNoVigente → Error resolución numeración",
    "R5b":  "Factura+DIAN+NumeroFueraRango → Error número fuera de rango",
    "R6":   "Doc+Duplicado → Documento ya procesado",
    "R10a": "Manifiesto+RNDC+TerceroInválido → Tercero mal diligenciado",
    "R10b": "Manifiesto+RNDC+PropietarioInválido → Propietario mal diligenciado",
    "R10c": "Manifiesto+RNDC+ClienteInválido → Cliente mal diligenciado",
    "R10d": "Manifiesto+RNDC+VehiculoInválido → Vehículo mal diligenciado",
    "R10e": "Manifiesto+RNDC+FacturableInválido → Facturable mal diligenciado",
    "R11a": "Remesa+RNDC+TerceroInválido → Tercero mal diligenciado",
    "R11b": "Remesa+RNDC+DestinatarioInválido → Destinatario mal diligenciado",
    "R11c": "Remesa+RNDC+DestinoNoExiste → Destino no existe en RNDC",
    "R11d": "Remesa+RNDC+CoordenadasIncoherentes → Error coordenadas remesa",
    "R12":  "Factura+DIAN+FacturableInválido → Facturable mal diligenciado",
    "R13a": "NC+DIAN+FacturableInválido → Facturable mal diligenciado",
    "R13b": "NC+DIAN+FacturaYaAceptada → Error factura ya aceptada",
    "R14a": "Factura+RNDC+NoEsTipo12 → Error documento no tipo 12",
    "R14b": "NC+RNDC+NoEsTipo12 → Error documento no tipo 12",
    "R14c": "Factura+RNDC+Tipo12+FacturableInconsistente → Error facturable inconsistente",
    "R14d": "NC+RNDC+Tipo12+FacturableInconsistente → Error facturable inconsistente",
    "R15":  "Manifiesto+RNDC+TodasEntidadesOk+Internet → Envío exitoso RNDC",
    "R16a": "Factura+DIAN+CertVig+ResolVig+NumRango+FacturableOk → CUFE generado",
    "R16b": "NC+DIAN+CertVig+FacturableOk → CUFE generado",
    "R17a": "Factura+CufeGenerado+Tipo12 → XML tipo 12",
    "R17b": "Factura+CufeGenerado+NoTipo12 → XML tipo 10",
    "R17c": "NC+CufeGenerado+Tipo12 → XML tipo 12",
    "R17d": "NC+CufeGenerado+NoTipo12 → XML tipo 10",
}


def _crear_regla(nombre, condiciones, conclusion, certeza=1.0):
    return {"nombre": nombre, "condiciones": condiciones, "conclusion": conclusion, "certeza": certeza}


def crear_base_conocimiento():
    r = _crear_regla
    return [
        # Grupo A — Conectividad
        r("R1a", [("Factura",True),("EnvioDian",True),("FacturableOk",True),("ErrorConexion",False),
                  ("TieneInternet",True),("CertificadoVigente",True),("ResolucionVigente",True),
                  ("NumeroEnRango",True),("DocumentoRechazado",True),("TimeoutEnvio",False),("FallaSOAP",False)],
          ("DianCaida",True), 0.90),
        r("R1b", [("NotaCredito",True),("EnvioDian",True),("FacturableOk",True),("ErrorConexion",False),
                  ("TieneInternet",True),("CertificadoVigente",True),("FacturaAceptadaCliente",False),
                  ("DocumentoRechazado",True),("TimeoutEnvio",False),("FallaSOAP",False)],
          ("DianCaida",True), 0.90),
        r("R2a", [("Manifiesto",True),("EnvioRNDC",True),("FallaSOAP",True)], ("RndcCaida",True), 0.98),
        r("R2b", [("Remesa",True),("EnvioRNDC",True),("FallaSOAP",True)], ("RndcCaida",True), 0.98),
        r("R3a", [("Documento",True),("EnvioDian",True),("ErrorConexion",True),("TieneInternet",True),
                  ("TimeoutEnvio",False)], ("ErrorAPI",True), 0.90),
        r("R3b", [("Documento",True),("EnvioRNDC",True),("ErrorConexion",True),("TieneInternet",True),
                  ("TimeoutEnvio",False)], ("ErrorAPI",True), 0.90),
        r("R7a", [("EnvioDian",True),("TieneInternet",False)], ("ProblemaInternet",True), 1.0),
        r("R7b", [("EnvioRNDC",True),("TieneInternet",False)], ("ProblemaInternet",True), 1.0),
        # Grupo B — Certificado
        r("R4a", [("Factura",True),("EnvioDian",True),("CertificadoVigente",False)], ("ErrorCertificado",True), 1.0),
        r("R4b", [("NotaCredito",True),("EnvioDian",True),("CertificadoVigente",False)], ("ErrorCertificado",True), 1.0),
        # Grupo C — Numeración
        r("R5a", [("Factura",True),("EnvioDian",True),("ResolucionVigente",False)], ("ErrorResolucionNumeracion",True), 1.0),
        r("R5b", [("Factura",True),("EnvioDian",True),("NumeroEnRango",False)], ("ErrorNumeroFueraRango",True), 1.0),
        # Grupo D — Duplicado
        r("R6", [("Documento",True),("DocumentoDuplicado",True)], ("DocumentoYaProcesado",True), 1.0),
        # Grupo E — Manifiesto entidades
        r("R10a", [("Manifiesto",True),("EnvioRNDC",True),("TerceroOk",False)], ("TerceroMalDiligenciado",True), 1.0),
        r("R10b", [("Manifiesto",True),("EnvioRNDC",True),("PropietarioOk",False)], ("PropietarioMalDiligenciado",True), 1.0),
        r("R10c", [("Manifiesto",True),("EnvioRNDC",True),("ClienteOk",False)], ("ClienteMalDiligenciado",True), 1.0),
        r("R10d", [("Manifiesto",True),("EnvioRNDC",True),("VehiculoOk",False)], ("VehiculoMalDiligenciado",True), 1.0),
        r("R10e", [("Manifiesto",True),("EnvioRNDC",True),("FacturableOk",False)], ("FacturableMalDiligenciado",True), 1.0),
        # Grupo F — Remesa errores
        r("R11a", [("Remesa",True),("EnvioRNDC",True),("TerceroOk",False)], ("TerceroMalDiligenciado",True), 1.0),
        r("R11b", [("Remesa",True),("EnvioRNDC",True),("DestinatarioOk",False)], ("DestinatarioMalDiligenciado",True), 1.0),
        r("R11c", [("Remesa",True),("EnvioRNDC",True),("DestinoExisteRNDC",False)], ("DestinoNoExisteRNDC",True), 1.0),
        r("R11d", [("Remesa",True),("EnvioRNDC",True),("CoordenadasCoherentes",False)], ("ErrorCoordenadasRemesa",True), 1.0),
        # Grupo G — Factura DIAN
        r("R12", [("Factura",True),("EnvioDian",True),("FacturableOk",False)], ("FacturableMalDiligenciado",True), 1.0),
        # Grupo H — NC DIAN
        r("R13a", [("NotaCredito",True),("EnvioDian",True),("FacturableOk",False)], ("FacturableMalDiligenciado",True), 1.0),
        r("R13b", [("NotaCredito",True),("EnvioDian",True),("FacturaAceptadaCliente",True)], ("ErrorFacturaYaAceptada",True), 1.0),
        # Grupo I — Factura/NC → RNDC tipo 12
        r("R14a", [("Factura",True),("EnvioRNDC",True),("DocumentoTipo12",False)], ("ErrorDocumentoNoTipo12",True), 1.0),
        r("R14b", [("NotaCredito",True),("EnvioRNDC",True),("DocumentoTipo12",False)], ("ErrorDocumentoNoTipo12",True), 1.0),
        r("R14c", [("Factura",True),("EnvioRNDC",True),("DocumentoTipo12",True),("FacturableConsistente",False)], ("ErrorFacturableInconsistente",True), 1.0),
        r("R14d", [("NotaCredito",True),("EnvioRNDC",True),("DocumentoTipo12",True),("FacturableConsistente",False)], ("ErrorFacturableInconsistente",True), 1.0),
        # Grupo J — Éxito
        r("R15", [("Manifiesto",True),("EnvioRNDC",True),("TerceroOk",True),("FacturableOk",True),
                  ("PropietarioOk",True),("ClienteOk",True),("DestinatarioOk",True),("RemitenteOk",True),
                  ("VehiculoOk",True),("TieneInternet",True),("FallaSOAP",False)],
          ("EnvioExitosoRNDC",True), 0.98),
        r("R16a", [("Factura",True),("EnvioDian",True),("CertificadoVigente",True),("ResolucionVigente",True),
                   ("NumeroEnRango",True),("FacturableOk",True)], ("CufeGenerado",True), 0.98),
        r("R16b", [("NotaCredito",True),("EnvioDian",True),("CertificadoVigente",True),
                   ("FacturableOk",True),("FacturaAceptadaCliente",False)], ("CufeGenerado",True), 0.98),
        r("R17a", [("Factura",True),("CufeGenerado",True),("DocumentoTipo12",True)], ("TipoXML12",True), 1.0),
        r("R17b", [("Factura",True),("CufeGenerado",True),("DocumentoTipo12",False)], ("TipoXML10",True), 1.0),
        r("R17c", [("NotaCredito",True),("CufeGenerado",True),("DocumentoTipo12",True)], ("TipoXML12",True), 1.0),
        r("R17d", [("NotaCredito",True),("CufeGenerado",True),("DocumentoTipo12",False)], ("TipoXML10",True), 1.0),
    ]


def validar_hechos(hechos):
    vistos = {}
    for pred, valor in hechos:
        if pred in vistos and vistos[pred] != valor:
            raise ValueError(f"Contradicción: '{pred}' aparece como True y False a la vez.")
        vistos[pred] = valor
    tipos_activos = [t for t in TIPOS_DOCUMENTO if vistos.get(t) is True]
    if len(tipos_activos) > 1:
        raise ValueError(f"Tipos mutuamente excluyentes seleccionados: {', '.join(tipos_activos)}.")


def aplicar_mundo_cerrado(hechos):
    presentes = {h[0] for h in hechos}
    return list(hechos) + [(p, False) for p in PREDICADOS_SINTOMA if p not in presentes]


def detectar_conflictos(diagnosticos):
    nombres = {d[0] for d in diagnosticos if d[1]}
    return [g for g in CONFLICTOS_DIAGNOSTICO if g.issubset(nombres)]


def encadenamiento_adelante(reglas, hechos):
    hechos_unicos = list(dict.fromkeys(hechos))
    validar_hechos(hechos_unicos)
    nuevos = aplicar_mundo_cerrado(hechos_unicos)
    aplicadas = []
    certezas = {}
    cambio = True
    while cambio:
        cambio = False
        for regla in reglas:
            if regla["nombre"] in aplicadas:
                continue
            if all(c in nuevos for c in regla["condiciones"]):
                aplicadas.append(regla["nombre"])
                if regla["conclusion"] not in nuevos:
                    nuevos.append(regla["conclusion"])
                    certezas[regla["conclusion"]] = regla["certeza"]
                    cambio = True
                else:
                    c_prev = certezas.get(regla["conclusion"], 0)
                    certezas[regla["conclusion"]] = round(
                        1 - (1 - c_prev) * (1 - regla["certeza"]), 4)
    return nuevos, aplicadas, certezas


# ─────────────────────────────────────────────────────────────────────────────
# INTERFAZ GRÁFICA
# ─────────────────────────────────────────────────────────────────────────────

# Colores
BG        = "#f0f2f5"
CARD_BG   = "#ffffff"
HDR_BG    = "#1a252f"
HDR_SIDE  = "#2c3e50"
ACCENT    = "#2980b9"
SUCCESS   = "#27ae60"
ERR_COL   = "#c0392b"
WARN_COL  = "#d35400"
TEXT      = "#2c3e50"
MUTED     = "#7f8c8d"
BORDER    = "#dce1e7"

FONT_BODY   = ("Segoe UI", 9)
FONT_BOLD   = ("Segoe UI", 9, "bold")
FONT_TITLE  = ("Segoe UI", 13, "bold")
FONT_HEADER = ("Segoe UI", 10, "bold")
FONT_MONO   = ("Consolas", 10)
FONT_MONO_B = ("Consolas", 10, "bold")


class ScrollableFrame(tk.Frame):
    """Canvas-based scrollable container."""
    def __init__(self, parent, width=440, **kwargs):
        super().__init__(parent, bg=BG, **kwargs)
        self._canvas = tk.Canvas(self, bg=BG, highlightthickness=0, width=width)
        self._sb = ttk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self.inner = tk.Frame(self._canvas, bg=BG)

        self._win = self._canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self._canvas.configure(yscrollcommand=self._sb.set)

        self.inner.bind("<Configure>", self._update_scrollregion)
        self._canvas.bind("<Configure>", self._update_width)

        self._canvas.pack(side="left", fill="both", expand=True)
        self._sb.pack(side="right", fill="y")

        self._canvas.bind("<Enter>", self._bind_wheel)
        self._canvas.bind("<Leave>", self._unbind_wheel)

    def _update_scrollregion(self, _e=None):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _update_width(self, event):
        self._canvas.itemconfig(self._win, width=event.width)

    def _bind_wheel(self, _e=None):
        self._canvas.bind_all("<MouseWheel>", self._on_wheel)

    def _unbind_wheel(self, _e=None):
        self._canvas.unbind_all("<MouseWheel>")

    def _on_wheel(self, event):
        self._canvas.yview_scroll(-1 * (event.delta // 120), "units")


def _card(parent, title):
    """Styled LabelFrame card."""
    f = tk.LabelFrame(
        parent, text=f"  {title}  ",
        font=FONT_BOLD, bg=CARD_BG, fg=TEXT,
        bd=1, relief="groove", padx=10, pady=6,
    )
    f.pack(fill="x", padx=8, pady=4)
    return f


def _check(parent, text, var):
    tk.Checkbutton(
        parent, text=text, variable=var,
        font=FONT_BODY, bg=CARD_BG, fg=TEXT,
        activebackground=CARD_BG, selectcolor=CARD_BG,
        anchor="w",
    ).pack(fill="x", pady=2)


def _radio(parent, text, var, value):
    tk.Radiobutton(
        parent, text=text, variable=var, value=value,
        font=FONT_BODY, bg=CARD_BG, fg=TEXT,
        activebackground=CARD_BG, selectcolor=CARD_BG,
        anchor="w",
    ).pack(fill="x", pady=2)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Diagnóstico DIAN / RNDC  —  Sistema Basado en Conocimiento")
        self.root.geometry("1200x800")
        self.root.minsize(950, 640)
        self.root.configure(bg=BG)

        self._reglas = crear_base_conocimiento()
        self._init_vars()
        self._build()

    # ── Variables ──────────────────────────────────────────────────────────────

    def _init_vars(self):
        self.v_tipo         = tk.StringVar(value="")
        self.v_dian         = tk.BooleanVar(value=False)
        self.v_rndc         = tk.BooleanVar(value=False)
        # Conectividad
        self.v_internet     = tk.BooleanVar(value=True)
        self.v_error_con    = tk.BooleanVar(value=False)
        self.v_timeout      = tk.BooleanVar(value=False)
        self.v_soap         = tk.BooleanVar(value=False)
        # Estado del envío
        self.v_rechazado    = tk.BooleanVar(value=False)
        self.v_duplicado    = tk.BooleanVar(value=False)
        # Certificado y numeración
        self.v_cert         = tk.BooleanVar(value=True)
        self.v_resolucion   = tk.BooleanVar(value=True)
        self.v_rango        = tk.BooleanVar(value=True)
        # Entidades
        self.v_tercero      = tk.BooleanVar(value=True)
        self.v_propietario  = tk.BooleanVar(value=True)
        self.v_cliente      = tk.BooleanVar(value=True)
        self.v_destinatario = tk.BooleanVar(value=True)
        self.v_remitente    = tk.BooleanVar(value=True)
        self.v_vehiculo     = tk.BooleanVar(value=True)
        self.v_facturable   = tk.BooleanVar(value=True)
        # Especiales
        self.v_fact_aceptada  = tk.BooleanVar(value=False)
        self.v_tipo12         = tk.BooleanVar(value=False)
        self.v_fact_consist   = tk.BooleanVar(value=True)
        self.v_coordenadas    = tk.BooleanVar(value=True)
        self.v_destino_rndc   = tk.BooleanVar(value=True)

    # ── Construcción UI ────────────────────────────────────────────────────────

    def _build(self):
        self._build_header()
        self._build_body()

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=HDR_BG, height=58)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="  Sistema de Diagnóstico  DIAN / RNDC",
                 font=FONT_TITLE, bg=HDR_BG, fg="white").pack(side="left", padx=10, pady=14)

        tk.Label(hdr, text="Actividad 4 — SBC  Inteligencia Artificial II  ",
                 font=("Segoe UI", 9), bg=HDR_BG, fg="#aab7c4").pack(side="right", padx=10, pady=14)

    def _build_body(self):
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        # ── Panel izquierdo (formulario) ───────────────────────────────────────
        left = tk.Frame(body, bg=BG, width=450)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        sf = ScrollableFrame(left, width=432)
        sf.pack(fill="both", expand=True)
        p = sf.inner

        self._form_tipo(p)
        self._form_destino(p)
        self._form_conectividad(p)
        self._form_estado(p)
        self._form_certificado(p)
        self._form_entidades(p)
        self._form_especiales(p)
        self._form_buttons(p)

        # ── Separador ─────────────────────────────────────────────────────────
        sep = tk.Frame(body, bg=BORDER, width=1)
        sep.pack(side="left", fill="y", padx=8)

        # ── Panel derecho (resultados) ─────────────────────────────────────────
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="RESULTADOS DEL DIAGNÓSTICO",
                 font=FONT_HEADER, bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 6))

        self._result_txt = tk.Text(
            right, font=FONT_MONO, bg=CARD_BG, fg=TEXT,
            relief="flat", bd=1, wrap="word", state="disabled",
            padx=14, pady=12, spacing1=2, spacing3=2,
        )
        sb_r = ttk.Scrollbar(right, command=self._result_txt.yview)
        self._result_txt.configure(yscrollcommand=sb_r.set)
        self._result_txt.pack(side="left", fill="both", expand=True)
        sb_r.pack(side="right", fill="y")

        self._config_tags()
        self._show_welcome()

    # ── Secciones del formulario ───────────────────────────────────────────────

    def _form_tipo(self, p):
        c = _card(p, "1  Tipo de documento")
        for label, val in [
            ("Factura electrónica", "Factura"),
            ("Nota crédito",        "NotaCredito"),
            ("Remesa",              "Remesa"),
            ("Manifiesto de carga", "Manifiesto"),
        ]:
            _radio(c, label, self.v_tipo, val)
        _radio(c, "(ninguno seleccionado)", self.v_tipo, "")

    def _form_destino(self, p):
        c = _card(p, "2  Destino del envío")
        _check(c, "Envío a la DIAN", self.v_dian)
        _check(c, "Envío al RNDC",   self.v_rndc)

    def _form_conectividad(self, p):
        c = _card(p, "3  Conectividad")
        _check(c, "Tiene conexión a internet",          self.v_internet)
        _check(c, "Error de conexión al servicio",      self.v_error_con)
        _check(c, "Timeout en el envío",                self.v_timeout)
        _check(c, "Falla SOAP devuelta por el servicio",self.v_soap)

    def _form_estado(self, p):
        c = _card(p, "4  Estado del envío")
        _check(c, "Documento rechazado por el servicio",         self.v_rechazado)
        _check(c, "Documento duplicado (ya fue enviado antes)",  self.v_duplicado)

    def _form_certificado(self, p):
        c = _card(p, "5  Certificado y numeración DIAN")
        _check(c, "Certificado digital vigente",                     self.v_cert)
        _check(c, "Resolución de numeración vigente",                self.v_resolucion)
        _check(c, "Número de documento dentro del rango autorizado", self.v_rango)

    def _form_entidades(self, p):
        c = _card(p, "6  Validez de entidades")
        tk.Label(c, text="Desmarque si los datos están mal diligenciados",
                 font=("Segoe UI", 8), bg=CARD_BG, fg=MUTED).pack(anchor="w", pady=(0, 4))
        _check(c, "Tercero correcto",             self.v_tercero)
        _check(c, "Propietario del vehículo OK",  self.v_propietario)
        _check(c, "Cliente correcto",             self.v_cliente)
        _check(c, "Destinatario correcto",        self.v_destinatario)
        _check(c, "Remitente correcto",           self.v_remitente)
        _check(c, "Vehículo correcto",            self.v_vehiculo)
        _check(c, "Facturable correcto",          self.v_facturable)

    def _form_especiales(self, p):
        c = _card(p, "7  Condiciones especiales")
        _check(c, "Factura asociada ya aceptada por el cliente",     self.v_fact_aceptada)
        _check(c, "Documento es tipo 12 (transporte)",               self.v_tipo12)
        _check(c, "Facturable consistente (XML coincide con remesa)", self.v_fact_consist)
        _check(c, "Coordenadas coherentes con ciudad de destino",     self.v_coordenadas)
        _check(c, "Destino de remesa existe en el RNDC",             self.v_destino_rndc)

    def _form_buttons(self, p):
        f = tk.Frame(p, bg=BG, pady=14)
        f.pack(fill="x", padx=8)

        tk.Button(
            f, text="  Diagnosticar  ",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg="white", activebackground="#1f6aa5", activeforeground="white",
            relief="flat", padx=10, pady=8, cursor="hand2",
            command=self._diagnosticar,
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            f, text="Limpiar todo",
            font=FONT_BODY, bg="#ecf0f1", fg=TEXT,
            activebackground="#dde1e5", relief="flat", padx=10, pady=8, cursor="hand2",
            command=self._limpiar,
        ).pack(side="left")

    # ── Tags del área de resultados ────────────────────────────────────────────

    def _config_tags(self):
        t = self._result_txt
        t.tag_configure("title",    font=("Segoe UI", 12, "bold"), foreground=TEXT, spacing3=8)
        t.tag_configure("section",  font=("Segoe UI", 10, "bold"), foreground=ACCENT, spacing1=10, spacing3=3)
        t.tag_configure("ok",       foreground=SUCCESS, font=FONT_MONO_B)
        t.tag_configure("err",      foreground=ERR_COL, font=FONT_MONO_B)
        t.tag_configure("warn",     foreground=WARN_COL, font=FONT_BOLD)
        t.tag_configure("rule",     foreground="#8e44ad")
        t.tag_configure("muted",    foreground=MUTED)
        t.tag_configure("desc",     font=("Segoe UI", 9), foreground="#555555")
        t.tag_configure("fact_ok",  foreground=SUCCESS)
        t.tag_configure("fact_no",  foreground=MUTED)
        t.tag_configure("line",     foreground=BORDER)

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _build_hechos(self):
        hechos = []
        tipo = self.v_tipo.get()
        if tipo:
            hechos += [(tipo, True), ("Documento", True)]

        if self.v_dian.get(): hechos.append(("EnvioDian", True))
        if self.v_rndc.get(): hechos.append(("EnvioRNDC", True))

        for pred, var in [
            ("TieneInternet",      self.v_internet),
            ("ErrorConexion",      self.v_error_con),
            ("TimeoutEnvio",       self.v_timeout),
            ("FallaSOAP",          self.v_soap),
            ("DocumentoRechazado", self.v_rechazado),
            ("DocumentoDuplicado", self.v_duplicado),
            ("CertificadoVigente", self.v_cert),
            ("ResolucionVigente",  self.v_resolucion),
            ("NumeroEnRango",      self.v_rango),
            ("TerceroOk",          self.v_tercero),
            ("PropietarioOk",      self.v_propietario),
            ("ClienteOk",          self.v_cliente),
            ("DestinatarioOk",     self.v_destinatario),
            ("RemitenteOk",        self.v_remitente),
            ("VehiculoOk",         self.v_vehiculo),
            ("FacturableOk",       self.v_facturable),
            ("FacturaAceptadaCliente", self.v_fact_aceptada),
            ("DocumentoTipo12",    self.v_tipo12),
            ("FacturableConsistente", self.v_fact_consist),
            ("CoordenadasCoherentes", self.v_coordenadas),
            ("DestinoExisteRNDC",  self.v_destino_rndc),
        ]:
            hechos.append((pred, var.get()))

        return hechos

    def _write(self, text, tag=""):
        self._result_txt.insert("end", text, tag)

    def _diagnosticar(self):
        hechos = self._build_hechos()

        self._result_txt.configure(state="normal")
        self._result_txt.delete("1.0", "end")

        try:
            finales, aplicadas, certezas = encadenamiento_adelante(self._reglas, hechos)
        except ValueError as e:
            self._write("ERROR EN LOS HECHOS INGRESADOS\n\n", "title")
            self._write(str(e) + "\n", "err")
            self._result_txt.configure(state="disabled")
            return

        self._write("DIAGNÓSTICO DEL SISTEMA\n", "title")
        self._write("─" * 44 + "\n", "muted")

        # Hechos ingresados
        self._write("\nSíntomas ingresados:\n", "section")
        for h in hechos:
            if h[1]:
                self._write(f"  ✓  {h[0]}\n", "fact_ok")
            else:
                self._write(f"  ✗  {h[0]}\n", "fact_no")

        # Reglas disparadas
        self._write(f"\nReglas disparadas ({len(aplicadas)}):\n", "section")
        if aplicadas:
            for nombre in aplicadas:
                self._write(f"  [{nombre}]  ", "rule")
                self._write(DESCRIPCIONES_REGLAS.get(nombre, nombre) + "\n", "muted")
        else:
            self._write("  Ninguna regla fue disparada.\n", "muted")

        # Separar éxitos y errores
        diagnosticos = [
            h for h in finales
            if h not in hechos and h[1] and h[0] in PREDICADOS_DIAGNOSTICO
        ]
        exitos  = [d for d in diagnosticos if d[0] in EXITOS]
        errores = [d for d in diagnosticos if d[0] not in EXITOS]

        # Resultados de éxito
        if exitos:
            self._write("\nResultados exitosos:\n", "section")
            for d in exitos:
                cert = certezas.get(d, 1.0)
                self._write(f"  ✓  {d[0]}  ({cert:.0%})\n", "ok")
                desc = DESCRIPCIONES_DIAGNOSTICO.get(d[0], "")
                if desc:
                    self._write(f"       {desc}\n", "desc")

        # Diagnósticos de error
        self._write("\nDiagnósticos de error:\n", "section")
        if errores:
            for d in errores:
                cert = certezas.get(d, 1.0)
                self._write(f"  ✗  {d[0]}  ({cert:.0%})\n", "err")
                desc = DESCRIPCIONES_DIAGNOSTICO.get(d[0], "")
                if desc:
                    self._write(f"       {desc}\n", "desc")

            conflictos = detectar_conflictos(diagnosticos)
            if conflictos:
                self._write("\nADVERTENCIA — diagnósticos mutuamente excluyentes:\n", "warn")
                for grupo in conflictos:
                    self._write(f"  !  {' vs '.join(grupo)}\n", "warn")
        else:
            if not exitos:
                self._write("  No se detectaron problemas con los síntomas proporcionados.\n", "muted")
            else:
                self._write("  Sin errores detectados.\n", "muted")

        self._write("\n" + "─" * 44 + "\n", "muted")
        self._result_txt.configure(state="disabled")

    def _limpiar(self):
        for var, default in [
            (self.v_tipo, ""),
            (self.v_dian, False), (self.v_rndc, False),
            (self.v_internet, True), (self.v_error_con, False),
            (self.v_timeout, False), (self.v_soap, False),
            (self.v_rechazado, False), (self.v_duplicado, False),
            (self.v_cert, True), (self.v_resolucion, True), (self.v_rango, True),
            (self.v_tercero, True), (self.v_propietario, True), (self.v_cliente, True),
            (self.v_destinatario, True), (self.v_remitente, True),
            (self.v_vehiculo, True), (self.v_facturable, True),
            (self.v_fact_aceptada, False), (self.v_tipo12, False),
            (self.v_fact_consist, True), (self.v_coordenadas, True), (self.v_destino_rndc, True),
        ]:
            var.set(default)
        self._show_welcome()

    def _show_welcome(self):
        self._result_txt.configure(state="normal")
        self._result_txt.delete("1.0", "end")
        self._write("Bienvenido\n\n", "title")
        self._write("Instrucciones:\n", "section")
        self._write(
            "  1. Seleccione el tipo de documento\n"
            "  2. Marque el destino del envío (DIAN / RNDC)\n"
            "  3. Configure los síntomas observados\n"
            "  4. Haga clic en  Diagnosticar\n\n",
            "muted"
        )
        self._write("El motor de inferencia aplicará\n", "desc")
        self._write("encadenamiento hacia adelante con\n", "desc")
        self._write("supuesto de mundo cerrado (CWA)\n", "desc")
        self._write("para identificar la causa del\n", "desc")
        self._write("problema en el envío.\n", "desc")
        self._result_txt.configure(state="disabled")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except Exception:
        pass
    App(root)
    root.mainloop()
