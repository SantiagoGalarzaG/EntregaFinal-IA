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
# SISTEMA DE ICONOS SVG
# ─────────────────────────────────────────────────────────────────────────────

_ICONS = {
    "search":         '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>',
    "document":       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    "file-minus":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="15" x2="15" y2="15"/></svg>',
    "truck":          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    "package":        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    "send":           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
    "lock":           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "users":          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "building":       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "database":       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
    "zap":            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "refresh-cw":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
    "info":           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "check":          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "check-circle":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "x-circle":       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    "alert-triangle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "clipboard-list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/></svg>',
    "bar-chart-2":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "lightbulb":      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
    "cpu":            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
    "activity":       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    "terminal":       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>',
    "layers":         '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
    "arrow-right":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "target":         '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "dot":            '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="4"/></svg>',
}


def _svg(name, size=16, color="currentColor"):
    raw = _ICONS.get(name, "")
    if not raw:
        return ""
    return raw.replace(
        "<svg ",
        f'<svg width="{size}" height="{size}" style="display:inline-block;vertical-align:middle;flex-shrink:0;color:{color}" ',
    )


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES UI
# ─────────────────────────────────────────────────────────────────────────────

TIPOS_MAP = {
    "Factura electronica":  "Factura",
    "Nota credito":         "NotaCredito",
    "Remesa":               "Remesa",
    "Manifiesto de carga":  "Manifiesto",
}

_TIPO_ICON = {
    "Factura electronica":  "document",
    "Nota credito":         "file-minus",
    "Remesa":               "truck",
    "Manifiesto de carga":  "package",
}

_DOC_META = {
    "Factura electronica":  ("document",  "dci-blue",   "Cobro de bienes o servicios a un cliente"),
    "Nota credito":         ("file-minus","dci-violet",  "Devolucion, descuento o anulacion de factura"),
    "Remesa":               ("truck",     "dci-green",  "Despacho de mercancia en transporte terrestre"),
    "Manifiesto de carga":  ("package",   "dci-amber",  "Registro oficial de carga en el RNDC"),
}

