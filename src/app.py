"""
app.py — Interfaz web Streamlit
Sistema Basado en Conocimiento: Diagnóstico de envíos DIAN / RNDC
Autores: Galarza, Solano — Fundación Universitaria Los Libertadores, 2026

Ejecución:
    streamlit run src/app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from base_conocimiento import (
    crear_base_conocimiento, PREDICADOS_DIAGNOSTICO, EXITOS,
    CONFLICTOS_DIAGNOSTICO, DESCRIPCIONES_DIAGNOSTICO, DESCRIPCIONES_REGLAS,
)
from motor_inferencia import (
    encadenamiento_adelante, detectar_conflictos, porque,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES UI
# ─────────────────────────────────────────────────────────────────────────────

TIPOS_MAP = {
    "📄  Factura electrónica": "Factura",
    "📝  Nota crédito":        "NotaCredito",
    "🚛  Remesa":              "Remesa",
    "📦  Manifiesto de carga": "Manifiesto",
}

EJEMPLOS = {
    "🔴  DIAN caída": dict(
        ej_tipo="📄  Factura electrónica", ej_dian=True,  ej_rndc=False,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=True, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "📶  Sin internet": dict(
        ej_tipo="📄  Factura electrónica", ej_dian=True,  ej_rndc=False,
        ej_internet=False, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "🔏  Certificado vencido": dict(
        ej_tipo="📄  Factura electrónica", ej_dian=True,  ej_rndc=False,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=False, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "✅  Manifiesto exitoso": dict(
        ej_tipo="📦  Manifiesto de carga", ej_dian=False, ej_rndc=True,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "🚛  Remesa — tercero inválido": dict(
        ej_tipo="🚛  Remesa", ej_dian=False, ej_rndc=True,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=["Tercero"], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "🔁  Documento duplicado": dict(
        ej_tipo="🚛  Remesa", ej_dian=False, ej_rndc=True,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=True,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
}

DEFAULT_STATE = dict(
    ej_tipo=None, ej_dian=False, ej_rndc=False,
    ej_internet=True, ej_errorcon=False, ej_timeout=False, ej_soap=False,
    ej_rechazado=False, ej_dup=False,
    ej_cert=True, ej_resol=True, ej_rango=True,
    ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
    ej_fconsist=True, ej_coord=True, ej_destrndc=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# ESTADO Y HELPERS
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
[data-testid="stAppViewContainer"] { background: #f1f5f9; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #0f172a !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown p { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: #334155 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #1e3a5f !important; color: #e2e8f0 !important;
    border: 1px solid #334155 !important; border-radius: 8px !important;
    font-size: 0.85rem !important; margin-bottom: 4px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2563eb !important; color: white !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(120deg, #0f172a 0%, #1e3a5f 50%, #1d4ed8 100%);
    padding: 1.6rem 2rem 1.4rem; border-radius: 14px; margin: 0 0 1.2rem 0;
    box-shadow: 0 6px 24px rgba(15,23,42,0.22);
}
.hero h1     { color: #ffffff !important; font-size: 1.55rem; font-weight: 800; margin: 0 0 0.3rem; }
.hero p      { color: #93c5fd !important; margin: 0; font-size: 0.87rem; }
.hero span   { color: #bfdbfe !important; }
.hero-badge  {
    display: inline-block; background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2); color: #bfdbfe !important;
    font-size: 0.73rem; font-weight: 600;
    padding: 0.18rem 0.65rem; border-radius: 999px; margin-bottom: 0.6rem;
}
/* Override final hero */
.hero, .hero *, .hero h1, .hero p, .hero span, .hero div { color: #ffffff !important; }
.hero p      { color: #93c5fd !important; }
.hero .hero-badge { color: #bfdbfe !important; }

/* ── Step bar ── */
.step-bar {
    display: flex; align-items: center; justify-content: center;
    background: white; border-radius: 14px; padding: 0.9rem 1.5rem;
    margin-bottom: 1.2rem; box-shadow: 0 1px 4px rgba(0,0,0,0.07); gap: 0;
}
.step-item  { display: flex; flex-direction: column; align-items: center; min-width: 72px; }
.step-num   { width: 34px; height: 34px; border-radius: 50%; display: flex;
              align-items: center; justify-content: center;
              font-size: 0.85rem; font-weight: 700; margin-bottom: 0.25rem; }
.step-done    { background: #dcfce7; color: #15803d !important; }
.step-active  { background: #1d4ed8; color: white !important; box-shadow: 0 0 0 4px #bfdbfe; }
.step-pending { background: #f1f5f9; color: #94a3b8 !important; }
.step-lbl   { font-size: 0.7rem; color: #64748b !important; font-weight: 600;
              text-transform: uppercase; letter-spacing: 0.4px; }
.step-line  { flex: 1; height: 2px; margin: 0 0.3rem 1.4rem; min-width: 30px; }
.line-done  { background: #22c55e; }
.line-active{ background: linear-gradient(90deg, #22c55e, #bfdbfe); }
.line-pend  { background: #e2e8f0; }

/* ── Forzar texto oscuro en contenido principal ── */
[data-testid="stMain"] p, [data-testid="stMain"] span, [data-testid="stMain"] label,
[data-testid="stMain"] li { color: #1e293b; }
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span,
[data-testid="stCheckbox"] label, [data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] label span,
[data-testid="stRadio"] label, [data-testid="stRadio"] label p,
[data-testid="stRadio"] label span,
[data-testid="stMultiSelect"] label, [data-testid="stMultiSelect"] p,
[data-testid="stSelectbox"] label { color: #1e293b !important; }
[data-testid="stCaptionContainer"] p, small { color: #64748b !important; }

/* ── Expanders ── */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0 !important; border-radius: 10px !important;
    overflow: hidden; background: #ffffff !important;
}
[data-testid="stExpander"] summary {
    background: #f8fafc !important; font-weight: 600; color: #1e293b !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span { color: #1e293b !important; }
[data-testid="stExpander"] > div,
[data-testid="stExpander"] [data-testid="stVerticalBlock"] { background: #ffffff !important; }

/* ── Result cards ── */
.dcard { border-radius: 12px; padding: 1rem 1.2rem; margin: 0.55rem 0;
         box-shadow: 0 1px 3px rgba(0,0,0,0.06); animation: fadeUp 0.3s ease; }
.dcard-ok   { background: #f0fdf4; border-left: 4px solid #22c55e; }
.dcard-err  { background: #fef2f2; border-left: 4px solid #ef4444; }
.dcard-warn { background: #fffbeb; border-left: 4px solid #f59e0b; }
.dcard-title  { font-weight: 700; font-size: 0.96rem; color: #1e293b; margin: 0 0 0.25rem; }
.dcard-desc   { font-size: 0.85rem; color: #475569; margin: 0 0 0.55rem; line-height: 1.5; }
.dcard-action { font-size: 0.82rem; color: #1d4ed8; background: #eff6ff;
                padding: 0.3rem 0.65rem; border-radius: 6px; display: inline-block; }
.dcard-action-warn { font-size: 0.82rem; color: #92400e; background: #fef3c7;
                     padding: 0.3rem 0.65rem; border-radius: 6px; display: inline-block; }

/* ── Confidence badge ── */
.cbadge { display: inline-block; font-size: 0.73rem; font-weight: 700;
          padding: 0.12rem 0.55rem; border-radius: 999px; margin-left: 0.5rem; vertical-align: middle; }
.cbadge-high { background: #dcfce7; color: #15803d; }
.cbadge-med  { background: #fef9c3; color: #854d0e; }
.cbadge-low  { background: #fee2e2; color: #991b1b; }

/* ── Summary ── */
.summary-row { display: flex; align-items: center; gap: 0.6rem;
               background: #f8fafc; border-radius: 9px; padding: 0.55rem 0.9rem;
               margin: 0.4rem 0; font-size: 0.88rem; color: #334155;
               border: 1px solid #e2e8f0; }
.summary-lbl { font-weight: 600; min-width: 90px; color: #64748b; font-size: 0.8rem; }

/* ── Metrics ── */
[data-testid="stMetricLabel"] p  { color: #64748b !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] div { color: #1e293b !important; font-weight: 700 !important; }

/* ── Primary button ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    border: none !important; border-radius: 10px !important;
    font-size: 1rem !important; font-weight: 700 !important; padding: 0.7rem 1.2rem !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8) !important;
    transform: translateY(-1px) !important;
}

@keyframes fadeUp { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# HTML HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _step_bar(step: int) -> str:
    def circle(n, label):
        cls  = "step-done" if n < step else ("step-active" if n == step else "step-pending")
        icon = "✓" if n < step else str(n)
        return f'<div class="step-item"><div class="step-num {cls}">{icon}</div><div class="step-lbl">{label}</div></div>'
    def line(n):
        cls = "line-done" if n < step else ("line-active" if n == step else "line-pend")
        return f'<div class="step-line {cls}"></div>'
    steps = [(1,"Documento"),(2,"Destino"),(3,"Síntomas"),(4,"Resultado")]
    html  = '<div class="step-bar">'
    for i,(n,lbl) in enumerate(steps):
        html += circle(n, lbl)
        if i < len(steps)-1:
            html += line(n)
    return html + "</div>"


def _badge(cert: float) -> str:
    cls = "cbadge-high" if cert >= 0.95 else ("cbadge-med" if cert >= 0.80 else "cbadge-low")
    return f'<span class="cbadge {cls}">{cert:.0%}</span>'


def _dcard(kind, titulo, accion, cert):
    action_cls = "dcard-action" if kind in ("ok","err") else "dcard-action-warn"
    return (f'<div class="dcard dcard-{kind}">'
            f'<p class="dcard-title">{titulo} {_badge(cert)}</p>'
            f'<span class="{action_cls}">💡 {accion}</span></div>')


# ─────────────────────────────────────────────────────────────────────────────
# APP PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Diagnóstico DIAN / RNDC",
    page_icon="🔍", layout="wide",
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
    st.caption("Cargue un escenario para explorar el sistema:")
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
**Motor:** Encadenamiento hacia adelante con CWA (supuesto de mundo cerrado).

**Certeza combinada:**
`P(A∨B) = 1 − (1−P(A))·(1−P(B))`

**35 reglas** organizadas en 10 grupos. **20 diagnósticos** posibles.
        """)
    st.divider()
    st.caption("Galarza & Solano · 2026")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">SISTEMA BASADO EN CONOCIMIENTO · ACTIVIDAD 4</div>
  <h1>🔍 Diagnóstico de Envíos DIAN / RNDC</h1>
  <p>Responda las preguntas paso a paso · El sistema identificará la causa del problema automáticamente</p>