EJEMPLOS = {
    "DIAN caida": dict(
        ej_tipo="Factura electronica", ej_dian=True,  ej_rndc=False,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=True, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "Sin internet": dict(
        ej_tipo="Factura electronica", ej_dian=True,  ej_rndc=False,
        ej_internet=False, ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "Certificado vencido": dict(
        ej_tipo="Factura electronica", ej_dian=True,  ej_rndc=False,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=False, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "Manifiesto exitoso": dict(
        ej_tipo="Manifiesto de carga", ej_dian=False, ej_rndc=True,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=[], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "Remesa — tercero invalido": dict(
        ej_tipo="Remesa", ej_dian=False, ej_rndc=True,
        ej_internet=True,  ej_errorcon=False, ej_timeout=False, ej_soap=False,
        ej_rechazado=False, ej_dup=False,
        ej_cert=True, ej_resol=True, ej_rango=True,
        ej_ent_mal=["Tercero"], ej_factaceptada=False, ej_tipo12=False,
        ej_fconsist=True, ej_coord=True, ej_destrndc=True,
    ),
    "Documento duplicado": dict(
        ej_tipo="Remesa", ej_dian=False, ej_rndc=True,
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
# CSS — SISTEMA DE DISENO
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif !important;
}

[data-testid="stAppViewContainer"] { background: #f1f5f9; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1380px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d1a 0%, #0f172a 60%, #0d1b35 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown p { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.48rem 0.85rem !important;
    margin-bottom: 3px !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(37,99,235,0.2) !important;
    color: #93c5fd !important;
    border-color: rgba(59,130,246,0.3) !important;
    transform: translateX(2px) !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 40%, #1d4ed8 100%);
    padding: 1.85rem 2.1rem 1.7rem;
    border-radius: 18px;
    margin: 0 0 1.25rem;
    box-shadow: 0 10px 40px rgba(8,13,26,0.35), 0 1px 0 rgba(255,255,255,0.08) inset;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
}
.hero::after {
    content: "";
    position: absolute; top: -50%; right: -5%;
    width: 55%; height: 220%;
    background: radial-gradient(ellipse, rgba(99,179,237,0.18) 0%, transparent 65%);
    pointer-events: none;
}
/* Garantizar contraste: anular override oscuro de stMain */
.hero, .hero * { color: #ffffff !important; }
.hero .hero-eyebrow,
.hero .hero-eyebrow span { color: #bfdbfe !important; }
.hero .hero-sub { color: #bfdbfe !important; }
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    color: #bfdbfe !important;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0.22rem 0.8rem 0.22rem 0.55rem;
    border-radius: 999px;
    margin-bottom: 0.85rem;
    position: relative; z-index: 1;
}
.hero-status-dot {
    width: 6px; height: 6px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
    animation: pulse-green 2s infinite;
}
.hero-icon-wrap {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 46px; height: 46px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 14px;
    margin-bottom: 0.9rem;
    position: relative; z-index: 1;
}

/* ── Barra de pasos ── */
.step-bar {
    display: flex;
    align-items: center;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.step-item { display: flex; flex-direction: column; align-items: center; min-width: 80px; }
.step-num {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem; font-weight: 700; margin-bottom: 0.3rem;
}
.step-done    { background: #16a34a; color: #ffffff !important; box-shadow: 0 2px 8px rgba(22,163,74,0.4); }
.step-active  { background: #1d4ed8; color: #ffffff !important; box-shadow: 0 0 0 4px #dbeafe, 0 2px 10px rgba(29,78,216,0.4); }
.step-pending { background: #f1f5f9; color: #94a3b8 !important; border: 2px solid #e2e8f0; }
.step-lbl { font-size: 0.67rem; color: #94a3b8 !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap; }
.step-lbl-done   { color: #16a34a !important; }
.step-lbl-active { color: #1d4ed8 !important; }
.step-line { flex: 1; height: 2px; margin: 0 0.3rem 1.75rem; min-width: 20px; border-radius: 1px; }
.line-done   { background: #16a34a; }
.line-active { background: linear-gradient(90deg, #16a34a 0%, #bfdbfe 100%); }
.line-pend   { background: #e2e8f0; }

/* ── Cabeceras de seccion ── */
.sec-hdr { display: flex; align-items: center; gap: 0.55rem; margin: 0 0 0.7rem; }
.sec-hdr-icon { display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 7px; flex-shrink: 0; }
.ic-blue   { background: #dbeafe; color: #1d4ed8; }
.ic-indigo { background: #e0e7ff; color: #4338ca; }
.ic-slate  { background: #f1f5f9; color: #475569; }
.sec-hdr-label { font-size: 0.69rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px; color: #64748b !important; flex: 1; }
.sec-hdr-step  { font-size: 0.67rem; font-weight: 700; color: #1d4ed8 !important; background: #dbeafe; padding: 0.12rem 0.5rem; border-radius: 5px; }

/* ── Forzar texto oscuro en area principal (excluye .hero) ── */
[data-testid="stMain"] p,
[data-testid="stMain"] span,
[data-testid="stMain"] label,
[data-testid="stMain"] li { color: #1e293b; }
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span,
[data-testid="stCheckbox"] label, [data-testid="stCheckbox"] label p, [data-testid="stCheckbox"] label span,
[data-testid="stRadio"] label, [data-testid="stRadio"] label p, [data-testid="stRadio"] label span,
[data-testid="stMultiSelect"] label, [data-testid="stMultiSelect"] p,
[data-testid="stSelectbox"] label { color: #1e293b !important; }
[data-testid="stCaptionContainer"] p, small { color: #64748b !important; }
/* Restaurar hero sobre el override anterior */
.hero, .hero * { color: #ffffff !important; }
.hero .hero-eyebrow, .hero .hero-eyebrow span, .hero .hero-sub { color: #bfdbfe !important; }

/* ── Expanders ── */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 11px !important;
    overflow: hidden; background: #ffffff !important;
    margin-bottom: 0.6rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
[data-testid="stExpander"] summary { background: #f8fafc !important; font-weight: 600; color: #1e293b !important; font-size: 0.87rem !important; padding: 0.72rem 1.1rem !important; }
[data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span { color: #1e293b !important; }
[data-testid="stExpander"] > div, [data-testid="stExpander"] [data-testid="stVerticalBlock"] { background: #ffffff !important; }

/* ── Tarjetas de diagnostico ── */
.dcard { border-radius: 12px; padding: 1rem 1.15rem 0.9rem; margin: 0.45rem 0; animation: fadeUp 0.25s ease; }
.dcard-ok   { background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; }
.dcard-err  { background: #fef2f2; border: 1px solid #fecaca; border-left: 4px solid #dc2626; }
.dcard-warn { background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #d97706; }
.dcard-top  { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.45rem; }
.dcard-title { font-weight: 700; font-size: 0.92rem; color: #0f172a; margin: 0; line-height: 1.35; }
.dcard-action { display: inline-flex; align-items: center; gap: 0.35rem; font-size: 0.79rem; color: #1e40af; background: #eff6ff; border: 1px solid #bfdbfe; padding: 0.27rem 0.7rem; border-radius: 6px; font-weight: 500; margin-top: 0.2rem; }
.dcard-action-warn { display: inline-flex; align-items: center; gap: 0.35rem; font-size: 0.79rem; color: #92400e; background: #fef3c7; border: 1px solid #fde68a; padding: 0.27rem 0.7rem; border-radius: 6px; font-weight: 500; margin-top: 0.2rem; }

/* ── Badge de certeza ── */
.cbadge { display: inline-flex; align-items: center; gap: 0.2rem; font-size: 0.69rem; font-weight: 700; padding: 0.12rem 0.55rem; border-radius: 999px; white-space: nowrap; flex-shrink: 0; }
.cbadge-high { background: #dcfce7; color: #15803d; }
.cbadge-med  { background: #fef9c3; color: #854d0e; }
.cbadge-low  { background: #fee2e2; color: #991b1b; }

/* ── Panel de resumen ── */
.summary-panel { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 0.8rem; }
.summary-hdr { display: flex; align-items: center; gap: 0.45rem; font-size: 0.67rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px; color: #64748b; margin: 0 0 0.8rem; }
.summary-row { display: flex; align-items: center; gap: 0.55rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.48rem 0.8rem; margin: 0.28rem 0; font-size: 0.86rem; color: #334155; }
.summary-row-warn { border-color: #fca5a5 !important; background: #fef2f2 !important; }
.summary-lbl { font-weight: 600; min-width: 80px; color: #64748b; font-size: 0.77rem; flex-shrink: 0; }

/* ── Banner de resultado ── */
.result-banner { display: flex; align-items: center; gap: 1rem; border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 0.85rem; }
.rb-err  { background: #fef2f2; border: 1px solid #fecaca; border-left: 5px solid #dc2626; }
.rb-ok   { background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 5px solid #16a34a; }
.rb-info { background: #f8fafc; border: 1px solid #e2e8f0; border-left: 5px solid #94a3b8; }
.rb-icon { flex-shrink: 0; width: 42px; height: 42px; border-radius: 11px; display: flex; align-items: center; justify-content: center; }
.rbi-err  { background: #fee2e2; color: #dc2626; }
.rbi-ok   { background: #dcfce7; color: #16a34a; }
.rbi-info { background: #f1f5f9; color: #64748b; }
.rb-title { font-weight: 800; font-size: 1.05rem; color: #0f172a; margin: 0 0 0.15rem; }
.rb-sub   { font-size: 0.82rem; color: #64748b; margin: 0; }

/* ── Cabeceras de resultados ── */
.res-hdr { display: flex; align-items: center; gap: 0.5rem; padding: 0.55rem 0.9rem; border-radius: 8px; margin: 0.8rem 0 0.5rem; font-weight: 700; font-size: 0.84rem; }
.res-hdr-ok   { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.res-hdr-err  { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.res-hdr-warn { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }

/* ── Metricas ── */
[data-testid="stMetricLabel"] p { color: #64748b !important; font-size: 0.74rem !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
[data-testid="stMetricValue"] div { color: #0f172a !important; font-weight: 800 !important; font-size: 1.55rem !important; }
[data-testid="metric-container"] { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 11px !important; padding: 0.75rem 1rem !important; }

/* ── Boton principal ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
    border: none !important; border-radius: 10px !important;
    font-size: 0.94rem !important; font-weight: 700 !important; padding: 0.72rem 1.2rem !important;
    box-shadow: 0 4px 16px rgba(29,78,216,0.35) !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
    box-shadow: 0 6px 22px rgba(29,78,216,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Guia de onboarding ── */
.guide-panel { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.4rem 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.guide-panel-title { font-size: 0.93rem; font-weight: 700; color: #0f172a; margin: 0 0 1rem; display: flex; align-items: center; gap: 0.5rem; }
.guide-step { display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 1rem; animation: fadeUp 0.3s ease both; }
.guide-step:last-child { margin-bottom: 0; }
.guide-step-num { flex-shrink: 0; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 800; background: #1d4ed8; color: #ffffff; margin-top: 1px; }
.guide-step-num-done { background: #16a34a; }
.guide-step-body { flex: 1; }
.guide-step-title { font-size: 0.85rem; font-weight: 700; color: #1e293b; margin: 0 0 .18rem; }
.guide-step-desc  { font-size: 0.8rem; color: #64748b; margin: 0; line-height: 1.5; }

/* ── Tarjetas de tipo de documento ── */
.doc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-bottom: 0.75rem; }
.doc-card { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 0.7rem 0.8rem; display: flex; align-items: flex-start; gap: 0.6rem; }
.doc-card-active { background: #eff6ff; border-color: #1d4ed8; }
.doc-card-icon { flex-shrink: 0; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }
.dci-blue   { background: #dbeafe; color: #1d4ed8; }
.dci-violet { background: #ede9fe; color: #6d28d9; }
.dci-green  { background: #dcfce7; color: #16a34a; }
.dci-amber  { background: #fef3c7; color: #d97706; }
.doc-card-text { flex: 1; }
.doc-card-name { font-size: 0.81rem; font-weight: 700; color: #1e293b; margin: 0 0 .12rem; }
.doc-card-desc { font-size: 0.74rem; color: #64748b; margin: 0; line-height: 1.4; }

/* ── Tip inline ── */
.tip-box { display: flex; align-items: flex-start; gap: 0.5rem; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 0.55rem 0.8rem; margin: 0.55rem 0; font-size: 0.81rem; color: #0c4a6e; line-height: 1.5; }
.tip-box-warn { background: #fffbeb; border-color: #fde68a; color: #78350f; }
.tip-box-icon { flex-shrink: 0; margin-top: 1px; }

/* ── Destino cards ── */
.dest-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin: 0.4rem 0 0.75rem; }
.dest-card { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 0.75rem 0.85rem; }
.dest-card-icon { display: flex; align-items: center; gap: .45rem; margin-bottom: .4rem; }
.dest-card-name { font-size: 0.82rem; font-weight: 700; color: #1e293b; }
.dest-card-desc { font-size: 0.75rem; color: #64748b; line-height: 1.45; margin: 0; }

/* ── Hint en expander ── */
.exp-hint { font-size: 0.79rem; color: #64748b; background: #f8fafc; border-radius: 7px; padding: 0.45rem 0.7rem; margin-bottom: 0.65rem; line-height: 1.5; border-left: 3px solid #e2e8f0; }

/* ── Detalle tecnico ── */
.tech-row { display: flex; align-items: center; gap: 0.5rem; margin: 0.2rem 0; padding: 0.3rem 0.4rem; border-radius: 7px; transition: background 0.1s; }
.tech-row:hover { background: #f8fafc; }
.tech-code { background: #f1f5f9; color: #475569; padding: 0.1rem 0.45rem; border-radius: 5px; font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.76rem; border: 1px solid #e2e8f0; flex-shrink: 0; }
.tech-desc { color: #475569; font-size: 0.82rem; flex: 1; }

/* ── Animaciones ── */
@keyframes fadeUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse-green {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(74,222,128,0); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 4px rgba(74,222,128,0.2); }
}
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# HTML HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _step_bar(step):
    def circle(n, label):
        if n < step:
            cls = "step-done"; icon = _svg("check", 16, "white"); lbl_cls = "step-lbl step-lbl-done"
        elif n == step:
            cls = "step-active"; icon = f'<span style="font-size:.82rem;font-weight:800;color:white">{n}</span>'; lbl_cls = "step-lbl step-lbl-active"
        else:
            cls = "step-pending"; icon = f'<span style="font-size:.82rem;font-weight:700;color:#94a3b8">{n}</span>'; lbl_cls = "step-lbl"
        return (f'<div class="step-item"><div class="step-num {cls}">{icon}</div>'
                f'<div class="{lbl_cls}">{label}</div></div>')
    def line(n):
        cls = "line-done" if n < step else ("line-active" if n == step else "line-pend")
        return f'<div class="step-line {cls}"></div>'
    steps = [(1,"Documento"),(2,"Destino"),(3,"Sintomas"),(4,"Resultado")]
    html = '<div class="step-bar">'
    for i, (n, lbl) in enumerate(steps):
        html += circle(n, lbl)
        if i < len(steps) - 1: html += line(n)
    return html + "</div>"


def _badge(cert):
    cls = "cbadge-high" if cert >= 0.95 else ("cbadge-med" if cert >= 0.80 else "cbadge-low")
    dot_color = "#16a34a" if cert >= 0.95 else ("#d97706" if cert >= 0.80 else "#dc2626")
    return f'<span class="cbadge {cls}">{_svg("dot", 7, dot_color)}{cert:.0%}</span>'


def _dcard(kind, titulo, accion, cert):
    action_cls = "dcard-action" if kind in ("ok", "err") else "dcard-action-warn"
    return (f'<div class="dcard dcard-{kind}">'
            f'<div class="dcard-top"><p class="dcard-title">{titulo}</p>{_badge(cert)}</div>'
            f'<span class="{action_cls}">{_svg("lightbulb", 13)} {accion}</span></div>')


def _result_banner(kind, icon_name, title, subtitle):
    return (f'<div class="result-banner rb-{kind}">'
            f'<div class="rb-icon rbi-{kind}">{_svg(icon_name, 22)}</div>'
            f'<div><p class="rb-title">{title}</p><p class="rb-sub">{subtitle}</p></div></div>')


def _sec_hdr(icon, label, step_n, ic_cls="ic-blue"):
    step_badge = f'<span class="sec-hdr-step">Paso {step_n}</span>' if step_n else ""
    return (f'<div class="sec-hdr"><span class="sec-hdr-icon {ic_cls}">{_svg(icon, 14)}</span>'
            f'<span class="sec-hdr-label">{label}</span>{step_badge}</div>')


def _res_hdr(kind, icon_name, text, count=None):
    cnt = (f' <span style="background:rgba(0,0,0,0.08);padding:.08rem .45rem;border-radius:999px;font-size:.72rem">{count}</span>' if count else "")
    return f'<div class="res-hdr res-hdr-{kind}">{_svg(icon_name, 15)}<span>{text}{cnt}</span></div>'


def _doc_guide(selected):
    cards = ""
    for name, (icon, ic_cls, desc) in _DOC_META.items():
        active = "doc-card-active" if name == selected else ""
        cards += (f'<div class="doc-card {active}">'
                  f'<span class="doc-card-icon {ic_cls}">{_svg(icon, 16)}</span>'
                  f'<span class="doc-card-text">'
                  f'<p class="doc-card-name">{name}</p>'
                  f'<p class="doc-card-desc">{desc}</p></span></div>')
    return f'<div class="doc-grid">{cards}</div>'


def _dest_guide():
    return (f'<div class="dest-grid">'
            f'<div class="dest-card"><div class="dest-card-icon">{_svg("building",15,"#1d4ed8")}'
            f'<span class="dest-card-name">DIAN</span></div>'
            f'<p class="dest-card-desc">Autoridad tributaria. Procesa <strong>facturas electronicas</strong> y <strong>notas credito</strong>.</p></div>'
            f'<div class="dest-card"><div class="dest-card-icon">{_svg("database",15,"#16a34a")}'
            f'<span class="dest-card-name">RNDC</span></div>'
            f'<p class="dest-card-desc">Registro de Carga. Procesa <strong>remesas</strong> y <strong>manifiestos de carga</strong>.</p></div></div>')


def _tip(text, warn=False):
    cls = "tip-box-warn" if warn else ""
    icon = _svg("alert-triangle", 14, "#d97706") if warn else _svg("info", 14, "#0ea5e9")
    return f'<div class="tip-box {cls}"><span class="tip-box-icon">{icon}</span><span>{text}</span></div>'


def _exp_hint(text):
    return f'<div class="exp-hint">{text}</div>'


def _guide_panel(paso):
    steps = [
        ("document",    "Seleccione el tipo de documento",
         "Identifique si es una factura, nota credito, remesa o manifiesto."),
        ("send",        "Indique el destino del envio",
         "Elija si envio a la DIAN, al RNDC, o a ambos sistemas."),
        ("activity",    "Describa los sintomas observados",
         "Marque todo lo que noto en el momento del error."),
        ("bar-chart-2", "Obtenga el diagnostico",
         "Presione 'Diagnosticar ahora' — el motor explicara la causa."),
    ]
    steps_html = ""
    for i, (icon, title, desc) in enumerate(steps):
        n = i + 1
        if n < paso:
            num_cls = "guide-step-num guide-step-num-done"
            num_ico = _svg("check", 13, "white")
        else:
            num_cls = "guide-step-num"
            num_ico = str(n)
        opacity = "1" if n <= paso else "0.4"
        icon_color = "#1d4ed8" if n == paso else ("#16a34a" if n < paso else "#94a3b8")
        steps_html += (
            f'<div class="guide-step" style="opacity:{opacity}">'
            f'<div class="{num_cls}">{num_ico}</div>'
            f'<div class="guide-step-body">'
            f'<p class="guide-step-title">{_svg(icon, 13, icon_color)} {title}</p>'
            f'<p class="guide-step-desc">{desc}</p></div></div>')
    return (f'<div class="guide-panel">'
            f'<p class="guide-panel-title">{_svg("info", 16, "#1d4ed8")} Como usar este sistema</p>'
            f'{steps_html}</div>')


def _why_block(item):
    conds_html = ""
    for cond in item["condiciones"]:
        ok_c  = cond["valor_esperado"]
        ic    = _svg("check", 13, "#16a34a") if ok_c else _svg("x-circle", 13, "#dc2626")
        bg    = "#f0fdf4" if ok_c else "#fef2f2"
        bd    = "#bbf7d0" if ok_c else "#fecaca"
        valor = "debe ser SI" if ok_c else "debe ser NO"
        conds_html += (f'<div style="display:flex;align-items:center;gap:.4rem;background:{bg};'
                       f'border:1px solid {bd};border-radius:6px;padding:.28rem .65rem;'
                       f'margin:.18rem 0 .18rem .6rem;font-size:.79rem">'
                       f'{ic}<code style="background:transparent;color:#475569;font-size:.77rem">'
                       f'{cond["predicado"]}</code>'
                       f'<span style="color:#b0bec5">—</span>'
                       f'<span style="color:#475569">{valor}</span></div>')
    return (f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:9px;'
            f'padding:.7rem .95rem;margin:.35rem 0">'
            f'<div style="display:flex;align-items:center;gap:.45rem;font-size:.82rem;'
            f'font-weight:700;color:#1e293b;margin-bottom:.45rem;flex-wrap:wrap">'
            f'{_svg("terminal", 13, "#1d4ed8")}'
            f'<code style="background:#dbeafe;color:#1e40af;padding:.08rem .42rem;'
            f'border-radius:4px;font-size:.76rem">{item["regla"]}</code>'
            f'<span style="font-weight:500;color:#475569;flex:1;font-size:.81rem">{item["descripcion"]}</span>'
            f'<span>{_badge(item["certeza"])}</span></div>'
            f'{conds_html}</div>')


# ─────────────────────────────────────────────────────────────────────────────
# APP PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Diagnostico DIAN / RNDC",
    page_icon="Dx",
    layout="wide",
    initial_sidebar_state="expanded",
)
_init()
REGLAS = get_reglas()
st.markdown(CSS, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.65rem;margin-bottom:.2rem">'
        f'<span style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;'
        f'background:rgba(59,130,246,0.15);border:1px solid rgba(59,130,246,0.25);border-radius:10px;color:#60a5fa">'
        f'{_svg("search", 18)}</span>'
        f'<div><p style="font-size:.95rem;font-weight:800;color:#f1f5f9;margin:0">Diagnostico DIAN/RNDC</p>'
        f'<p style="font-size:.7rem;color:#64748b;margin:0">Sistema Experto · IA II</p></div></div>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.4rem;margin-bottom:.5rem;'
        f'font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:#64748b">'
        f'{_svg("info", 12, "#60a5fa")}<span style="color:#64748b">Guia rapida</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="font-size:.8rem;color:#cbd5e1;line-height:1.65">'
        + "".join([
            f'<div style="display:flex;gap:.55rem;margin-bottom:.55rem">'
            f'<span style="background:{bg};color:white;border-radius:50%;width:18px;height:18px;'
            f'display:flex;align-items:center;justify-content:center;font-size:.65rem;'
            f'font-weight:800;flex-shrink:0;margin-top:1px">{num}</span>'
            f'<span>{txt}</span></div>'
            for bg, num, txt in [
                ("#1d4ed8","1","Elija el <strong>tipo de documento</strong> que genero el error"),
                ("#1d4ed8","2","Indique si envio a <strong>DIAN</strong>, <strong>RNDC</strong> o ambos"),
                ("#1d4ed8","3","Marque los <strong>sintomas</strong> que observo al momento del error"),
                ("#16a34a", _svg("check",10,"white"), "Presione <strong>Diagnosticar ahora</strong>"),
            ]
        ])
        + f'</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.4rem;margin-bottom:.3rem;'
        f'font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:#64748b">'
        f'{_svg("zap", 12, "#f59e0b")}<span style="color:#64748b">Ejemplos de prueba</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("Cargue un escenario para explorar sin escribir nada:")
    for nombre in EJEMPLOS:
        if st.button(nombre, use_container_width=True, key=f"btn_{nombre}"):
            _cargar_ejemplo(nombre)
            st.rerun()

    st.divider()
    if st.button("Reiniciar formulario", use_container_width=True):
        _reset()
        st.rerun()
    st.divider()

    with st.expander("Como funciona el motor"):
        st.markdown(
            f'<div style="font-size:.82rem;color:#e2e8f0;line-height:1.65">'
            f'<div style="display:flex;gap:.5rem;align-items:flex-start;margin-bottom:.55rem">'
            f'<span style="color:#60a5fa;margin-top:2px">{_svg("cpu", 13)}</span>'
            f'<span><strong>Motor:</strong> Encadenamiento hacia adelante con CWA</span></div>'
            f'<div style="display:flex;gap:.5rem;align-items:flex-start;margin-bottom:.55rem">'
            f'<span style="color:#60a5fa;margin-top:2px">{_svg("activity", 13)}</span>'
            f'<span><strong>Certeza:</strong> P(A∨B) = 1 − (1−P(A))·(1−P(B))</span></div>'
            f'<div style="display:flex;gap:.5rem;align-items:flex-start">'
            f'<span style="color:#60a5fa;margin-top:2px">{_svg("layers", 13)}</span>'
            f'<span><strong>35 reglas</strong> · 10 grupos · <strong>20 diagnosticos</strong></span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.divider()
    st.caption("Galarza & Solano · 2026 · Los Libertadores")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="hero">'
    f'<div class="hero-icon-wrap" style="color:#ffffff">{_svg("search", 22, "white")}</div>'
    f'<div style="margin-bottom:.75rem"></div>'
    f'<div class="hero-eyebrow" style="color:#bfdbfe!important">'
    f'<span class="hero-status-dot"></span>'
    f'<span style="color:#bfdbfe">Sistema Basado en Conocimiento &middot; Actividad 4</span></div>'
    f'<h1 style="color:#ffffff!important;font-size:1.65rem;font-weight:800;'
    f'letter-spacing:-0.025em;margin:0 0 0.4rem;line-height:1.18;'
    f'text-shadow:0 2px 8px rgba(0,0,0,0.4)">'
    f'Diagn&#243;stico de Env&#237;os DIAN / RNDC</h1>'
    f'<p style="color:#bfdbfe!important;font-size:.88rem;margin:0;font-weight:400;opacity:.95">'
    f'Responda las preguntas paso a paso &mdash; '
    f'el motor de inferencia identificar&#225; la causa del problema autom&#225;ticamente</p>'
    f'</div>',
    unsafe_allow_html=True,
)

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

    # ── Paso 1 — Tipo de documento ───────────────────────────────────────
    st.markdown(_sec_hdr("document", "Tipo de documento", 1, "ic-blue"), unsafe_allow_html=True)
    st.markdown(_tip("Identifique que tipo de documento estaba enviando cuando ocurrio el error."), unsafe_allow_html=True)
    st.markdown(_doc_guide(tipo_label), unsafe_allow_html=True)
    idx = list(TIPOS_MAP.keys()).index(tipo_label) if tipo_label in TIPOS_MAP else None
    tipo_label = st.radio(
        "Seleccione el tipo:", list(TIPOS_MAP.keys()), index=idx, key="ej_tipo",
        help="El tipo de documento determina que reglas aplica el motor de diagnostico.",
    )
    st.markdown("<div style='margin-bottom:.9rem'></div>", unsafe_allow_html=True)
    tipo = TIPOS_MAP.get(tipo_label) if tipo_label else None

    if not tipo:
        st.stop()

    # ── Paso 2 — Destino ─────────────────────────────────────────────────
    st.markdown(_sec_hdr("send", "Destino del envio", 2, "ic-indigo"), unsafe_allow_html=True)
    st.markdown(_tip("A que sistema estaba enviando el documento? Puede marcar ambos si aplica."), unsafe_allow_html=True)
    st.markdown(_dest_guide(), unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    env_dian = c1.checkbox("Enviando a la DIAN", key="ej_dian",
                           help="Facturas electronicas y notas credito van a la DIAN.")
    env_rndc = c2.checkbox("Enviando al RNDC",  key="ej_rndc",
                           help="Remesas y manifiestos de carga van al RNDC.")
    st.markdown("<div style='margin-bottom:.9rem'></div>", unsafe_allow_html=True)

    if not env_dian and not env_rndc:
        st.markdown(_tip("Marque al menos un destino para continuar.", warn=True), unsafe_allow_html=True)
        st.stop()

    # ── Paso 3 — Sintomas ────────────────────────────────────────────────
    st.markdown(_sec_hdr("activity", "Sintomas observados", 3, "ic-slate"), unsafe_allow_html=True)
    st.markdown(_tip("Marque todo lo que observo al momento del error. Si no esta seguro, deje el valor predeterminado."), unsafe_allow_html=True)

    with st.expander("Conectividad e internet", expanded=True):
        st.markdown(_exp_hint("Revise el estado de la red al momento del error. Si no recuerda, deje los valores predeterminados."), unsafe_allow_html=True)
        internet   = st.checkbox("Tiene conexion a internet", key="ej_internet", value=True,
                                 help="Puede abrir paginas web desde este equipo ahora mismo.")
        errorcon   = st.checkbox("Hubo error de conexion al servicio", key="ej_errorcon",
                                 help="El sistema mostro un error al intentar comunicarse con la DIAN o el RNDC.")
        timeout    = st.checkbox("El envio vencio el tiempo de espera (timeout)", key="ej_timeout",
                                 help="El envio se inicio pero el servidor no respondio en el tiempo esperado.")
        falla_soap = False
        if env_rndc:
            falla_soap = st.checkbox("El servicio RNDC respondio con una falla SOAP", key="ej_soap",
                                     help="El RNDC devolvio un error de protocolo SOAP en la respuesta.")

    with st.expander("Estado del envio", expanded=True):
        st.markdown(_exp_hint("Indique que respuesta dio el servicio externo al recibir su documento."), unsafe_allow_html=True)
        rechazado = st.checkbox("El servicio rechazo el documento", key="ej_rechazado",
                                help="El servicio externo recibio el documento pero lo rechazo explicitamente.")
        duplicado = st.checkbox("Este documento ya habia sido enviado antes", key="ej_dup",
                                help="Usted o alguien mas ya envio este mismo documento anteriormente.")

    cert_vigente = res_vigente = num_rango = True
    if env_dian and tipo in ("Factura", "NotaCredito"):
        with st.expander("Certificado y numeracion DIAN", expanded=True):
            st.markdown(_exp_hint("Verifique el estado del certificado digital y la resolucion de numeracion en el portal DIAN o en su software."), unsafe_allow_html=True)
            cert_vigente = st.checkbox("El certificado digital esta vigente", key="ej_cert", value=True,
                                       help="El certificado digital para firmar documentos no ha expirado.")
            if tipo == "Factura":
                res_vigente = st.checkbox("La resolucion de numeracion esta vigente", key="ej_resol", value=True,
                                          help="La resolucion DIAN que autoriza el rango de numeracion vigente.")
                num_rango   = st.checkbox("El numero esta dentro del rango autorizado", key="ej_rango", value=True,
                                          help="El numero de la factura cae dentro del rango de la resolucion.")

    tercero_ok = propietario_ok = cliente_ok = True
    destinatario_ok = remitente_ok = vehiculo_ok = facturable_ok = True
    opciones_ent = []
    if tipo == "Manifiesto" and env_rndc:
        opciones_ent = ["Tercero", "Propietario del vehiculo", "Cliente", "Destinatario", "Remitente", "Vehiculo", "Facturable"]
    elif tipo == "Remesa" and env_rndc:
        opciones_ent = ["Tercero", "Destinatario", "Facturable"]
    elif tipo in ("Factura", "NotaCredito") and env_dian:
        opciones_ent = ["Facturable", "Tercero"]
    elif tipo in ("Factura", "NotaCredito") and env_rndc:
        opciones_ent = ["Facturable"]

    if opciones_ent:
        with st.expander("Datos de entidades", expanded=True):
            st.markdown(_exp_hint("Seleccione las entidades con datos incorrectos. Si todo esta bien, deje esta lista vacia."), unsafe_allow_html=True)
            ent_mal = st.multiselect(
                "Entidades con problemas:", opciones_ent,
                default=st.session_state.get("ej_ent_mal", []),
                key="ej_ent_mal", placeholder="Ninguna — todos los datos estan correctos",
                help="Marque solo las entidades cuya informacion esta mal diligenciada.",
            )
            tercero_ok      = "Tercero"                  not in ent_mal
            propietario_ok  = "Propietario del vehiculo" not in ent_mal
            cliente_ok      = "Cliente"                  not in ent_mal
            destinatario_ok = "Destinatario"             not in ent_mal
            remitente_ok    = "Remitente"                not in ent_mal
            vehiculo_ok     = "Vehiculo"                 not in ent_mal
            facturable_ok   = "Facturable"               not in ent_mal

    fact_aceptada = tipo12 = False
    fact_consist = coord_ok = destino_rndc_ok = True
    conds_especiales = any([
        tipo == "NotaCredito" and env_dian,
        tipo in ("Factura", "NotaCredito") and env_rndc,
        tipo == "Remesa" and env_rndc,
    ])
    if conds_especiales:
        with st.expander("Condiciones especiales", expanded=False):
            st.markdown(_exp_hint("Abra esta seccion solo si alguna condicion aplica. Si no esta seguro, puede dejarla cerrada."), unsafe_allow_html=True)
            if tipo == "NotaCredito" and env_dian:
                fact_aceptada = st.checkbox("La factura asociada ya fue aceptada por el cliente", key="ej_factaceptada",
                                            help="El cliente ya respondio con aceptacion a la factura original.")
            if tipo in ("Factura", "NotaCredito") and env_rndc:
                tipo12       = st.checkbox("El documento es de tipo 12 (transporte)", key="ej_tipo12",
                                           help="El codigo de tipo en el XML es 12 — documentos de transporte.")
                fact_consist = st.checkbox("Los datos del facturable en el XML coinciden con la remesa", key="ej_fconsist", value=True,
                                           help="El XML generado contiene los mismos datos del facturable que la remesa.")
            if tipo == "Remesa" and env_rndc:
                coord_ok        = st.checkbox("Las coordenadas del destino son coherentes con la ciudad", key="ej_coord", value=True,
                                              help="Las coordenadas GPS corresponden al municipio de destino.")
                destino_rndc_ok = st.checkbox("El municipio de destino existe en el catalogo del RNDC", key="ej_destrndc", value=True,
                                              help="El municipio esta correctamente registrado en el catalogo oficial.")

    st.markdown("<div style='margin-bottom:.75rem'></div>", unsafe_allow_html=True)
    st.markdown(_tip("Revise que los sintomas esten completos. Una vez listo, presione el boton."), unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:.4rem'></div>", unsafe_allow_html=True)

    if st.button("Diagnosticar ahora", type="primary", use_container_width=True):
        hechos = [(tipo, True), ("Documento", True)]
        if env_dian: hechos.append(("EnvioDian", True))
        if env_rndc: hechos.append(("EnvioRNDC", True))
        for pred, val in [
            ("TieneInternet", internet), ("ErrorConexion", errorcon),
            ("TimeoutEnvio", timeout), ("FallaSOAP", falla_soap),
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

        with st.spinner("Analizando sintomas..."):
            try:
                finales, aplicadas, certezas = encadenamiento_adelante(REGLAS, hechos)
                diagnosticos = [h for h in finales if h not in hechos and h[1] and h[0] in PREDICADOS_DIAGNOSTICO]
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

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.55rem;margin:0 0 .9rem;font-size:.9rem;font-weight:700;color:#0f172a">'
        f'{_svg("bar-chart-2", 18, "#1d4ed8")}<span>Panel de diagnostico</span></div>',
        unsafe_allow_html=True,
    )

    # ── Sin diagnostico aun ───────────────────────────────────────────────
    if res is None:
        tipo_txt = tipo_label.strip() if tipo_label else None
        dest_txt = " + ".join(filter(None, ["DIAN" if env_dian else "", "RNDC" if env_rndc else ""]))

        st.markdown(_guide_panel(paso), unsafe_allow_html=True)

        if tipo_txt:
            rows = ""
            tipo_icon_name = _TIPO_ICON.get(tipo_txt, "document")
            rows += (f'<div class="summary-row"><span class="summary-lbl">Documento</span>'
                     f'<span style="display:inline-flex;align-items:center;gap:.4rem;flex:1">'
                     f'{_svg(tipo_icon_name,14,"#16a34a")}<strong style="color:#1e293b">{tipo_txt}</strong></span>'
                     f'{_svg("check",12,"#16a34a")}</div>')
            if dest_txt:
                rows += (f'<div class="summary-row"><span class="summary-lbl">Destino</span>'
                         f'<span style="display:inline-flex;align-items:center;gap:.4rem;flex:1">'
                         f'{_svg("send",14,"#16a34a")}<strong style="color:#1e293b">{dest_txt}</strong></span>'
                         f'{_svg("check",12,"#16a34a")}</div>')
            if not internet:
                rows += (f'<div class="summary-row summary-row-warn">'
                         f'<span class="summary-lbl">{_svg("alert-triangle",12,"#dc2626")} Alerta</span>'
                         f'Sin conexion a internet</div>')
            if rechazado:
                rows += (f'<div class="summary-row summary-row-warn">'
                         f'<span class="summary-lbl">{_svg("alert-triangle",12,"#dc2626")} Alerta</span>'
                         f'Documento rechazado</div>')
            if duplicado:
                rows += (f'<div class="summary-row summary-row-warn">'
                         f'<span class="summary-lbl">{_svg("alert-triangle",12,"#dc2626")} Alerta</span>'
                         f'Documento duplicado</div>')
            st.markdown(
                f'<div class="summary-panel" style="margin-top:.75rem">'
                f'<div class="summary-hdr">{_svg("clipboard-list",13)} PROGRESO DE LA CONSULTA</div>'
                f'{rows}'
                f'<div style="margin-top:.8rem;padding-top:.75rem;border-top:1px solid #f1f5f9;'
                f'font-size:.79rem;color:#94a3b8;text-align:center">'
                f'Complete los sintomas y presione <strong style="color:#1d4ed8">Diagnosticar ahora</strong>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        st.stop()

    # ── Error de validacion ───────────────────────────────────────────────
    if not res["ok"]:
        st.markdown(
            f'<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;'
            f'padding:.9rem 1.1rem;display:flex;align-items:flex-start;gap:.6rem;font-size:.86rem;color:#991b1b">'
            f'{_svg("x-circle",18,"#dc2626")}'
            f'<div><strong>Error en los datos:</strong> {res["error"]}</div></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    diagnosticos = res["diagnosticos"]
    aplicadas    = res["aplicadas"]
    certezas     = res["certezas"]
    finales_all  = res["finales"]
    errores      = [d for d in diagnosticos if d[0] not in EXITOS]
    exitos       = [d for d in diagnosticos if d[0] in EXITOS]
    conflictos   = detectar_conflictos(diagnosticos)
    tipo_txt     = res["tipo_label"].strip()
    dest_txt     = " + ".join(filter(None, ["DIAN" if res["env_dian"] else "", "RNDC" if res["env_rndc"] else ""]))

    # Banner
    if errores:
        n = len(errores)
        st.markdown(_result_banner("err", "x-circle",
                                   f'{n} problema{"s" if n>1 else ""} detectado{"s" if n>1 else ""}',
                                   f'{tipo_txt} → {dest_txt}'), unsafe_allow_html=True)
    elif exitos:
        st.markdown(_result_banner("ok", "check-circle",
                                   "Envio procesado correctamente",
                                   f'{tipo_txt} → {dest_txt}'), unsafe_allow_html=True)
    else:
        st.markdown(_result_banner("info", "info",
                                   "Sin diagnostico concluyente",
                                   "Los sintomas no coinciden con ningun patron conocido."), unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Problemas",         len(errores))
    m2.metric("Reglas disparadas", len(aplicadas))
    m3.metric("Exitos",            len(exitos))

    if exitos:
        st.markdown(_res_hdr("ok", "check-circle", "Resultados exitosos", len(exitos)), unsafe_allow_html=True)
        for d in exitos:
            cert = certezas.get(d, 1.0)
            titulo, accion = DESCRIPCIONES_DIAGNOSTICO.get(d[0], (d[0], ""))
            st.markdown(_dcard("ok", titulo, accion, cert), unsafe_allow_html=True)
            with st.expander("Ver razonamiento — por que esta conclusion?"):
                explicacion = porque(d[0], REGLAS, aplicadas, finales_all)
                if explicacion:
                    st.markdown("".join(_why_block(item) for item in explicacion), unsafe_allow_html=True)
                else:
                    st.caption("Sin informacion de razonamiento disponible.")

    if errores:
        st.markdown(_res_hdr("err", "x-circle", "Problemas detectados", len(errores)), unsafe_allow_html=True)
        for d in errores:
            cert = certezas.get(d, 1.0)
            titulo, accion = DESCRIPCIONES_DIAGNOSTICO.get(d[0], (d[0], ""))
            st.markdown(_dcard("err", titulo, accion, cert), unsafe_allow_html=True)
            with st.expander("Ver razonamiento — por que esta conclusion?"):
                explicacion = porque(d[0], REGLAS, aplicadas, finales_all)
                if explicacion:
                    st.markdown("".join(_why_block(item) for item in explicacion), unsafe_allow_html=True)
                else:
                    st.caption("Sin informacion de razonamiento disponible.")

    if conflictos:
        st.markdown(_res_hdr("warn", "alert-triangle", "Advertencias de coherencia"), unsafe_allow_html=True)
        for grupo in conflictos:
            st.markdown(_dcard("warn", "Diagnosticos contradictorios detectados",
                               f"Mutuamente excluyentes: {' vs '.join(grupo)}. Revise los sintomas ingresados.", 1.0),
                        unsafe_allow_html=True)

    if not errores and not exitos:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:.5rem;background:#f8fafc;'
            f'border:1px solid #e2e8f0;border-radius:9px;padding:.65rem .9rem;font-size:.84rem;color:#475569">'
            f'{_svg("info",15,"#64748b")}'
            f'<span>Ninguna regla fue disparada. Verifique que los sintomas esten completos.</span></div>',
            unsafe_allow_html=True,
        )

    with st.expander(f"Detalle tecnico — {len(aplicadas)} regla(s) disparada(s)"):
        if aplicadas:
            for nombre in aplicadas:
                cert_r = next((r["certeza"] for r in REGLAS if r["nombre"] == nombre), 1.0)
                desc   = DESCRIPCIONES_REGLAS.get(nombre, nombre)
                st.markdown(
                    f'<div class="tech-row">'
                    f'<span class="tech-code">{nombre}</span>'
                    f'<span class="tech-desc">{desc}</span>'
                    f'{_badge(cert_r)}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.caption("Ninguna regla fue disparada.")

    st.divider()
    st.caption("SBC · Actividad 4 · IA II · Los Libertadores · Galarza & Solano · 2026")