</div>
""", unsafe_allow_html=True)

# ── Paso actual ───────────────────────────────────────────────────────────────
tipo_label = st.session_state.get("ej_tipo")
env_dian   = st.session_state.get("ej_dian", False)
env_rndc   = st.session_state.get("ej_rndc", False)

paso = (4 if st.session_state.resultado else
        3 if (tipo_label and (env_dian or env_rndc)) else
        2 if tipo_label else 1)
st.markdown(_step_bar(paso), unsafe_allow_html=True)

col_form, col_res = st.columns([1, 1], gap="large")

# ════════════════════════════════════════════════════════════════════════════
# COLUMNA IZQUIERDA — Formulario
# ════════════════════════════════════════════════════════════════════════════
with col_form:
    # Paso 1 — Tipo de documento
    st.markdown('<p style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:.6px;color:#64748b;margin:0 0 .4rem">🔵 PASO 1 — TIPO DE DOCUMENTO</p>',
                unsafe_allow_html=True)
    idx = list(TIPOS_MAP.keys()).index(tipo_label) if tipo_label in TIPOS_MAP else None
    tipo_label = st.radio(
        "Tipo", list(TIPOS_MAP.keys()), index=idx, key="ej_tipo",
        label_visibility="collapsed",
        help="Seleccione el tipo de documento que generó el error.",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    tipo = TIPOS_MAP.get(tipo_label) if tipo_label else None

    if not tipo:
        st.info("👆 Seleccione el tipo de documento para continuar.")
        st.stop()

    # Paso 2 — Destino
    st.markdown('<p style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:.6px;color:#64748b;margin:0 0 .4rem">🟣 PASO 2 — DESTINO DEL ENVÍO</p>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    env_dian = c1.checkbox("🏛️  Enviando a la DIAN", key="ej_dian",
                           help="La DIAN procesa facturas electrónicas y notas crédito.")
    env_rndc = c2.checkbox("🗂️  Enviando al RNDC",  key="ej_rndc",
                           help="El RNDC procesa manifiestos de carga y remesas de transporte.")
    st.markdown("<br>", unsafe_allow_html=True)

    if not env_dian and not env_rndc:
        st.warning("Seleccione al menos un destino para continuar.")
        st.stop()

    # Paso 3 — Síntomas
    st.markdown('<p style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:.6px;color:#64748b;margin:0 0 .4rem">🔷 PASO 3 — SÍNTOMAS OBSERVADOS</p>',
                unsafe_allow_html=True)

    # 3a · Conectividad
    with st.expander("🌐  Conectividad e internet", expanded=True):
        internet  = st.checkbox("Tiene conexión a internet",                            key="ej_internet", value=True,
                                help="¿Puede abrir páginas web desde este equipo ahora?")
        errorcon  = st.checkbox("Hubo error de conexión al servicio",                   key="ej_errorcon",
                                help="El sistema mostró un error al intentar comunicarse con la DIAN o el RNDC.")
        timeout   = st.checkbox("El envío venció el tiempo de espera (timeout)",        key="ej_timeout",
                                help="El envío se inició pero el servidor no respondió en el tiempo esperado.")
        falla_soap = False
        if env_rndc:
            falla_soap = st.checkbox("El servicio RNDC respondió con una falla SOAP",   key="ej_soap",
                                     help="El RNDC devolvió un error de protocolo SOAP.")

    # 3b · Estado del envío
    with st.expander("📬  Estado del envío", expanded=True):
        rechazado = st.checkbox("El servicio rechazó el documento",                     key="ej_rechazado",
                                help="El servicio externo recibió el documento pero lo rechazó explícitamente.")
        duplicado = st.checkbox("Este documento ya había sido enviado antes",            key="ej_dup",
                                help="Usted o alguien más ya envió este mismo documento anteriormente.")

    # 3c · Certificado y numeración (solo DIAN)
    cert_vigente = res_vigente = num_rango = True
    if env_dian and tipo in ("Factura", "NotaCredito"):
        with st.expander("🔏  Certificado y numeración DIAN", expanded=True):
            cert_vigente = st.checkbox("El certificado digital está vigente",           key="ej_cert", value=True,
                                       help="El certificado digital para firmar documentos no ha expirado.")
            if tipo == "Factura":
                res_vigente = st.checkbox("La resolución de numeración está vigente",   key="ej_resol", value=True,
                                          help="La resolución DIAN que autoriza el rango de numeración vigente.")
                num_rango   = st.checkbox("El número está dentro del rango autorizado", key="ej_rango", value=True,
                                          help="El número de la factura cae dentro del rango de la resolución.")

    # 3d · Entidades (multiselect)
    tercero_ok = propietario_ok = cliente_ok = True
    destinatario_ok = remitente_ok = vehiculo_ok = facturable_ok = True
    opciones_ent: list = []
    if tipo == "Manifiesto" and env_rndc:
        opciones_ent = ["Tercero","Propietario del vehículo","Cliente",
                        "Destinatario","Remitente","Vehículo","Facturable"]
    elif tipo == "Remesa" and env_rndc:
        opciones_ent = ["Tercero","Destinatario","Facturable"]
    elif tipo in ("Factura","NotaCredito") and env_dian:
        opciones_ent = ["Facturable","Tercero"]
    elif tipo in ("Factura","NotaCredito") and env_rndc:
        opciones_ent = ["Facturable"]

    if opciones_ent:
        with st.expander("👥  Datos de entidades", expanded=True):
            st.caption("Seleccione las entidades con datos incorrectos. Si todo está bien, deje vacío.")
            ent_mal = st.multiselect(
                "Entidades con problemas", opciones_ent,
                default=st.session_state.get("ej_ent_mal", []),
                key="ej_ent_mal", placeholder="Ninguna — todo correcto",
                help="Marque solo las entidades cuya información está mal diligenciada.",
            )
            tercero_ok      = "Tercero"               not in ent_mal
            propietario_ok  = "Propietario del vehículo" not in ent_mal
            cliente_ok      = "Cliente"               not in ent_mal
            destinatario_ok = "Destinatario"          not in ent_mal
            remitente_ok    = "Remitente"             not in ent_mal
            vehiculo_ok     = "Vehículo"              not in ent_mal
            facturable_ok   = "Facturable"            not in ent_mal

    # 3e · Condiciones especiales
    fact_aceptada = tipo12 = False
    fact_consist = coord_ok = destino_rndc_ok = True
    conds_especiales = any([
        tipo == "NotaCredito" and env_dian,
        tipo in ("Factura","NotaCredito") and env_rndc,
        tipo == "Remesa" and env_rndc,
    ])
    if conds_especiales:
        with st.expander("🔧  Condiciones especiales", expanded=False):
            if tipo == "NotaCredito" and env_dian:
                fact_aceptada = st.checkbox("La factura asociada ya fue aceptada por el cliente",
                                            key="ej_factaceptada",
                                            help="El cliente ya respondió con aceptación a la factura original.")
            if tipo in ("Factura","NotaCredito") and env_rndc:
                tipo12        = st.checkbox("El documento es de tipo 12 (transporte)", key="ej_tipo12",
                                            help="El código de tipo en el XML es 12 — documentos de transporte.")
                fact_consist  = st.checkbox("Los datos del facturable en el XML coinciden con la remesa",
                                            key="ej_fconsist", value=True,
                                            help="El XML generado contiene los mismos datos del facturable que la remesa.")
            if tipo == "Remesa" and env_rndc:
                coord_ok       = st.checkbox("Las coordenadas del destino son coherentes con la ciudad",
                                             key="ej_coord", value=True,
                                             help="Las coordenadas GPS corresponden al municipio de destino.")
                destino_rndc_ok = st.checkbox("El municipio de destino existe en el catálogo del RNDC",
                                              key="ej_destrndc", value=True,
                                              help="El municipio está correctamente registrado en el catálogo oficial.")

    st.markdown("")

    # Botón diagnosticar
    if st.button("🔍  Diagnosticar ahora", type="primary", use_container_width=True):
        hechos = [(tipo, True), ("Documento", True)]
        if env_dian: hechos.append(("EnvioDian", True))
        if env_rndc: hechos.append(("EnvioRNDC", True))
        for pred, val in [
            ("TieneInternet", internet),       ("ErrorConexion", errorcon),
            ("TimeoutEnvio", timeout),         ("FallaSOAP", falla_soap),
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
                    "ok": True, "diagnosticos": diagnosticos,
                    "aplicadas": aplicadas, "certezas": certezas,
                    "hechos": hechos, "finales": finales,
                    "tipo_label": tipo_label, "env_dian": env_dian, "env_rndc": env_rndc,
                }
            except ValueError as e:
                st.session_state.resultado = {"ok": False, "error": str(e)}
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# COLUMNA DERECHA — Resultados
# ════════════════════════════════════════════════════════════════════════════
with col_res:
    res = st.session_state.resultado

    # ── Sin diagnóstico aún: resumen en tiempo real ───────────────────────
    if res is None:
        tipo_txt = tipo_label.strip() if tipo_label else None
        dest_txt = " + ".join(filter(None,
            ["🏛️ DIAN" if env_dian else "", "🗂️ RNDC" if env_rndc else ""]))

        st.markdown("### 📊 Diagnóstico")
        if not tipo_txt:
            st.markdown("""
            <div style="background:white;border-radius:14px;padding:2rem;text-align:center;
                        box-shadow:0 1px 3px rgba(0,0,0,.07);border:2px dashed #e2e8f0;">
                <div style="font-size:3rem">📋</div>
                <h3 style="color:#1e293b;margin:.3rem 0">Configura tu consulta</h3>
                <p style="color:#64748b;font-size:.88rem;margin:.5rem 0 0">
                    Completa los pasos y presiona<br>
                    <strong style="color:#1d4ed8">Diagnosticar ahora</strong>
                </p>
            </div>""", unsafe_allow_html=True)
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
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:1.3rem;
                        box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:.8rem;">
                <div style="font-size:.72rem;font-weight:700;text-transform:uppercase;
                            letter-spacing:.6px;color:#64748b;margin-bottom:.8rem">📋 RESUMEN DE TU CONSULTA</div>
                {rows}
                <p style="font-size:.82rem;color:#94a3b8;margin:.9rem 0 0;text-align:center">
                    👆 Presiona <strong style="color:#1d4ed8">Diagnosticar ahora</strong>
                </p>
            </div>""", unsafe_allow_html=True)
        st.stop()

    # ── Error de validación ───────────────────────────────────────────────
    st.markdown("### 📊 Diagnóstico")
    if not res["ok"]:
        st.error(f"**Error en los datos:** {res['error']}")
        st.stop()

    diagnosticos = res["diagnosticos"]
    aplicadas    = res["aplicadas"]
    certezas     = res["certezas"]
    hechos_orig  = res["hechos"]
    finales_all  = res["finales"]
    errores      = [d for d in diagnosticos if d[0] not in EXITOS]
    exitos       = [d for d in diagnosticos if d[0] in EXITOS]
    conflictos   = detectar_conflictos(diagnosticos)

    tipo_txt = res["tipo_label"].strip()
    dest_txt = " + ".join(filter(None,
        ["DIAN" if res["env_dian"] else "", "RNDC" if res["env_rndc"] else ""]))

    # ── Banner resumen ────────────────────────────────────────────────────
    if errores:
        n = len(errores)
        st.markdown(f"""
        <div style="background:#fef2f2;border-left:5px solid #ef4444;border-radius:14px;
                    padding:1.1rem 1.3rem;margin-bottom:.8rem;box-shadow:0 1px 3px rgba(0,0,0,.07)">
            <div style="font-size:1.7rem">❌</div>
            <div style="font-weight:800;font-size:1.1rem;color:#1e293b;margin:.2rem 0">
                {n} problema{"s" if n>1 else ""} detectado{"s" if n>1 else ""}
            </div>
            <div style="font-size:.85rem;color:#64748b">{tipo_txt} → {dest_txt}</div>
        </div>""", unsafe_allow_html=True)
    elif exitos:
        st.markdown(f"""
        <div style="background:#f0fdf4;border-left:5px solid #22c55e;border-radius:14px;
                    padding:1.1rem 1.3rem;margin-bottom:.8rem;box-shadow:0 1px 3px rgba(0,0,0,.07)">
            <div style="font-size:1.7rem">✅</div>
            <div style="font-weight:800;font-size:1.1rem;color:#1e293b;margin:.2rem 0">
                Envío procesado correctamente
            </div>
            <div style="font-size:.85rem;color:#64748b">{tipo_txt} → {dest_txt}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#f8fafc;border-left:5px solid #94a3b8;border-radius:14px;
                    padding:1.1rem 1.3rem;margin-bottom:.8rem;box-shadow:0 1px 3px rgba(0,0,0,.07)">
            <div style="font-size:1.7rem">⚠️</div>
            <div style="font-weight:700;font-size:1rem;color:#1e293b;margin:.2rem 0">Sin diagnóstico concluyente</div>
            <div style="font-size:.85rem;color:#64748b">Los síntomas no coinciden con ningún patrón conocido. Verifique los datos.</div>
        </div>""", unsafe_allow_html=True)

    # ── Métricas ──────────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.metric("Problemas",         len(errores))
    m2.metric("Reglas disparadas", len(aplicadas))
    m3.metric("Éxitos",            len(exitos))

    # ── Resultados exitosos con ¿Por qué? ────────────────────────────────
    if exitos:
        st.markdown("#### ✅ Resultados exitosos")
        for d in exitos:
            cert  = certezas.get(d, 1.0)
            titulo, accion = DESCRIPCIONES_DIAGNOSTICO.get(d[0], (d[0], ""))
            st.markdown(_dcard("ok", titulo, accion, cert), unsafe_allow_html=True)
            with st.expander("🔍  ¿Por qué se llegó a esta conclusión?"):
                explicacion = porque(d[0], REGLAS, aplicadas, finales_all)
                if explicacion:
                    for item in explicacion:
                        st.markdown(f"**Regla `{item['regla']}`** — {item['descripcion']}  "
                                    f"(certeza: **{item['certeza']:.0%}**)")
                        for cond in item["condiciones"]:
                            icono = "✅" if cond["valor_esperado"] else "❌"
                            valor = "debe ser SÍ" if cond["valor_esperado"] else "debe ser NO"
                            st.markdown(f"&nbsp;&nbsp;{icono} `{cond['predicado']}` — {valor}")
                        st.markdown("---")
                else:
                    st.caption("Sin información de razonamiento disponible.")

    # ── Diagnósticos de error con ¿Por qué? ──────────────────────────────
    if errores:
        st.markdown("#### ❌ Problemas detectados")
        for d in errores:
            cert  = certezas.get(d, 1.0)
            titulo, accion = DESCRIPCIONES_DIAGNOSTICO.get(d[0], (d[0], ""))
            st.markdown(_dcard("err", titulo, accion, cert), unsafe_allow_html=True)
            with st.expander("🔍  ¿Por qué se llegó a esta conclusión?"):
                explicacion = porque(d[0], REGLAS, aplicadas, finales_all)
                if explicacion:
                    for item in explicacion:
                        st.markdown(f"**Regla `{item['regla']}`** — {item['descripcion']}  "
                                    f"(certeza: **{item['certeza']:.0%}**)")
                        for cond in item["condiciones"]:
                            icono = "✅" if cond["valor_esperado"] else "❌"
                            valor = "debe ser SÍ" if cond["valor_esperado"] else "debe ser NO"
                            st.markdown(f"&nbsp;&nbsp;{icono} `{cond['predicado']}` — {valor}")
                        st.markdown("---")
                else:
                    st.caption("Sin información de razonamiento disponible.")

    # ── Conflictos ────────────────────────────────────────────────────────
    if conflictos:
        st.markdown("#### ⚠️ Advertencia")
        for grupo in conflictos:
            st.markdown(_dcard("warn",
                               "Diagnósticos contradictorios detectados",
                               f"Diagnósticos mutuamente excluyentes: {' vs '.join(grupo)}. "
                               "Revise los síntomas ingresados.", 1.0),
                        unsafe_allow_html=True)

    if not errores and not exitos:
        st.info("Ninguna regla fue disparada. Verifique que los síntomas estén completos.")

    # ── Detalle técnico ───────────────────────────────────────────────────
    with st.expander(f"🔧  Detalle técnico — {len(aplicadas)} regla(s) disparada(s)"):
        if aplicadas:
            for nombre in aplicadas:
                cert_r = next((r["certeza"] for r in REGLAS if r["nombre"] == nombre), 1.0)
                desc   = DESCRIPCIONES_REGLAS.get(nombre, nombre)
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:.5rem;margin:.3rem 0;font-size:.85rem;">'
                    f'<code style="background:#f1f5f9;padding:.1rem .4rem;border-radius:5px">{nombre}</code>'
                    f'<span style="color:#475569">{desc}</span>'
                    f'{_badge(cert_r)}</div>', unsafe_allow_html=True)
        else:
            st.caption("Ninguna regla fue disparada.")

    st.divider()
    st.caption("SBC · Actividad 4 · IA II · Los Libertadores · Galarza & Solano · 2026")
